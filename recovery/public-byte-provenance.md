# Public-byte provenance: Git historical composition

**Evidence-only: no recovery release admitted and no source ownership reassignment.**

The exact public HTML roots were found in historical Git commits of an archival estate projection. For each file that differs from its root-matched tree, this report searches all commits ancestral to the fixed archival witness commit for the exact public SHA-256. This locates independently recoverable historical blobs **without downloading or committing live content**.

| Public target | Root-tree exact | Exact blob in another historical revision | Public bytes not found in Git search | Archive URL not HTTP 200 |
|---|---:|---:|---:|---:|
| book.fountain.coach/ | 51 | 1 | 2 | 0 |
| midi2.fountain.coach/ | 32 | 1 | 3 | 0 |
| works.benedikt-eickhoff.de/solstice/ | 87 | 5 | 0 | 2 |

**Across this limited archived-file set:** 177 public responses have exact Git blob provenance out of 182 files returning HTTP 200. This is not a denominator for all public site files; unlisted routes/assets remain unknown.

## Files still lacking exact historical Git bytes

### book.fountain.coach/
- `capabilities/csound-auv3-instrument-boundary/index.html` — 482d37b5e9cc21e77684e2f739989f1b0ed0bc10c99c488f5526e9a398f8196a
- `csound-teatro/index.html` — 07b7595c3061ac2e96a0eb27874d524e3e7943519f34f3e86aaf2f4d47d03f38

### midi2.fountain.coach/
- `docs/README.html` — 03a47b4d45cdf00de78c7c36ec3faabc3368b0b77bec51bb3c38afb81395cdfb
- `docs/generated/normative-coverage.html` — 6bf7810f0953a2979b2199f313b298f95021a2981dde4d6206fb64cd52117069
- `docs/spec-compliance-dashboard.html` — 56b9aaef34b006c9140aa4be0e631eac8d8bc897270162bbb566dea6c4471cea

## Not-public or unverified archival URLs

- works.benedikt-eickhoff.de/solstice/assets/solstice-mark.svg: ARCHIVAL_FILE_NOT_PUBLIC_AT_PROBED_URL (HTTP 404)
- works.benedikt-eickhoff.de/solstice/template-contract.json: ARCHIVAL_FILE_NOT_PUBLIC_AT_PROBED_URL (HTTP 404)

## Authority and release gate

- Source owner remains the domain registry owner. Historical projection repository entries are cross-repository **evidence**, not alternate domain owners.
- A mixture of historical Git blobs is **not** a proven atomic published release. Exact blob provenance is necessary but insufficient for a full release manifest.
- The data is based on a bounded earlier live HTTPS observation and on Git commits available from the pinned archival ancestry. The archive must also be proven retrievable from remote GitHub for provider-loss recovery.
- Do not copy unknown public bytes into Git to make an audit pass; first establish source ownership, editorial scope and authority.
- No permission for SSH, Caddy, tunnel, DNS or recovery deployment follows from this audit.

Build/refresh: `npm run recovery:blob-plan`; independently verify: `npm run recovery:blob-verify`.
