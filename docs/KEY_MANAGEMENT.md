# Key Management

## Public Release

The public repository may contain:

```text
custody/public-key.pem
custody/release-manifest.json
custody/release-root.txt
custody/release-root.sig
scripts/verify_release.py
```

## Local Only

The private signing key must stay outside GitHub:

```text
.custody-private/signing-key.pem
```

The `.gitignore` blocks `.custody-private/`, `*.private.pem`, `*.key`,
`secrets/`, and `.env`.

## Signature Scope

The release signature covers the release Merkle root, not each file
independently:

```text
artifact -> canonical FCO leaf -> FCO id -> Merkle release root -> private-key signature
```

This preserves FCO recursion while giving reviewers one public verification
target.

## Current Implementation

`scripts/build_release.py` creates a local RSA signing key if one does not
exist, writes the public key to `custody/public-key.pem`, signs
`custody/release-root.txt`, and writes `custody/release-root.sig`.

`scripts/verify_release.py` verifies hashes, parent closure, Merkle root, release
signature, claim ceilings, rights-source provenance, and private-key leak
patterns.
