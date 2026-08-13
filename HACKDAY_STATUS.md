# Hackday Status - AWS Biopharma

**Updated:** 2026-08-13  
**Workspace:** `/Users/byron/projects/active/aws-biopharma`  
**Current priority:** AWS Biopharma Hack Day demo surface.

## What Currently Works

- Local project folder exists and is now isolated as its own Git repo.
- `@strands-agents/sdk` is installed.
- OpenAI is wired through Strands with `scripts/openai_agent_smoke.mjs`.
- Strands MCP config exists in `.mcp.json`.
- Convoke Bio MCP endpoint is configured in `.mcp.json` as `convoke-bio`.
- Bright Data Web MCP is configured in `.mcp.json` as `bright-data`.
- Convoke sign-in page has been opened for operator login.
- Static dashboard exists in `public/`.
- Snapshot data exists in `data/dashboard_snapshot.json` and
  `public/data/dashboard_snapshot.json`.
- Data puller exists at `scripts/pull_data.py`.
- OpenAI agent status is written to `data/openai_agent_status.json` and
  mirrored into dashboard data after `npm run pull:data`.
- Bright Data status is written to `data/brightdata_status.json` and mirrored
  into dashboard data after `npm run pull:data`.
- MagicStudioBox overnight outputs are included under `data/magicstudiobox/`.
- Chain-of-custody design is documented in `CHAIN_OF_CUSTODY_DESIGN.md` and
  rendered in the dashboard snapshot.
- FCG perturbation star chart is generated repeatably from committed artifacts
  with `npm run build:figures`.
- Signed release-root custody is built with `npm run build:release` and checked
  with `npm run verify:release`.
- Teammate BioCustody/FTO ledger import contract exists in
  `custody/required-ledger-artifacts.json`; present ledger files are hashed,
  wrapped as FCO leaves, and checked by `npm run verify:release`.

## Exact Demo Path

```bash
cd /Users/byron/projects/active/aws-biopharma
npm install
npm run agent:openai
npm run status:brightdata
npm run build:figures
npm run build:release
npm run verify:release
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
- Bright Data: MCP server configured with `@brightdata/mcp@2.6.0`; token
  visibility depends on shell or `.env`. Status check does not spend credits.
- OpenAI: `OPENAI_API_KEY` is present in the current environment; Strands uses
  it through `OpenAIModel`, and only status/output metadata is written.

## Licensing / Redistribution Boundary

- Source code: Apache License 2.0.
- Restrictive boundary: Apache 2.0 does not relicense datasets, provider
  outputs, API responses, credentials, or evidence records.
- Provider outputs from Convoke, Bright Data, Muni, Rowan, OnePot, Boltz, or
  similar services are local-only/redacted until usage and redistribution rights
  are verified.
- Do not commit `.env`, API keys, tokens, restricted records, or copied provider
  output.

## Chain Of Custody

- Public dashboard artifacts are listed with SHA-256 hashes in
  `data/dashboard_snapshot.json`.
- Overnight custody receipt:
  `data/magicstudiobox/runs/primary/merkle_receipt.json`.
- Tamper demonstration:
  `data/magicstudiobox/runs/primary/tamper_test.json`.
- Conversation/agent provenance is represented by handoff/status files and Git
  commits, not by publishing raw private chat text.
- Claim ceiling remains `REPURPOSING_HYPOTHESIS / reproducible evidence
  workflow only`.
- Figure receipt:
  `data/figures/fcg_perturbation_star_chart.receipt.json`.
- Public release signature:
  `custody/release-root.sig`.
- Public verification command:
  `python3 custody/verify-release.py`.
- Ledger hash status:
  `custody/ledger-artifact-status.json`.

## Team Split

- Demo runner: make `npm run serve` dashboard present cleanly.
- Integration owner: complete Convoke login and verify tool visibility.
- Strands owner: confirm MCP docs/tooling path and identify one agent workflow.
- Data/evidence owner: choose the smallest public biopharma evidence slice.
- Pitch owner: keep the claim bounded to a reproducible evidence workflow.

## Tasks That Can Safely Be Cut

- Full KG ingestion.
- Full BioCustody/Bio-Delta-G import.
- Legacy side-project work.
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
