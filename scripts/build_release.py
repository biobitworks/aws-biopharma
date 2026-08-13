#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
CUSTODY = ROOT / "custody"
FCO_DIR = CUSTODY / "fco"
PRIVATE_DIR = ROOT / ".custody-private"
PRIVATE_KEY = PRIVATE_DIR / "signing-key.pem"
PUBLIC_KEY = CUSTODY / "public-key.pem"
MANIFEST = CUSTODY / "release-manifest.json"
ROOT_TXT = CUSTODY / "release-root.txt"
SIG = CUSTODY / "release-root.sig"

ARTIFACTS = [
    ("AGENTS.md", "project_governance_artifact", "PROJECT_POLICY", "PUBLIC", "Apache-2.0"),
    ("README.md", "project_readme", "PROJECT_OVERVIEW", "PUBLIC", "Apache-2.0"),
    ("DATA_POLICY.md", "project_governance_artifact", "PROJECT_POLICY", "PUBLIC", "Apache-2.0"),
    ("docs/IP_AWARE_FCG.md", "project_governance_artifact", "PROJECT_POLICY", "PUBLIC", "Apache-2.0"),
    ("docs/TEAM_DATABASE_BUILD_PROMPT.md", "project_governance_artifact", "PROJECT_POLICY", "PUBLIC", "Apache-2.0"),
    ("docs/KEY_MANAGEMENT.md", "project_governance_artifact", "PROJECT_POLICY", "PUBLIC", "Apache-2.0"),
    ("CHAIN_OF_CUSTODY_DESIGN.md", "project_governance_artifact", "PROJECT_POLICY", "PUBLIC", "Apache-2.0"),
    ("HACKDAY_STATUS.md", "project_status", "PROJECT_STATUS", "PUBLIC", "Apache-2.0"),
    ("TEAM_UPDATE.md", "team_handoff", "PROJECT_STATUS", "PUBLIC", "Apache-2.0"),
    ("public/index.html", "dashboard_ui", "DEMO_UI", "PUBLIC", "Apache-2.0"),
    ("public/app.js", "dashboard_ui", "DEMO_UI", "PUBLIC", "Apache-2.0"),
    ("public/styles.css", "dashboard_ui", "DEMO_UI", "PUBLIC", "Apache-2.0"),
    ("scripts/build_release.py", "release_tool", "CUSTODY_RECEIPT", "PUBLIC", "Apache-2.0"),
    ("scripts/verify_release.py", "release_tool", "CUSTODY_RECEIPT", "PUBLIC", "Apache-2.0"),
    ("custody/verify-release.py", "release_tool", "CUSTODY_RECEIPT", "PUBLIC", "Apache-2.0"),
    ("public/assets/fcg_perturbation_star_chart.svg", "figure", "REPRODUCIBLE_FIGURE", "PUBLIC", "Apache-2.0"),
    ("data/figures/fcg_perturbation_star_chart.receipt.json", "figure_receipt", "REPRODUCIBLE_FIGURE", "PUBLIC", "Apache-2.0"),
    ("data/openai_redteam_status.json", "redteam_receipt", "PROJECT_STATUS", "PUBLIC", "SOURCE_TERMS_APPLY"),
    ("data/dashboard_snapshot.json", "dashboard_data", "DEMO_DATA", "PUBLIC", "SOURCE_TERMS_APPLY"),
    ("data/magicstudiobox/deliverables/FINAL_METRICS.json", "result_metrics", "REPURPOSING_HYPOTHESIS", "PUBLIC", "SOURCE_TERMS_APPLY"),
    ("data/magicstudiobox/deliverables/REPURPOSING_EVIDENCE_TABLE.md", "evidence_table", "REPURPOSING_HYPOTHESIS", "PUBLIC", "SOURCE_TERMS_APPLY"),
    ("data/magicstudiobox/runs/primary/repurposing_evidence_table.csv", "evidence_table", "REPURPOSING_HYPOTHESIS", "PUBLIC", "SOURCE_TERMS_APPLY"),
    ("data/magicstudiobox/runs/primary/candidate_ranking.csv", "candidate_ranking", "REPURPOSING_HYPOTHESIS", "PUBLIC", "SOURCE_TERMS_APPLY"),
    ("data/magicstudiobox/runs/primary/similar_drug_evidence_graph.json", "evidence_graph", "REPURPOSING_HYPOTHESIS", "PUBLIC", "SOURCE_TERMS_APPLY"),
    ("data/magicstudiobox/runs/primary/merkle_receipt.json", "custody_receipt", "CUSTODY_RECEIPT", "PUBLIC", "SOURCE_TERMS_APPLY"),
    ("data/magicstudiobox/runs/primary/tamper_test.json", "tamper_test", "CUSTODY_RECEIPT", "PUBLIC", "SOURCE_TERMS_APPLY"),
]

PARENTS = {
    "docs/IP_AWARE_FCG.md": ["DATA_POLICY.md"],
    "docs/TEAM_DATABASE_BUILD_PROMPT.md": ["DATA_POLICY.md", "docs/IP_AWARE_FCG.md"],
    "docs/KEY_MANAGEMENT.md": ["CHAIN_OF_CUSTODY_DESIGN.md"],
    "public/assets/fcg_perturbation_star_chart.svg": [
        "data/magicstudiobox/runs/primary/similar_drug_evidence_graph.json",
        "data/magicstudiobox/deliverables/FINAL_METRICS.json",
        "data/magicstudiobox/runs/primary/merkle_receipt.json",
        "data/magicstudiobox/runs/primary/tamper_test.json",
    ],
    "data/figures/fcg_perturbation_star_chart.receipt.json": [
        "public/assets/fcg_perturbation_star_chart.svg",
        "data/magicstudiobox/runs/primary/similar_drug_evidence_graph.json",
    ],
    "data/dashboard_snapshot.json": [
        "data/figures/fcg_perturbation_star_chart.receipt.json",
        "data/magicstudiobox/deliverables/FINAL_METRICS.json",
        "data/openai_redteam_status.json",
    ],
}


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def merkle_root(ids: Iterable[str]) -> str:
    level = [bytes.fromhex(item) for item in sorted(ids)]
    if not level:
        return hashlib.sha256(b"").hexdigest()
    while len(level) > 1:
        next_level = []
        for index in range(0, len(level), 2):
            left = level[index]
            right = level[index + 1] if index + 1 < len(level) else left
            next_level.append(hashlib.sha256(left + right).digest())
        level = next_level
    return level[0].hex()


def ensure_keypair() -> None:
    PRIVATE_DIR.mkdir(parents=True, exist_ok=True)
    CUSTODY.mkdir(parents=True, exist_ok=True)
    if not PRIVATE_KEY.exists():
        subprocess.run(
            ["openssl", "genpkey", "-algorithm", "RSA", "-pkeyopt", "rsa_keygen_bits:3072", "-out", str(PRIVATE_KEY)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        PRIVATE_KEY.chmod(0o600)
    subprocess.run(
        ["openssl", "pkey", "-in", str(PRIVATE_KEY), "-pubout", "-out", str(PUBLIC_KEY)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def sign_root() -> None:
    subprocess.run(
        ["openssl", "dgst", "-sha256", "-sign", str(PRIVATE_KEY), "-out", str(SIG), str(ROOT_TXT)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main() -> int:
    CUSTODY.mkdir(parents=True, exist_ok=True)
    if FCO_DIR.exists():
        shutil.rmtree(FCO_DIR)
    FCO_DIR.mkdir(parents=True, exist_ok=True)
    ensure_keypair()

    path_to_fco_id: dict[str, str] = {}
    pending_records: list[tuple[str, dict[str, object]]] = []

    for artifact, fco_type, claim_ceiling, disclosure, license_value in ARTIFACTS:
        path = ROOT / artifact
        if not path.exists():
            raise FileNotFoundError(artifact)
        record = {
            "schema": "aws-biopharma.fco.v1",
            "fco_type": fco_type,
            "artifact": artifact,
            "payload_sha256": f"sha256:{sha256_file(path)}",
            "payload_bytes": path.stat().st_size,
            "parents": [],
            "claim_ceiling": claim_ceiling,
            "disclosure": disclosure,
            "license": license_value,
            "signature_scope": "release_root",
        }
        fco_id = sha256_bytes(canonical_json(record))
        record["fco_id"] = f"fco:{fco_id}"
        path_to_fco_id[artifact] = record["fco_id"]
        pending_records.append((artifact, record))

    fcos = []
    for artifact, record in pending_records:
        record["parents"] = [path_to_fco_id[parent] for parent in PARENTS.get(artifact, [])]
        fco_id = sha256_bytes(canonical_json({k: v for k, v in record.items() if k != "fco_id"}))
        record["fco_id"] = f"fco:{fco_id}"
        path_to_fco_id[artifact] = record["fco_id"]
        fcos.append(record)

    root = merkle_root(record["fco_id"].split(":", 1)[1] for record in fcos)
    ROOT_TXT.write_text(root + "\n", encoding="utf-8")
    sign_root()

    for record in fcos:
        leaf = FCO_DIR / (record["artifact"].replace("/", "__") + ".fco.json")
        leaf.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    manifest = {
        "schema": "aws-biopharma.release-manifest.v1",
        "release_name": "aws-biopharma-hackday",
        "release_root": root,
        "signature": {
            "algorithm": "RSA-SHA256",
            "signature_file": str(SIG.relative_to(ROOT)),
            "public_key_file": str(PUBLIC_KEY.relative_to(ROOT)),
            "signature_base64": base64.b64encode(SIG.read_bytes()).decode("ascii"),
        },
        "claim_ceiling": "REPURPOSING_HYPOTHESIS / reproducible evidence workflow only",
        "private_key_policy": "private key stays local in .custody-private/signing-key.pem and is ignored by git",
        "fcos": fcos,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"release_root": root, "fcos": len(fcos), "signature": str(SIG.relative_to(ROOT))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
