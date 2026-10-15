# Public-root-matched historical estate artifacts

**Archival Git evidence; canonical ownership and publication authorization unchanged.**

Each selected archival revision contains one byte-identical *published root document*, compared against the independent public-readback witness. All Git-tracked files at the selected revision were then compared individually against current public HTTPS. This still does not prove that Git contains *every* public route or asset.

| Published surface | Matching archive revision | Committed files | Exact | Different | HTTP missing | Other errors |
|---|---|---:|---:|---:|---:|---:|
| book.fountain.coach/ | `e23618e1f5e0` | 54 | 51 | 3 | 0 | 0 |
| midi2.fountain.coach/ | `e23618e1f5e0` | 36 | 32 | 4 | 0 | 0 |
| works.benedikt-eickhoff.de/solstice/ | `5e9d6b0ba574` | 94 | 87 | 5 | 2 | 0 |

## Independent authority boundary

- The archival repository is Fountain-Coach/midi2-gpu-fabric, not the listed publication owner for the Book of Reframe, MIDI2, or the delegated Solstice. This audit **does not** transfer ownership.
- A root-matching archival tree is not a complete public release receipt; individual mismatches and absent files are retained.
- The published Solstice URL is on works.benedikt-eickhoff.de/solstice/, while its canonical source owner is Fountain-Coach/solstice.fountain.coach.
- Never replace present public sites with these Git trees until complete route/asset admission and domain-owner authorization.

## Remaining divergences

### book.fountain.coach/

- DIFFERENT: `assets/estate-core.js` (HTTP 200)
- DIFFERENT: `capabilities/csound-auv3-instrument-boundary/index.html` (HTTP 200)
- DIFFERENT: `csound-teatro/index.html` (HTTP 200)

### midi2.fountain.coach/

- DIFFERENT: `assets/estate-core.js` (HTTP 200)
- DIFFERENT: `docs/README.html` (HTTP 200)
- DIFFERENT: `docs/generated/normative-coverage.html` (HTTP 200)
- DIFFERENT: `docs/spec-compliance-dashboard.html` (HTTP 200)

### works.benedikt-eickhoff.de/solstice/

- DIFFERENT: `assets/book.css` (HTTP 200)
- DIFFERENT: `assets/book.js` (HTTP 200)
- DIFFERENT: `assets/linotype-engine.js` (HTTP 200)
- NOT_HTTP_200: `assets/solstice-mark.svg` (HTTP 404)
- DIFFERENT: `editions/first-reading/proof/index.html` (HTTP 200)
- DIFFERENT: `editions/first-reading/proof/proof-manifest.json` (HTTP 200)
- NOT_HTTP_200: `template-contract.json` (HTTP 404)

## Controls

Probe: `npm run recovery:matched-probe` (read-only GETs and Git committed objects). Verify recorded evidence: `npm run recovery:matched-verify`.
No DNS, SSH, Caddy configuration, public routing, credentials or deployment are changed.
