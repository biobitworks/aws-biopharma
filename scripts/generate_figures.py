#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import html
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = ROOT / "data/magicstudiobox/runs/primary/similar_drug_evidence_graph.json"
FINAL_METRICS = ROOT / "data/magicstudiobox/deliverables/FINAL_METRICS.json"
MERKLE_RECEIPT = ROOT / "data/magicstudiobox/runs/primary/merkle_receipt.json"
TAMPER_TEST = ROOT / "data/magicstudiobox/runs/primary/tamper_test.json"
OUT_SVG = ROOT / "public/assets/fcg_perturbation_star_chart.svg"
OUT_RECEIPT = ROOT / "data/figures/fcg_perturbation_star_chart.receipt.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def short_label(value: str) -> str:
    label = value.split("|")[0]
    return label[:32]


def build_graph() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    rows = read_json(GRAPH_PATH)
    edges = []
    nodes: dict[str, dict[str, str]] = {}
    for row in rows:
        subject = str(row.get("subject") or "")
        target = str(row.get("object") or "")
        predicate = str(row.get("predicate") or "")
        if not subject or not target or not predicate:
            continue
        nodes.setdefault(subject, {"id": subject, "label": short_label(subject), "kind": "candidate"})
        kind = "comparator" if predicate == "CLINICALLY_ADJACENT" else "mechanism"
        nodes.setdefault(target, {"id": target, "label": short_label(target), "kind": kind})
        edges.append(
            {
                "source": subject,
                "target": target,
                "predicate": predicate,
                "status": str(row.get("evidence_status") or ""),
                "method": str(row.get("method") or ""),
                "value": str(row.get("value") or ""),
            }
        )
    return (
        sorted(nodes.values(), key=lambda item: (item["kind"], item["id"])),
        sorted(edges, key=lambda item: (item["source"], item["predicate"], item["target"], item["status"])),
    )


def svg_text(x: float, y: float, value: str, klass: str = "label") -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{klass}">{html.escape(value)}</text>'


def build_svg() -> str:
    nodes, edges = build_graph()
    metrics = read_json(FINAL_METRICS)
    merkle = read_json(MERKLE_RECEIPT)
    tamper = read_json(TAMPER_TEST)

    candidate = next((node for node in nodes if node["kind"] == "candidate"), nodes[0])
    leaves = [node for node in nodes if node["id"] != candidate["id"]]

    width, height = 1200, 760
    cx, cy = width / 2, 355
    positions = {candidate["id"]: (cx, cy)}
    for index, node in enumerate(leaves):
        angle = -math.pi / 2 + (2 * math.pi * index / max(len(leaves), 1))
        radius = 250 if node["kind"] == "comparator" else 320
        positions[node["id"]] = (cx + math.cos(angle) * radius, cy + math.sin(angle) * radius)

    edge_markup = []
    for edge in edges:
        source = positions.get(edge["source"])
        target = positions.get(edge["target"])
        if not source or not target:
            continue
        klass = "edge mechanism-edge" if edge["predicate"] == "MECHANISM_SIMILAR" else "edge adjacent-edge"
        edge_markup.append(
            f'<line x1="{source[0]:.1f}" y1="{source[1]:.1f}" x2="{target[0]:.1f}" y2="{target[1]:.1f}" class="{klass}" />'
        )

    node_markup = []
    for node in nodes:
        x, y = positions[node["id"]]
        radius = 50 if node["kind"] == "candidate" else 28
        node_markup.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius}" class="node {node["kind"]}" />')
        node_markup.append(svg_text(x, y + radius + 22, node["label"], "label"))

    merkle_root = str(
        merkle.get("root")
        or merkle.get("merkle_root")
        or merkle.get("fco_root")
        or merkle.get("receipt_sha256")
        or "recorded"
    )
    tamper_status = str(tamper.get("status") or tamper.get("tamper_test") or "recorded")
    top_candidate = str(metrics.get("top_candidate") or "top candidate")
    claim_ceiling = str(metrics.get("claim_ceiling") or "REPURPOSING_HYPOTHESIS")

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">FCG perturbation evidence star chart</title>
  <desc id="desc">Deterministic star chart from MagicStudioBox evidence graph, final metrics, Merkle receipt, and tamper test.</desc>
  <defs>
    <style>
      .bg {{ fill: #f7f8fb; }}
      .frame {{ fill: #ffffff; stroke: #d8dde6; stroke-width: 1.5; }}
      .title {{ fill: #111827; font: 700 28px Inter, Arial, sans-serif; }}
      .subtitle {{ fill: #5b6472; font: 15px Inter, Arial, sans-serif; }}
      .label {{ fill: #111827; font: 700 13px Inter, Arial, sans-serif; text-anchor: middle; }}
      .small {{ fill: #5b6472; font: 12px Inter, Arial, sans-serif; }}
      .node {{ stroke: #ffffff; stroke-width: 4; }}
      .candidate {{ fill: #136f63; }}
      .comparator {{ fill: #7c3f12; }}
      .mechanism {{ fill: #51617a; }}
      .edge {{ stroke-linecap: round; opacity: 0.82; }}
      .mechanism-edge {{ stroke: #136f63; stroke-width: 2.6; }}
      .adjacent-edge {{ stroke: #98a2b3; stroke-width: 1.5; stroke-dasharray: 6 6; }}
      .receipt {{ fill: #101826; }}
      .receipt-text {{ fill: #ecfdf5; font: 12px "SFMono-Regular", Consolas, monospace; }}
    </style>
  </defs>
  <rect class="bg" width="{width}" height="{height}" />
  <rect class="frame" x="28" y="26" width="{width - 56}" height="{height - 52}" rx="10" />
  <text x="56" y="72" class="title">FCG perturbation evidence star chart</text>
  <text x="56" y="101" class="subtitle">Center: {html.escape(top_candidate)}. Spokes: mechanism-similar and clinically-adjacent evidence nodes.</text>
  <g id="edges">
    {chr(10).join(edge_markup)}
  </g>
  <g id="nodes">
    {chr(10).join(node_markup)}
  </g>
  <g id="legend">
    <circle cx="76" cy="660" r="9" class="node candidate" />
    <text x="94" y="664" class="small">candidate</text>
    <circle cx="190" cy="660" r="9" class="node comparator" />
    <text x="208" y="664" class="small">clinically adjacent comparator</text>
    <circle cx="410" cy="660" r="9" class="node mechanism" />
    <text x="428" y="664" class="small">mechanism/evidence node</text>
  </g>
  <rect class="receipt" x="56" y="686" width="{width - 112}" height="42" rx="6" />
  <text x="72" y="711" class="receipt-text">claim={html.escape(claim_ceiling)} | merkle={html.escape(merkle_root[:24])} | tamper={html.escape(tamper_status)} | source=similar_drug_evidence_graph.json</text>
</svg>
'''


def main() -> int:
    OUT_SVG.parent.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    svg = build_svg()
    OUT_SVG.write_text(svg, encoding="utf-8")

    source_paths = [GRAPH_PATH, FINAL_METRICS, MERKLE_RECEIPT, TAMPER_TEST]
    receipt = {
        "schema": "aws-biopharma.figure-receipt.v1",
        "figure": str(OUT_SVG.relative_to(ROOT)),
        "figure_sha256": sha256_file(OUT_SVG),
        "generator": str(Path(__file__).relative_to(ROOT)),
        "generator_sha256": sha256_file(Path(__file__)),
        "source_files": [
            {
                "path": str(path.relative_to(ROOT)),
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
            }
            for path in source_paths
        ],
        "determinism": {
            "layout": "fixed radial star chart sorted by node id and edge tuple",
            "volatile_fields": "none",
            "claim_ceiling": "source-derived, no clinical efficacy claim",
        },
    }
    OUT_RECEIPT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"figure": receipt["figure"], "figure_sha256": receipt["figure_sha256"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
