# Public HTTPS to immutable Git recovery reconciliation

**Scope:** bounded nine-host public route census, matched strictly by normalized public URL and byte-identical SHA-256 to a pinned owning commit, archival Git projection, or an owner-domain public HTML recovery snapshot.

**Do not deploy:** this does not prove an exhaustive public route or asset inventory, atomic publication revision, or private/dynamic services. The recovery lock remains BLOCKED.

| Host | Owner release commit | Owner asset | Owner public readback | Historical projection | Unmatched HTTP 200 | Non-200 |
|---|---:|---:|---:|---:|---:|---:|
| benedikt-eickhoff.de | 23 | 0 | 0 | 0 | 0 | 1 |
| book.fountain.coach | 0 | 0 | 2 | 52 | 0 | 0 |
| fountain.coach | 26 | 0 | 0 | 0 | 0 | 14 |
| governance.fountain.coach | 277 | 0 | 0 | 0 | 0 | 0 |
| instruments.fountain.coach | 14 | 0 | 0 | 0 | 0 | 0 |
| midi2.fountain.coach | 0 | 0 | 3 | 34 | 0 | 0 |
| status.fountain.coach | 22 | 0 | 0 | 0 | 0 | 0 |
| teatro.fountain.coach | 5 | 0 | 0 | 0 | 0 | 4 |
| works.benedikt-eickhoff.de | 43 | 2 | 5 | 92 | 0 | 2 |

## Unmatched public resources in this census

- None among probed URLs. This still does not certify full public release coverage.

## Guardrails

- Provenance categories are mutually exclusive for presentation; a URL may have multiple historical Git candidates. Each selected match is digest-verified.
- The historical projection does not gain domain ownership by having byte-identical files.
- All ten previously unmatched public HTML and PDF files are now present in their owning repositories as frozen, explicitly non-deployable readbacks. The two Solstice CSS/JavaScript assets are proven directly from a pinned owning Git commit.
- Public 404 and 401 are reported, not “recovered” by inventing or promoting a staging page.
- Assets not linked or listed in the historical seed may be absent from this census.
- Dynamic runtime data, unpublished content and secrets are outside scope.

Regenerate offline: npm run recovery:coverage:build. Verify unchanged witness: npm run recovery:coverage:verify.
