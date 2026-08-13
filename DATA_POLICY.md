# Data Policy

## Admission Rule

Allowed:

- public open datasets;
- synthetic data generated in this repository;
- provider outputs only when local use and redistribution rights are verified;
- de-identified sample data explicitly permitted for public hackathon use.

Rejected by default:

- PHI or private patient records;
- confidential sponsor or employer material;
- restricted-access research datasets;
- local clinical records;
- proprietary datasets whose use rights have not been checked;
- secrets, API keys, access tokens, credentials.

## Required Metadata

Each imported source or provider result should record:

```json
{
  "public_data": true,
  "contains_phi": false,
  "access_restricted": false,
  "usage_rights_verified": true,
  "source": "...",
  "source_record_id": "...",
  "dataset_version": "...",
  "license_or_terms": "...",
  "retrieved_at": "...",
  "payload_sha256": "..."
}
```

## Provider Outputs

Convoke, Bright Data, Muni, Rowan, OnePot, Boltz, and similar outputs are not
automatically public artifacts. They may be used locally only if provider terms
permit the use. Do not publish raw provider output unless redistribution rights
are explicit.

## Claim Boundary

This demo may claim a reproducible evidence workflow and bounded candidate
ranking. It must not claim therapeutic efficacy, clinical utility, diagnosis,
treatment recommendation, measured rescue, or biological rejuvenation.
