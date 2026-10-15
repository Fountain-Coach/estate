# Candidate release lock — cold restore, evidence only

**Blocked:** this is a read-only reconstruction plan, not a complete last-public release or authority to start a tunnel.

Recorded public HTTPS witness: 2026-10-15T13:14:11+00:00

| Public host / path | Source owner | Exact live-document Git revision | Sampled routes | Recovery status |
|---|---|---|---|---|
| benedikt-eickhoff.de/ | Fountain-Coach/benedikt-eickhoff.de | fa3d1b406d11 | 4/4 | BLOCKED |
| book.fountain.coach/ | Fountain-Coach/book-of-reframe | not found | — | BLOCKED |
| fountain.coach/ | Fountain-Coach/fountain.coach | 420be0ca655d | 2/2 | BLOCKED |
| governance.fountain.coach/ | Fountain-Coach/governance.fountain.coach | 9f48476835a9 | 4/4 | BLOCKED |
| instruments.fountain.coach/ | Fountain-Coach/instruments.fountain.coach | 34f75755f1d7 | 4/4 | BLOCKED |
| midi2.fountain.coach/ | Fountain-Coach/midi2 | not found | — | BLOCKED |
| solstice.fountain.coach | Fountain-Coach/solstice.fountain.coach | not found | — | NOT_PUBLIC_RECOVERY_TARGET |
| status.fountain.coach/ | Fountain-Coach/status.fountain.coach | 941cd20b2b7c | 4/4 | BLOCKED |
| teatro.fountain.coach/ | Fountain-Coach/teatro.fountain.coach | 609122db395f | 1/1 | BLOCKED |
| tennis.fountain.coach | Fountain-Coach/tennis.fountain.coach | not found | — | NOT_PUBLIC_RECOVERY_TARGET |
| works.benedikt-eickhoff.de/ | Fountain-Coach/works-benedikt-eickhoff | 6b4721db185a | 3/3 | BLOCKED |
| works.benedikt-eickhoff.de/solstice/ | Fountain-Coach/solstice.fountain.coach | not found | — | BLOCKED |

## Cross-repository historical byte provenance

177 archival public file responses have exact Git blob provenance (170 in their matching historical root trees; 7 in other historical commits). 5 publicly responding files remain unmatched; 2 archival files returned HTTP 404.

See [public-byte-provenance.md](public-byte-provenance.md) and [root-matched-historical-artifacts.md](root-matched-historical-artifacts.md). This is evidence from midi2-gpu-fabric, **not** a change to domain source ownership or an approved static recovery release.

## Findings and next steps

Only Git objects of pinned candidate commits are inspected, never uncommitted working-tree files.
A match is per public HTML document. Some hosts also have sampled route matches; none has an independently certified complete public static asset manifest.
The candidate lock lists Git blobs/tree objects for reconstruction but does not claim these are all the bytes presently published.
A 404 or 401 for a staging-only route does not imply the public historic release should contain it.
The MIDI2 owning repository has no verified static publication root; a separate historical estate projection may contain an exact homepage copy, but that projection is **not yet** an approved Git-owned recovery input.
The Solstice First Reading is delegated under works.benedikt-eickhoff.de/solstice/ and must have an independent content/source match.
Before any deployment, prove every required public route/asset, identify remaining web or dynamic state, authorize a full last-published lock, and verify the existing Ubuntu host is isolated.

## Blocking conditions

- benedikt-eickhoff.de/: FULL_LAST_PUBLIC_RELEASE_AND_ASSET_PROOF_NOT_ESTABLISHED
- book.fountain.coach/: NO_EXACT_GIT_COMMIT_MATCHING_LIVE_DOCUMENT
- book.fountain.coach/: FULL_LAST_PUBLIC_RELEASE_AND_ASSET_PROOF_NOT_ESTABLISHED
- fountain.coach/: FULL_LAST_PUBLIC_RELEASE_AND_ASSET_PROOF_NOT_ESTABLISHED
- governance.fountain.coach/: FULL_LAST_PUBLIC_RELEASE_AND_ASSET_PROOF_NOT_ESTABLISHED
- instruments.fountain.coach/: FULL_LAST_PUBLIC_RELEASE_AND_ASSET_PROOF_NOT_ESTABLISHED
- midi2.fountain.coach/: MISSING_GIT_TRACKED_DEPLOYMENT_ROOT
- midi2.fountain.coach/: FULL_LAST_PUBLIC_RELEASE_AND_ASSET_PROOF_NOT_ESTABLISHED
- status.fountain.coach/: FULL_LAST_PUBLIC_RELEASE_AND_ASSET_PROOF_NOT_ESTABLISHED
- teatro.fountain.coach/: FULL_LAST_PUBLIC_RELEASE_AND_ASSET_PROOF_NOT_ESTABLISHED
- works.benedikt-eickhoff.de/: FULL_LAST_PUBLIC_RELEASE_AND_ASSET_PROOF_NOT_ESTABLISHED
- works.benedikt-eickhoff.de/solstice/: NO_EXACT_GIT_COMMIT_MATCHING_LIVE_DOCUMENT
- works.benedikt-eickhoff.de/solstice/: FULL_LAST_PUBLIC_RELEASE_AND_ASSET_PROOF_NOT_ESTABLISHED

## Reproducibility

Run: npm run recovery:plan, then npm run recovery:verify.
No SSH, DNS mutation, Caddy reload, tunnel, secrets, public deployment or Git owner modifications.
