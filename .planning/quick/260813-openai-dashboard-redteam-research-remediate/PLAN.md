# OpenAI Dashboard Red-Team / Research / Remediate Plan

## Target Artifact / Ask

Make the AWS Biopharma static dashboard viable for teammate review using an
OpenAI-only red-team fanout and committed custody/provenance artifacts.

## Owning Repo

`/Users/byron/projects/active/aws-biopharma`

## Evidence Class

- public dashboard status
- local integration status
- release custody receipt
- reproducible figure receipt
- OpenAI red-team receipt

## Claim Ceiling

Reproducible evidence workflow and repurposing hypothesis only. No therapeutic,
clinical, diagnostic, treatment, efficacy, or biological rescue claim.

## Restricted-Data Risk

Do not commit `.env`, API keys, bearer tokens, raw private chat, restricted
provider output, or unverified third-party data exports.

## Destination / Writeback Risk

GitHub push is allowed for source, redacted status, public data snapshots, and
custody receipts. No live AWS, Convoke, Bright Data, KG, or provider writeback.

## Required Skill Chain

1. `gsigmad-redteam-research-remediate`
2. OpenAI API fanout with local `.env` / shell secret loading
3. deterministic dashboard snapshot rebuild
4. deterministic release custody rebuild and verification
5. Git commit/push per stage

## Expected Outputs

- red-team prompt package in this directory
- `data/openai_redteam_status.json`
- `public/data/openai_redteam_status.json`
- dashboard panel for OpenAI red-team status
- regenerated `data/dashboard_snapshot.json`
- regenerated custody/FCO release artifacts
- GitHub push for each stage

## Stop Boundaries

- Stop on secret leakage.
- Stop on dashboard-render blocker.
- Stop on claim-ceiling violation.
- Stop on release custody verification failure.
- Do not launch AWS resources or paid provider workflows.
- Do not perform KG/provider writeback.
