# IP-Aware FCG

The public release treats licensing and intellectual-property evidence as
first-class custody leaves rather than informal notes.

## Separation Of Evidence

Scientific evidence and rights evidence are separate routes:

```text
candidate artifact
  |-- SCIENTIFIC_EVIDENCE
  |     |-- morphology / perturbation result
  |     |-- target or mechanism evidence
  |     `-- clinical-progress source rows
  |
  `-- RIGHTS_EVIDENCE
        |-- source-data license or terms
        |-- provider-output terms
        |-- patent / ownership signal when available
        |-- regulatory exclusivity signal when available
        `-- FTO status when reviewed
```

## FCO Requirement

Every public rights assertion should be backed by a source FCO with:

- source name and record identifier;
- source URL or local path when public;
- retrieval date or source version;
- payload hash;
- claim ceiling;
- disclosure route.

## Current Hack Boundary

This repository records source-code licensing, public-data boundaries, provider
boundaries, and claim ceilings. It does not provide freedom-to-operate,
patentability, ownership, regulatory exclusivity, or legal advice.
