# Research Prompt

Research the smallest source-backed path to make the AWS Biopharma dashboard
shareable for teammate review.

Read:

- `README.md`
- `HACKDAY_STATUS.md`
- `TEAM_UPDATE.md`
- `DATA_POLICY.md`
- `CHAIN_OF_CUSTODY_DESIGN.md`
- `package.json`
- `scripts/pull_data.py`
- `scripts/build_release.py`
- `scripts/verify_release.py`
- `public/index.html`
- `public/app.js`
- `public/styles.css`
- `data/dashboard_snapshot.json`
- `custody/release-manifest.json`

Ask:

- What schemas or contracts apply to dashboard status and custody?
- Which status files are canonical local inputs?
- Which hashes, Merkle roots, release signatures, and receipts already exist?
- What identifiers or public/private boundaries need reconciliation?
- What is the minimum implementation path to add OpenAI red-team evidence
  without adding a new source of truth?

Hard rails:

- Cite local files or mark findings unresolved.
- Do not browse or call non-OpenAI providers.
- Do not convert missing provider auth into a dashboard blocker unless the UI
  falsely claims it is configured.
