#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "custody/release-manifest.json"
ROOT_TXT = ROOT / "custody/release-root.txt"
SIG = ROOT / "custody/release-root.sig"
PUBLIC_KEY = ROOT / "custody/public-key.pem"
LEDGER_STATUS = ROOT / "custody/ledger-artifact-status.json"
PROHIBITED_CLAIM_TERMS = [
    "therapeutic efficacy",
    "clinical utility",
    "treatment recommendation",
    "measured rescue",
    "biological rejuvenation",
]
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----"),
    re.compile(r"OPENAI_API_KEY=sk-[A-Za-z0-9_\\-]{12,}"),
    re.compile(r"CONVOKE_MCP_TOKEN=[A-Za-z0-9_\\-\\.]{20,}"),
]
CLAIM_POLICY_ARTIFACTS = {
    "DATA_POLICY.md",
    "AGENTS.md",
    "CHAIN_OF_CUSTODY_DESIGN.md",
    "HACKDAY_STATUS.md",
    "README.md",
    "TEAM_UPDATE.md",
    "scripts/build_release.py",
    "scripts/verify_release.py",
    "custody/verify-release.py",
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


def print_status(name: str, ok: bool, detail: str = "") -> bool:
    suffix = f" - {detail}" if detail else ""
    print(f"{name:<28} {'PASS' if ok else 'FAIL'}{suffix}")
    return ok


def main() -> int:
    ok = True
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    fcos = manifest.get("fcos", [])
    fco_ids = {record["fco_id"] for record in fcos}

    hashes_ok = True
    fco_ids_ok = True
    ceilings_ok = True
    rights_ok = True
    for record in fcos:
        artifact = ROOT / record["artifact"]
        expected_hash = record["payload_sha256"].split(":", 1)[1]
        hashes_ok = hashes_ok and artifact.exists() and sha256_file(artifact) == expected_hash

        recomputed = sha256_bytes(canonical_json({k: v for k, v in record.items() if k != "fco_id"}))
        fco_ids_ok = fco_ids_ok and record["fco_id"] == f"fco:{recomputed}"

        text = artifact.read_text(encoding="utf-8", errors="ignore").lower()
        if record["artifact"] not in CLAIM_POLICY_ARTIFACTS:
            ceilings_ok = ceilings_ok and not any(term in text for term in PROHIBITED_CLAIM_TERMS)
        if record["license"] == "SOURCE_TERMS_APPLY":
            rights_ok = rights_ok and record["disclosure"] == "PUBLIC" and bool(record["claim_ceiling"])

    ok &= print_status("Artifact hashes", hashes_ok)
    ok &= print_status("FCO roots", fco_ids_ok)

    parent_closure = all(parent in fco_ids for record in fcos for parent in record.get("parents", []))
    ok &= print_status("FCG parent closure", parent_closure)

    computed_root = merkle_root(record["fco_id"].split(":", 1)[1] for record in fcos)
    recorded_root = ROOT_TXT.read_text(encoding="utf-8").strip()
    manifest_root_ok = manifest["release_root"] == recorded_root == computed_root
    ok &= print_status("Merkle root", manifest_root_ok, computed_root[:16])

    verify = subprocess.run(
        ["openssl", "dgst", "-sha256", "-verify", str(PUBLIC_KEY), "-signature", str(SIG), str(ROOT_TXT)],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    ok &= print_status("Release signature", verify.returncode == 0, verify.stdout.strip() or verify.stderr.strip())
    ok &= print_status("Public key verification", PUBLIC_KEY.exists() and "PRIVATE KEY" not in PUBLIC_KEY.read_text())
    ok &= print_status("Rights-source provenance", rights_ok)
    ok &= print_status("Claim ceilings", ceilings_ok)

    tracked_files = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    ).stdout.splitlines()
    leak_hits = []
    for relpath in tracked_files:
        path = ROOT / relpath
        if path.is_dir():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            leak_hits.append(relpath)
    ok &= print_status("Private-key leak scan", not leak_hits, ", ".join(leak_hits[:5]))

    manifest_artifacts = {record["artifact"] for record in fcos}
    ledger_payload = json.loads(LEDGER_STATUS.read_text(encoding="utf-8"))
    ledger_hash_coverage = True
    for item in ledger_payload.get("artifacts", []):
        path = ROOT / item["path"]
        if not path.exists():
            continue
        ledger_hash_coverage = (
            ledger_hash_coverage
            and item.get("status") == "present"
            and item.get("payload_sha256") == f"sha256:{sha256_file(path)}"
            and item["path"] in manifest_artifacts
        )
    ok &= print_status("Ledger hash coverage", ledger_hash_coverage)

    print()
    print(f"CUSTODY STATUS: {'VERIFIED' if ok else 'FAILED'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
