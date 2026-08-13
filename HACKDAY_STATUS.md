# Hackday Status - AWS Biopharma

**Updated:** 2026-08-13  
**Workspace:** `/Users/byron/projects/active/aws-biopharma`  
**Current priority:** AWS Biopharma Hack Day demo surface.

## What Currently Works

- Local project folder exists and is now isolated as its own Git repo.
- `@strands-agents/sdk` is installed.
- Strands MCP config exists in `.mcp.json`.
- Convoke Bio MCP endpoint is configured in `.mcp.json` as `convoke-bio`.
- Convoke sign-in page has been opened for operator login.
- Static dashboard exists in `public/`.
- Snapshot data exists in `data/dashboard_snapshot.json` and
  `public/data/dashboard_snapshot.json`.
- Data puller exists at `scripts/pull_data.py`.

## Exact Demo Path

```bash
cd /Users/byron/projects/active/aws-biopharma
npm install
npm run pull:data
npm run serve
```

Open:

```text
http://127.0.0.1:8765
```

## Current Integration State

- Strands SDK: installed locally.
- Strands MCP: configured, requires an MCP client that can run `uvx`.
- Convoke Bio MCP: configured, auth required before tools are visible.
- AWS resources: none created by this scaffold.
- Bright Data: env placeholders only; no verified local tool smoke test yet.
- OpenAI: env placeholder only in this folder; do not assume usage unless a
  local `.env` is supplied and a smoke test is run.

## Licensing / Redistribution Boundary

- Source code: Apache License 2.0.
- Restrictive boundary: Apache 2.0 does not relicense datasets, provider
  outputs, API responses, credentials, or evidence records.
- Provider outputs from Convoke, Bright Data, Muni, Rowan, OnePot, Boltz, or
  similar services are local-only/redacted until usage and redistribution rights
  are verified.
- Do not commit `.env`, API keys, tokens, restricted records, or copied provider
  output.

## Team Split

- Demo runner: make `npm run serve` dashboard present cleanly.
- Integration owner: complete Convoke login and verify tool visibility.
- Strands owner: confirm MCP docs/tooling path and identify one agent workflow.
- Data/evidence owner: choose the smallest public biopharma evidence slice.
- Pitch owner: keep the claim bounded to a reproducible evidence workflow.

## Tasks That Can Safely Be Cut

- Full KG ingestion.
- Full BioCustody/Bio-Delta-G import.
- Hydra/Vithia/LongMemEval work.
- New model training.
- Any AWS service that does not improve the working demo.

## Supported Claims

- "This dashboard shows the AWS Biopharma hack workspace, integrations, and
  candidate demo lanes."
- "The workflow preserves source and integration state for reproducibility."
- "Provider/tool outputs are only shown when access and usage rights are
  verified."

## Prohibited / Unsupported Claims

- therapeutic efficacy
- clinical utility
- diagnosis
- treatment recommendation
- measured rescue
- biological rejuvenation
- provider-data redistribution unless rights are verified
