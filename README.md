# AWS Biopharma Hack Day

Local working folder:

```text
/Users/byron/projects/active/aws-biopharma
```

This project is the AWS Biopharma Hack Day workspace. It is separate from BioCustody, Bio-Delta-G, StateShift, and Hydra.

## Current Setup

- Strands Agents docs/data puller.
- Project-local Strands MCP config in `.mcp.json`.
- Convoke Bio MCP endpoint configured in `.mcp.json`; login/auth is required
  before tools are visible.
- Static dashboard in `public/`.
- Local data snapshots in `data/` and `public/data/`.

## Run

```bash
cd /Users/byron/projects/active/aws-biopharma
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
npm install
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

## Boundaries

- No AWS resources are created by this scaffold.
- No paid APIs are called by `scripts/pull_data.py`.
- Do not make BioCustody, Bio-Delta-G, StateShift, or Hydra claims from this dashboard unless explicitly imported as source material.
- Source code is Apache 2.0. Data, provider outputs, API responses,
  credentials, and evidence records are not relicensed by this repo and remain
  governed by source/provider terms.

## Convoke

Sign in here:

```text
https://platform.convoke.bio/sign-in?redirect_url=https%3A%2F%2Fplatform.convoke.bio%2F
```

If a bearer token is issued for local MCP use, place it only in `.env`:

```text
CONVOKE_MCP_TOKEN=...
```
