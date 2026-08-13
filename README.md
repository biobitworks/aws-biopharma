# AWS Biopharma Hack Day

Local working folder:

```text
/Users/byron/projects/active/aws-biopharma
```

This project is the AWS Biopharma Hack Day workspace. It is separate from BioCustody, Bio-Delta-G, and StateShift.

## Current Setup

- Strands Agents docs/data puller.
- Project-local Strands MCP config in `.mcp.json`.
- Convoke Bio MCP endpoint configured in `.mcp.json`; login/auth is required
  before tools are visible.
- Bright Data Web MCP configured in `.mcp.json`; token is read from the local
  environment or `.env`.
- OpenAI is wired through Strands for a local smoke agent.
- Static dashboard in `public/`.
- Local data snapshots in `data/` and `public/data/`.
- MagicStudioBox overnight artifacts included under `data/magicstudiobox/`.
- Chain-of-custody design in `CHAIN_OF_CUSTODY_DESIGN.md`.

## Run

```bash
cd /Users/byron/projects/active/aws-biopharma
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
npm install
npm run agent:openai
npm run status:brightdata
npm run build:figures
npm run pull:data
npm run serve
```

Open:

```text
http://127.0.0.1:8765
```

## Data Sources

- Strands Agents docs and `llms.txt` from `https://strandsagents.com`.
- Local AWS Biopharma problem statements from `/Users/byron/projects/inbox/Biopharma Hack Day Problem Statements.md`.
- Bounded MagicStudioBox overnight run artifacts copied into
  `data/magicstudiobox/`, including result tables, Merkle receipt, tamper test,
  and final metrics.

## Boundaries

- No AWS resources are created by this scaffold.
- No paid APIs are called by `scripts/pull_data.py`.
- Do not make BioCustody, Bio-Delta-G, or StateShift claims from this dashboard
  beyond explicitly imported source artifacts and their documented claim
  ceiling.
- Source code is Apache 2.0. Data, provider outputs, API responses,
  credentials, and evidence records are not relicensed by this repo and remain
  governed by source/provider terms.

## Chain Of Custody

The dashboard lists included MagicStudioBox artifacts with SHA-256 hashes and
points to the overnight Merkle receipt and tamper-test result. The operator/agent
conversation is represented through status files, handoff notes, hashes,
receipts, and Git commits; raw private chat text and secrets are not published.

Judge-facing figures are repeatable FCG/FCO artifacts. Rebuild the perturbation
star chart with:

```bash
npm run build:figures
```

The figure receipt is written to
`data/figures/fcg_perturbation_star_chart.receipt.json`.

## Convoke

Sign in here:

```text
https://platform.convoke.bio/sign-in?redirect_url=https%3A%2F%2Fplatform.convoke.bio%2F
```

If a bearer token is issued for local MCP use, place it only in `.env`:

```text
CONVOKE_MCP_TOKEN=...
```

## OpenAI

The local Strands smoke path uses `OPENAI_API_KEY` from the shell environment
or `.env` without writing the key to disk:

```bash
npm run agent:openai
npm run pull:data
```

Set `OPENAI_MODEL` to override the default `gpt-4o-mini`.

## Bright Data

The local MCP server is `bright-data` in `.mcp.json` and uses
`@brightdata/mcp@2.6.0`, pinned to avoid current MCP SDK audit advisories. It
reads one of these local-only token aliases:

```text
BRIGHTDATA_API_KEY
BRIGHT_DATA_API_KEY
BRIGHTDATA_TOKEN
BRIGHT_DATA_TOKEN
```

Run the status check without spending credits:

```bash
npm run status:brightdata
npm run pull:data
```
