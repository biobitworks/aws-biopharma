# Remediate Prompt

Apply only fixes supported by the red-team and research findings.

Required fixes:

- Add an OpenAI-only red-team fanout script.
- Run multiple available OpenAI model reviewers when available.
- Persist model IDs, reviewer IDs, blockers, findings, and API/model errors.
- Mirror the red-team receipt into `public/data/`.
- Add a dashboard panel that renders the red-team status.
- Include the red-team receipt in deterministic dashboard snapshot and release
  custody inputs.
- Update teammate-facing docs with exact run/verify commands.

Hard rails:

- Preserve row-level and provider restrictions.
- Do not commit `.env` or secrets.
- Do not perform live provider/KG writeback.
- Do not claim therapeutic, clinical, diagnostic, or efficacy outcomes.
- Do not mark optional provider auth as PASS; use `not_configured`.
- Rebuild and verify release custody before final push.
