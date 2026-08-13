#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import shutil
import sys
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DATA = ROOT / "public" / "data"
LOCAL_DATA = ROOT / "data"
PROBLEM_STATEMENTS = Path("/Users/byron/projects/inbox/Biopharma Hack Day Problem Statements.md")

STRANDS_URLS = {
    "home": "https://strandsagents.com/",
    "llms": "https://strandsagents.com/llms.txt",
    "llms_full": "https://strandsagents.com/llms-full.txt",
}


@dataclass
class FetchResult:
    key: str
    url: str
    status: str
    bytes: int
    error: str | None = None


class TitleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._in_title = False
        self.title_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data.strip())

    @property
    def title(self) -> str:
        return " ".join(part for part in self.title_parts if part).strip()


def fetch_text(url: str) -> tuple[str, FetchResult]:
    request = urllib.request.Request(url, headers={"user-agent": "aws-biopharma-dashboard/0.1"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read()
        return raw.decode("utf-8", errors="replace"), FetchResult(
            key="",
            url=url,
            status="ok",
            bytes=len(raw),
        )
    except (urllib.error.URLError, TimeoutError) as exc:
        return "", FetchResult(key="", url=url, status="error", bytes=0, error=str(exc))


def parse_problem_statements(text: str) -> list[dict[str, str]]:
    statements: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    heading = re.compile(r"^\*\*(\d+)\\\.\s*(?:\*\*)?\s*(.*?)\s*\*\*\s*$")

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = heading.match(line)
        if match:
            if current:
                statements.append(current)
            number, title = match.groups()
            title = re.sub(r"^\*\*|\*\*$", "", title).strip()
            current = {"id": number, "title": " ".join(title.split()), "description": ""}
            continue
        if current:
            current["description"] = " ".join([current["description"], line]).strip()

    if current:
        statements.append(current)

    return statements


def parse_llms_links(text: str) -> list[dict[str, str]]:
    links: list[dict[str, str]] = []
    link_pattern = re.compile(r"^\s*-\s+(?:\[([^\]]+)\]\(([^)]+)\)|([A-Za-z].*?))(?::\s*(.*))?$")
    current_section = "Docs"
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- ") and not stripped.startswith("- ["):
            section = stripped[2:].strip()
            if section and len(section) < 80 and ":" not in section:
                current_section = section
        match = link_pattern.match(line)
        if not match:
            continue
        label, url, plain, description = match.groups()
        if not url:
            continue
        links.append(
            {
                "section": current_section,
                "title": " ".join((label or plain or "").split()),
                "url": url,
                "description": " ".join((description or "").split()),
            }
        )
    return links


def find_install_commands(texts: Iterable[str]) -> list[str]:
    commands: set[str] = set()
    patterns = [
        r"pip install strands-agents(?:-[a-z0-9-]+)?",
        r"npm install @strands-agents/sdk",
        r"uvx strands-agents-mcp-server",
    ]
    for text in texts:
        for pattern in patterns:
            commands.update(re.findall(pattern, text, flags=re.I))
    return sorted(commands)


def redact_env(names: Iterable[str]) -> list[dict[str, object]]:
    placeholders = {"", "...", "changeme", "paste_key_here", "paste_token_here"}
    values: list[dict[str, object]] = []
    for name in names:
        value = os.getenv(name, "")
        values.append(
            {
                "name": name,
                "present": bool(value and value.lower() not in placeholders),
                "length": len(value) if value else 0,
            }
        )
    return values


def main() -> int:
    LOCAL_DATA.mkdir(parents=True, exist_ok=True)
    PUBLIC_DATA.mkdir(parents=True, exist_ok=True)

    fetched: dict[str, str] = {}
    fetch_results: list[FetchResult] = []
    for key, url in STRANDS_URLS.items():
        text, result = fetch_text(url)
        result.key = key
        fetched[key] = text
        fetch_results.append(result)
        if text:
            (LOCAL_DATA / f"source_{key}.txt").write_text(text, encoding="utf-8")

    parser = TitleParser()
    parser.feed(fetched.get("home", ""))

    problem_text = PROBLEM_STATEMENTS.read_text(encoding="utf-8") if PROBLEM_STATEMENTS.exists() else ""
    problem_statements = parse_problem_statements(problem_text)

    llms_text = fetched.get("llms", "")
    links = parse_llms_links(llms_text)
    selected_docs = [
        item
        for item in links
        if item["title"].lower()
        in {
            "quickstart: python",
            "using mcp tools",
            "amazon-bedrock",
            "operating-agents-in-production",
            "deploy_to_bedrock_agentcore",
            "responsible-ai",
            "guardrails",
            "observability",
            "metrics",
        }
    ]

    snapshot = {
        "schema": "aws-biopharma.dashboard.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project": {
            "name": "AWS Biopharma Hack Day",
            "path": str(ROOT),
            "boundaries": [
                "Separate from BioCustody, Bio-Delta-G, StateShift, and Hydra.",
                "No AWS resources created by the pull script.",
                "No paid provider APIs called by the pull script.",
            ],
        },
        "strands": {
            "site": STRANDS_URLS["home"],
            "title": parser.title or "Strands Agents",
            "summary": "Strands Agents is an open source SDK for building production agents with tools, MCP integration, model providers, guardrails, observability, and deployment paths.",
            "install_commands": find_install_commands(fetched.values()),
            "mcp_config": {
                "command": "uvx",
                "args": ["strands-agents-mcp-server"],
            },
            "selected_docs": selected_docs[:12],
            "fetches": [asdict(result) for result in fetch_results],
        },
        "biopharma": {
            "problem_statement_source": str(PROBLEM_STATEMENTS),
            "problem_statements": problem_statements,
            "candidate_lanes": [
                {
                    "id": "trial-efficiency",
                    "title": "Running more efficient trials",
                    "fit": "Use Strands tools to retrieve prior trial records, normalize endpoints, and produce pattern summaries with traceable sources.",
                },
                {
                    "id": "repurposing",
                    "title": "Repurposing opportunities",
                    "fit": "Use Bright Data or other retrieval tools to collect public drug/target/trial progress evidence, then rank opportunities with source custody.",
                },
                {
                    "id": "patient-observability",
                    "title": "Treatment observability for patients",
                    "fit": "Build a patient-facing treatment option monitor that separates trial availability from medical advice.",
                },
                {
                    "id": "claims-adjudication",
                    "title": "Claims Adjudication Simulator",
                    "fit": "Model payer policy reading as a guarded tool workflow with approve/deny rationale and citations.",
                },
                {
                    "id": "regulated-content",
                    "title": "Reducing Redundant Content Development at Scale",
                    "fit": "Use Strands agents to transform approved source material into audience-specific outputs while preserving traceability.",
                },
            ],
        },
        "integrations": {
            "env": redact_env(
                [
                    "AWS_PROFILE",
                    "AWS_REGION",
                    "CONVOKE_MCP_TOKEN",
                    "BRIGHTDATA_API_KEY",
                    "BRIGHT_DATA_API_KEY",
                    "BRIGHTDATA_TOKEN",
                    "BRIGHT_DATA_TOKEN",
                ]
            )
        },
    }

    out = LOCAL_DATA / "dashboard_snapshot.json"
    public_out = PUBLIC_DATA / "dashboard_snapshot.json"
    out.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    shutil.copyfile(out, public_out)
    print(json.dumps({"wrote": [str(out), str(public_out)], "problem_statements": len(problem_statements)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
