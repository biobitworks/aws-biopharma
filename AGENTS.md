# Agent Operating Rules

This folder is the active AWS Biopharma Hack Day workspace:

```text
/Users/byron/projects/active/aws-biopharma
```

Do not use the older BioCustody, StateShift, or inbox package as the active work
surface unless a task explicitly asks to import a specific artifact.

## Priority

Build the smallest complete AWS Biopharma demo around a public-data,
evidence-bounded workflow:

```text
public source data -> traceable processing -> candidate/evidence ranking ->
provenance/custody -> simple dashboard/demo
```

Current scaffold:

- Strands Agents SDK and MCP setup.
- Convoke Bio MCP endpoint configured, auth required.
- Static local dashboard in `public/`.
- Local snapshots in `data/` and `public/data/`.

## Boundaries

- No PHI, patient records, restricted sponsor material, confidential data, or
  unchecked provider output in source control.
- No secrets in files, logs, snapshots, dashboards, FCO payloads, or slides.
- Do not claim therapeutic efficacy, clinical utility, diagnosis, rescue,
  rejuvenation, or treatment recommendation from this demo.
- Apache 2.0 applies to source code only. Data, provider outputs, API responses,
  and evidence records remain governed by their original source terms.
- Convoke, Bright Data, OpenAI, AWS, and other external providers are optional
  unless their credentials and usage rights are verified.

## Sharing

Share this folder/repo for code and demo review. Redact provider outputs and
credentials unless redistribution rights are explicit.
