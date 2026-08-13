# Team Update

The active workspace is now:

```text
/Users/byron/projects/active/aws-biopharma
```

Use this for the AWS Biopharma Hack Day workstream. Do not use the old
BioCustody/inbox path as the active repo unless we explicitly import a specific
artifact.

## Current Setup

- Strands SDK installed with `npm install @strands-agents/sdk`.
- Strands MCP configured in `.mcp.json`.
- Convoke Bio MCP configured in `.mcp.json`.
- Convoke sign-in URL:
  `https://platform.convoke.bio/sign-in?redirect_url=https%3A%2F%2Fplatform.convoke.bio%2F`
- Local dashboard:
  `http://127.0.0.1:8765`

## Local Run

```bash
cd /Users/byron/projects/active/aws-biopharma
npm install
npm run pull:data
npm run serve
```

## Licensing / Sharing

- Source code: Apache License 2.0.
- Data, provider outputs, API responses, credentials, and evidence records are
  not relicensed by this repo.
- Do not commit `.env` or tokens.
- Treat Convoke, Bright Data, Muni, Rowan, OnePot, Boltz, and similar provider
  outputs as local-only/redacted until usage rights are verified.

## Immediate Assignments

1. Integration owner: complete Convoke auth and confirm tools are visible.
2. Strands owner: verify the MCP workflow and one agent path.
3. Demo owner: run the local dashboard and make the UI presentable.
4. Data/evidence owner: choose one tiny public evidence slice.
5. Pitch owner: keep claims to reproducible workflow/evidence custody, not
   clinical efficacy.
