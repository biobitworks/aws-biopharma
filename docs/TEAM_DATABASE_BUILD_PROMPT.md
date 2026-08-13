# Team Database Build Prompt

Build a small public, rights-aware evidence database for the AWS Biopharma demo.

## Scope

Use only public or explicitly permitted sources. Keep the first slice small:

- candidate profile / perturbation record;
- target or mechanism record;
- pathway or biological-process label;
- clinical-progress record when public;
- source license / usage-rights record;
- FCO provenance record for each source.

## Required Fields

```text
record_id
record_type
source
source_record_id
source_url
source_version_or_retrieved_at
payload_sha256
license_or_terms
usage_rights_verified
contains_phi
access_restricted
claim_ceiling
parents
```

## Exclusions

Do not add PHI, restricted sponsor data, unchecked provider output, credentials,
or free-text claims without a source record.

## Output

Produce normalized JSON/CSV plus FCO leaves that can be included in a signed
release manifest.
