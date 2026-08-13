# BioCustody Ledger Import Requirements

The teammate BioCustody/FTO ledger is not considered incorporated until each
file is imported as a content-addressed FCO leaf and included in the signed
release root.

## Expected File Set

Import the package under:

```text
biocustody-ledger/
```

Required science lane:

- `biocustody-ledger/README.md`
- `biocustody-ledger/fcg.py`
- `biocustody-ledger/ingest.py`
- `biocustody-ledger/origin_digests.json`
- `biocustody-ledger/tamper_test.py`
- `biocustody-ledger/index.json`
- `biocustody-ledger/merkle_receipt.json`
- `biocustody-ledger/tamper_test.json`

Required FTO lane:

- `biocustody-ledger/FTO_DESIGN.md`
- `biocustody-ledger/fto.py`
- `biocustody-ledger/ingest_fto.py`
- `biocustody-ledger/registry_digests.json`

## Hashing Rule

Every imported file must have:

- exact byte SHA-256;
- canonical FCO record in `custody/fco/`;
- FCG parent closure;
- inclusion in `custody/release-manifest.json`;
- inclusion in `custody/release-root.txt`;
- coverage by `custody/release-root.sig`.

## Verification

Run:

```bash
npm run build:release
npm run verify:release
```

The verifier checks that any present `biocustody-ledger/` required file has both
a SHA-256 status entry and an FCO in the release manifest. Missing files remain
`pending_import` until the teammate package is copied in.
