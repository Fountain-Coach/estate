# Published-release recovery lock: read-only candidate, not admission

This is the first executable slice of [ADR 001](../docs/decisions/001-local-ubuntu-off-provider-tunnel-recovery.md). It is **not** a released static estate, an executable SSH runbook, a DNS switch, or a tunnel configuration.

The generator `scripts/plan-recovery.py` reads:

- `inventory/domain-ownership.json`: every owner repository, Git revision and domain lifecycle
- `inventory/public-readback.json`: the independently measured public HTTP status and content SHA-256; its observation timestamp is pinned in the candidate
- `manifest.json`: the host/delegation registry
- Immutable, committed Git objects in the locally available owner checkouts, authenticated against their actual GitHub `origin` remote

It searches the revision history for the exact Git commit whose public root document matches the previously witnessed *live bytes*, then records that revision, Git tree object, complete tracked source-tree file/blob inventory and route-level sample comparisons. It **never** opens the owner's uncommitted working files, selects the latest Git `main` just because it exists, or rewrites the published estate. Excluded/staging-only 401/404 routes are not interpreted as a demand to invent pages.

The current result contains 12 domain/path surfaces: nine live host roots, the delegated published First Reading under `works.benedikt-eickhoff.de/solstice/`, one planned host and one archived host. Only seven of the ten publication surfaces have a verified exact public-root-document match in their *owning* Git repository. The other three remain blocked.

**The central limit**: a matching homepage is not a complete release witness. Even for the seven candidates, exhaustive comparison of every published route, asset, document, font, media file and any dynamic behavior has **not** been completed. The recovered source-tree Git blob identities prove what Git holds; they cannot establish that all those blobs constitute the last public release. All active surfaces therefore have the explicit `FULL_LAST_PUBLIC_RELEASE_AND_ASSET_PROOF_NOT_ESTABLISHED` blocker. The top-level lock is always `releaseAdmitted=false`, `allowRecoveryDeployment=false`. These cannot be flipped by a successful root comparison.

## Supplemental artifact lead (not an owning release)

A read-only investigation on 2026-10-15 found that `Fountain-Coach/midi2-gpu-fabric`, commit `aba0a0ea941a886642bb4d87df5bfd99f674c6d3`, includes `estate/sites/midi2.fountain.coach/index.html` whose committed Git blob exactly matches the live `https://midi2.fountain.coach/` root at the time of inspection (SHA-256 `c9872ee856d334a94e004abc9f511ac9ceeb0294aa3b57b92e61946d4a91b180`). That is strong evidence of an **archived derived projection**, but the registered owner remains `Fountain-Coach/midi2`. The root artifact has not been proven to be rebuildable from the owner, nor has the entire MIDI2 site been verified. Do not silently substitute this monorepo projection or change source ownership.

The `Fountain-Coach/book-of-reframe` Git history yielded **no byte-identical root** across 16 reviewed committed revisions. The served Solstice First Reading similarly differs from its owning source revision. Both remain explicit blockers until the actual published artifacts and provenance are reconciled.

## Recovery controls

- `npm run recovery:plan`: rebuild the candidate from owner Git objects and frozen public readback. No web mutation.
- `npm run recovery:verify`: deterministically regenerate in memory and fail on stale/tampered candidate or invalid fail-closed contract.
- `npm run check`: also enforce the existing estate-domain route inventory contract.

A new independent HTTPS observation should first be captured with `npm run inventory:probe`, then the source inventory and recovery candidate regenerated, reviewed and committed as one coherent evidence revision. The recovery lock is time-bounded evidence, **not** an ever-current claim about a remote server.

## Required next evidence

The next engineering slice must find exact committed or otherwise independently backed artifacts for Book of Reframe, MIDI2, and the delegated Solstice First Reading; enumerate all live public routes and required assets; verify every artifact against a committed Git owner and independently signed/approved release receipt; then produce a complete authorized release lock. No Caddy recovery promotion, SSH mutation, or temporary public tunnel is justified while the lock remains blocked.

All DNS, existing WLAN staging, Hetzner and current public HTTPS remain unchanged by this planner.

## Historical Git publication-artifact search (15 October 2026)

The read-only archival audit has now identified exact public root bytes for Book of Reframe and MIDI2 at `Fountain-Coach/midi2-gpu-fabric` commit `e23618e1f5e0f7102faaf7b980a854c2a295f2e2` and for the delegated Solstice First Reading at commit `5e9d6b0ba5746abceed41ffefbf69dc5a7d26066`. These commits, and the pinned archival audit commit `aba0a0ea941a886642bb4d87df5bfd99f674c6d3`, were individually confirmed accessible via authenticated GitHub API on 2026-10-15. That proves these Git history candidates are not confined to the development Mac; it does not confer release authority.

The full per-file read-only GET audit is recorded in [historical-projection-audit.md](historical-projection-audit.md) and the finer [root-matched-historical-artifacts.md](root-matched-historical-artifacts.md). An exhaustive check **of the Git-tracked files in those three selected archival trees** found 170 byte-identical public responses, 12 divergent responses and two 404s, out of 184 source files. Searching the pinned historical ancestry for individual changed file blobs recovered another seven exact public-byte matches. [Public-byte provenance](public-byte-provenance.md) records all 177 matches and the five unresolved publicly served documents. These numbers do not establish that 184 files constitute the entire published estate or even the complete route/asset inventory of those three surfaces.

The five unresolved public documents are the Book of Reframe's Csound AUv3 instrument and Csound Teatro pages plus MIDI2's `docs/README.html`, `docs/generated/normative-coverage.html`, and `docs/spec-compliance-dashboard.html`. The two archival 404s on Solstice do not necessarily represent lost published content; their URLs may be deliberately unserved.

**Owner invariant:** `Fountain-Coach/book-of-reframe`, `Fountain-Coach/midi2`, and `Fountain-Coach/solstice.fountain.coach` remain the source owners. `Fountain-Coach/midi2-gpu-fabric` is a historical projection/evidence repository, not a new publication authority or a reason to merge/rewrite canonical source trees. Full recovery remains BLOCKED until an approved complete static-release lock and public-route/asset census are proven, and private/dynamic state is separately recoverable.
