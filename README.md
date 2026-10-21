# Fountain Coach — the three-publication estate

## Owned audio archive — decision 2026-10-21

[Cross-estate owned audio boundary](docs/decisions/2026-10-21-owned-audio-archive-estate-boundary.md): independently verified 33 Bandcamp public playback MP4 files on Ubuntu; separate original-master and rights verification required. Artist Works catalogue owns work identity, Satzfunk owns hearing/performances, Store/EstatePublisher owns any public release. No new front door, deployed station, DNS, Caddy modification or storage bill.


This registry owns public editorial roles and GitHub ownership references, not the content of other repositories or deployment credentials.

## Current milestone: Teatro / Linotype v16 beta acknowledged

**On 14 October 2026 the author expressly recognized the current
Teatro book-first reader/listening experience as “a great beta state”.**
This is an accepted *beta UX reference*, not full Reframe acceptance or
permission to publish the Teatro domain. The canonical author decision
and frozen revision evidence are documented in
[Reframe — Teatro Linotype beta v16](https://github.com/Fountain-Coach/Reframe/blob/main/docs/milestones/2026-10-14-teatro-linotype-beta-v16.md).

The benchmark implementation is owned by Teatro `69656eb` and Fountain
Press `45e28c7`, staged as Ubuntu WLAN release
`20261014-teatro-r16-play-ring-calibrated-v16` on port 8182. The estate
manifest records a separate `betaMilestone` with explicit false
values for **public HTTPS publication**, **full Reframe writer
acceptance**, **native MIDI2 host transport** and **trusted iPad Csound
acceptance**. Earlier sections below describe the development path;
their outdated Hear/rail candidate wording is historical, **not**
the current v16 interface.

## Exactly three front doors

1. Fountain Coach: https://fountain.coach/ — editorial identity and publisher.
2. First Reading: https://works.benedikt-eickhoff.de/solstice/editions/first-reading/ — authored Linotype book. The source owner is Fountain-Coach/solstice.fountain.coach (private) and the renderer is Fountain-Coach/fountain-press. The future solstice.fountain.coach hostname is not currently DNS-resolved.
3. Teatro: https://teatro.fountain.coach/ — performance, sound and executable score.

## Supporting domains, references, archives

Governance owns the complete normative reference. MIDI2 is technical documentation and evidence. Instruments is a catalogue. Status is mandatory footer/legal transparency. The Book of Reframe recedes to an online historical reference and is not an admitted Linotype book. The founder pointer remains adjacent. Tennis has been archived privately in GitHub.

See manifest.json for each domain's actual GitHub source owner and its admission status.

## Publishing ownership

GitHub becomes the canonical home of content and estate composition. The old Hetzner Git remote is deprecated only after Git history and package consumers are reconciled. Hetzner Caddy can continue hosting HTTPS. Source commit, exact-site materialization, typed EstatePublisher release and public readback are separate operations.

Run npm run check for the machine-readable role and ownership contract. No GitHub Actions/CI, Git submodules, fictional books, automatic DNS mutation or force pushes.


## Editions hierarchy (October 2026, staging admitted)

The domain `fountain.coach/` now **lands in the editions catalogue**
(mirrored at `/editions/`). It no longer drops a reader straight onto the
Essays cover. The Fountain Coach estate rail points directly to its
**`/editions/essays/`** volume, while First Reading and Teatro point into
their independently owned edition surfaces.

The Essays volume has three complete nested sub-editions, each with a stable
`/editions/essays/<source-slug>/` address, its own cover, contents, and
independent Linotype reading position. The original complete authorial pages
in `/essays/` remain source material, byte-for-byte intact. This is a
published-hierarchy **candidate**, not an automatic claim of production HTTPS.

Current source: `Fountain-Coach/fountain.coach` at `e8d34eb`.
Current accepted WLAN release: `20261014-editions-hierarchy-three-front-v3` on
`192.168.8.249:8180`; First Reading remains on 8181, Teatro on 8182.
Run `npm run staging:verify` for real stage routes, nested readers, estate
rail and legal footer checks; the Git-owning source additionally runs
actual simulated browser tests for each sub-edition.


## Teatro First Hearing — book first, Stage as a sub-edition

The Teatro estate rail and the canonical Teatro homepage now land in the
complete source-bound Linotype manuscript **Teatro — An Unfinished
Composition**. Its source prose and single original score plate are pinned
to the separately owned Fountain Coach essay. Teatro's book and runtime
are owned by Fountain-Coach/teatro.fountain.coach at 564be196; the actual
stage remains accessible at /editions/stage/.

The first Satzfunk integration appears here as a **Hear** action inside
the real book. Its source-admitted module is Fountain-Coach/Satzfunk at
fad7009. Without an author-reviewed exact-source recording, it explicitly
reports that no narrated edition is released. The original browser-Csound
Stage remains interactive on demand but cannot be mislabeled as a narrated
book or native MIDI2 execution.

The accepted Ubuntu WLAN stage is
http://192.168.8.249:8182/ with a second stable book path at
http://192.168.8.249:8182/editions/first-hearing/ and original Stage at
http://192.168.8.249:8182/editions/stage/.
The source-lock and HTTPS publishing gates remain separate: Git push
and WLAN proof are **not** a public production release.

Teatro root edition latest source owner: Fountain-Coach/teatro.fountain.coach at 205a7c8; active Ubuntu WLAN release v5. The Teatro editions catalogue legal footer now groups Company Status with legal notices.

Teatro WebGL book-page source: Fountain-Coach/teatro.fountain.coach at 7063ae3, verified WLAN release v6. Original compiled scene is embedded as a measured interactive Linotype plate with lifecycle release on page turn; Csound remains user-activated.

Teatro Reframe R12 Slice A, source owner 17c76b1, is the verified WLAN v7 candidate. The scene is now source-pinned inside the essay, composed by Fountain Press 7f8411e; this is an unaccepted author UX trial, not a public production release.

Teatro R12 v8 is the GitHub-owned WLAN candidate: e7b1d70, original WebGL stage preserved, canonical moving puppet fallback source midi2-gpu-fabric branch codex/teatro-r12-moving-puppet-fallback-20261014 commit 30565d1. Author iPad acceptance pending.

## R17 — Linotype Bookshelf is now the Teatro landing candidate

The Teatro WLAN domain root `/` and `/editions/` use the
reusable **Fountain Press Bookshelf state**, not a direct full-book
page or a separate brochure. The single real book,
*Teatro — An Unfinished Composition*, has both a small paper
thumbnail and a large cover containing its original source-authorized
Teatro Memory Vector plate. A touch/click enters the preserved,
author-acknowledged v16 book at `/editions/first-hearing/`.
The original Stage is secondary, **not** another book.

Source owners: Press `6131c16`, Teatro `d415c39`,
Reframe R17 `900ad35`. Active Ubuntu WLAN v17 is
`20261014-teatro-r17-bookshelf-landing-v17` on port 8182;
the v16 beta remains independently pinned and available
for rollback. Estate's Teatro landing path and edition entry now
address `/editions/`, while `firstHearing.readerPath`
preserves the actual author-approved book. Other estate/front-door
rails still linking directly to the book are **not** claimed
to have been republished.

Five live responsive browser profiles, original book/source SHA
and unchanged reader controls were verified. The bookshelf is a
new author-approval candidate, and public HTTPS remains
unpublished. See
[Reframe scenario R17](https://github.com/Fountain-Coach/Reframe/blob/main/scenarios/017-linotype-bookshelf-landing.md).

## R18 — full source-admitted proofreading shelf, not a public claim

The Teatro WLAN root is now a **six-edition proofreading shelf**,
not the earlier one-book R17 placeholder. The author requested all
currently available books for comparative proofreading and explicitly
rejected the tilted/off-axis thumbnail. Each edition now displays
one upright cover made from its original source-authorized art.

Inventory: public First Reading (30 works), Teatro First Hearing
(the preserved v16 interactive book), the complete Fountain Coach
Essays collection, and its three separately addressable essay
sub-editions. These are **six edition objects, not six unrelated
literary manuscripts**. First Reading is the only edition among
these found reachable at its public URL on 14 October 2026;
the other five are staging proofs, not silently launched public
books. The Governance normative domain and Teatro Stage remain
separate resources rather than fake book catalogue entries.

Fountain Press `d85e49f`, Teatro `3113d46`, Reframe R18
`0c390ce`; Ubuntu WLAN staging release
`20261014-teatro-r18-six-book-proofreading-v18`.
The read-only estate verifier checks 6 covers and the real exact
reader routes. The disposable WLAN preparation projects five
cross-domain bookshelf links to existing stage ports 8180/8181,
retaining the internal Teatro route on port 8182. Git-owned
source metadata remains canonical HTTPS, with original image
SHA receipts preserved. No public HTTPS publication, native
MIDI2, approved narration or full Reframe writer release was
performed. The author's accepted v16 *book* stays intact; the
new cover arrangement awaits their assessment.

## R19 — correction: covers-only Bookshelf table

After reviewing the R18 six-edition shelf, the author rejected
the *additional links and labels underneath each cover*. The
Teatro landing is now a **compact 3×2 cover-thumbnail grid** on
iPad and **two columns on phone**, with no duplicate captions,
source tags or read links. Every cover is the single direct
link to its actual edition. All six original book identities,
source-authorized artwork, exact staging/owner destinations and
separate publication states remain in typed release metadata,
not visually repeated below book covers.

Fountain Press source `29fb26d`, Teatro `16df41c`, Reframe
`scenarios/019-cover-only-bookshelf-table.md`. Ubuntu WLAN
`20261014-teatro-r19-cover-grid-v19` replaces v18, which remains
available for rollback. The author's accepted v16 First Hearing
reader is untouched; public HTTPS remains unchanged.

## R20 — agreed three main editions, logo-only landing

The author corrected the earlier six-essay proofreading shelf:
the top-level editions are **Fountain Coach, First Reading and
Teatro**. The Linotype landing has one original open hand and
spring mark matching the online fountain.coach PNG SHA-256
`8c5fad1c3db56138d5959da75991dc8034a0be537ce46da6ffcc0d9655e7f729`.
No visible titles, counters, numbers, folio labels, duplicated
brand copy, website rail or footer remain. Three original-art
images function as the only edition links. Fountain Coach's
individual essays are nested *within* its collected Essays book,
not incorrectly promoted to parent editions. Likewise First
Reading retains its chapters and Teatro its separate Stage.

Active Ubuntu WLAN is `20261014-teatro-r20-three-editions-logo-v20`;
Teatro source `ff0d6f4`, Fountain Press `2caacf1`, Reframe
scenario R20. Existing 8180/8181 reader routes and the approved
v16 Teatro book on 8182 are preserved. The R17–R19 layouts are
historical candidates; none changes the established three-edition
estate taxonomy. No public HTTPS mutation was requested or made.

## Estate thumbnails (15 October 2026)

The estate owner Fountain-Coach/fountain.coach projects `/` and `/editions/`
as an Instruments-inspired *edition* grid: the verified Fountain Coach
open-hand logo plus exactly three source-backed cover images (Essays,
First Reading, Teatro). This adapts grid rhythm, not iOS application icons or
MIDI2 instrument identities. Its previous detailed, text-rich catalogue is
retained at `/editions/catalogue/`, with all the original complete authorial
essays and reader routes unchanged. The estate staging projection rewrites
only the three verified book destinations to WLAN ports, never content.

The owner repository builds the grid deterministically; source commits and
WLAN tests do not constitute production publication.

## Complete estate inventory and HTTPS reconciliation

The canonical source-owner inventory is in [inventory/](inventory/README.md).
Its [contract](inventory/CONTRACT.md) separates the complete registered domain
estate from the editorial Bookshelf, maps delegated Solstice hosting beneath
works.benedikt-eickhoff.de, and records every Git-tracked HTML source route and
navigation dependency. The current-public-versus-Git evidence is stored in
[inventory/public-readback.json](inventory/public-readback.json). It is a
bounded read-only public HTTPS witness, not a release command or a claim of
complete remote crawl coverage.

- `npm run inventory:build` regenerates deterministic owner, routes, and link graph files.
- `npm run inventory:verify` checks them without modification.
- `npm run inventory:probe` refreshes independently read public HTTPS samples.
- `npm run check` enforces the owner graph and anti-omission contract.

No hosting, Caddy, DNS, GitHub CI or public content is modified by inventory commands.

## Disaster recovery: local Ubuntu as an independent recovery origin

[ADR 001 — Local Ubuntu emergency origin through an outbound tunnel](docs/decisions/001-local-ubuntu-off-provider-tunnel-recovery.md) records the Hetzner provider-loss rationale. The first planned test reconstructs exact published GitHub source on the existing WLAN Ubuntu machine, runs isolated Caddy and exposes it via a temporary outbound tunnel. Permanent DNS and named tunnel routing are later, owner-authorized decisions.

The ADR is an architectural decision only. No live DNS, Cloudflare configuration, current Caddy site, SSH credentials or published material are changed by this record. See [the complete estate inventory](inventory/CONTRACT.md) for the source ownership and public-versus-Git discrepancies that recovery must resolve.

## Candidate published-release recovery lock

[Recovery contract](recovery/CONTRACT.md) and the [generated candidate](recovery/README.md) implement the read-only first step after ADR 001: match observed public HTML to immutable owning Git history, pin historical candidate revisions and their tracked source trees, and record missing release/asset proof as blockers. Use `npm run recovery:plan` to rebuild and `npm run recovery:verify` to check. This is **not** an admitted release; no SSH, tunnel, DNS, Caddy or publication mutation follows automatically. The live historical estate, not the newer Bookshelf, is the comparison baseline.

## Archival artifact provenance in GitHub

The recovery audit now records [historical Git projection comparisons](recovery/root-matched-historical-artifacts.md) and [individual public-byte provenance](recovery/public-byte-provenance.md). It found matching published roots for Book of Reframe, MIDI2 and delegated Solstice in older GitHub commits of `midi2-gpu-fabric`, then located byte-identical Git blobs for 177 of 182 publicly responding files in that limited archival inventory. Five publicly served files remain unmatched, and no complete route/asset release approval exists; this does not change canonical domain owners or permit deployment.

## Cold-recovery progress: complete observed public-byte evidence

The [bounded public estate census](recovery/public-route-census.md) lists 621 checked URLs across all nine currently active public hosts; 600 returned HTTP 200. The [source-to-public byte ledger](recovery/public-git-coverage.md) proves SHA-256-matching Git artifact custody for all 600 observed successful responses (410 pinned historical owner-tree files, 178 archived Git-projection files, 10 published recovery snapshots in canonical owners, and two directly pinned Solstice assets). This does **not** prove every unlinked asset, dynamic service or an authorized full release is restorable; recovery stays BLOCKED until the remaining acceptance requirements are met. The normal source inventory and publication ownership remain unchanged.

## Existing Ubuntu recovery host: read-only preflight

The [Ubuntu recovery-origin preflight](recovery/ubuntu-origin-preflight-20261015.txt) establishes that the WLAN machine is reachable and has Git/Docker, but currently lacks Caddy and cloudflared and cannot retrieve the private historical Git projection. Its default GitHub URL lookup is redirected toward a legacy Git host; an isolated Git configuration successfully reaches public GitHub. No installed service, credentials, DNS or live site was changed. The next phase must make the static release independently retrievable from GitHub and test an isolated Caddy origin before starting a tunnel.

## Reproducible public static cold-restore artifact

The [candidate bundle contract](recovery/bundles/CONTRACT.md) and [complete file-level manifest](recovery/bundles/estate-public-observed-20261015.manifest.json) describe a SHA-256-verified, immutable archive of the nine-domain observed public estate. The archive is intentionally delivered as a separate GitHub Release asset rather than embedding ~80 MB of public binary content in Git history. This is a recovery candidate, not authority to publish, change DNS, or modify existing Ubuntu services.

## Ubuntu cold restore now verified (2026-10-15)

The [Ubuntu static recovery receipt](recovery/ubuntu-cold-restore-witness-20261015.md) records direct GitHub download of the frozen recovery candidate, SHA-256 verification of 599 static files representing all 600 independently observed successful public URLs across nine domains, loopback-only Caddy serving with **600/600 byte-matching responses**, unknown-host rejection, and a working temporary Cloudflare Quick Tunnel for the Fountain Coach homepage. This is a bounded **static rehearsal, not an admitted public release or canonical DNS failover**. Full estate completeness, dynamic private state, multi-domain external routing and independent cellular-browser acceptance remain open.

## Proven local Ubuntu cold-restore rehearsal

On 15 October 2026 the existing Ubuntu Mac mini independently downloaded the immutable public GitHub release, verified its archive and all 600 public SHA-256 resources, and served them unchanged through a separate loopback-only Caddy container across all nine original HTTP Host names. A temporary one-host Cloudflare Quick Tunnel was verified against the exact published Fountain Coach homepage SHA. See the [full recovery witness](recovery/ubuntu-cold-restore-witness-20261015.md) for acceptance results, image digests, limitations, temporary URL and specific container-only shutdown instructions. This proves the bounded observed static surface only; it does **not** authorize production DNS failover or replace the blocked complete-release admission.

## Canonical-domain recovery: DNS and dynamic-service boundaries

[ADR 002](docs/decisions/002-canonical-domain-provider-loss-failover.md) governs the transition **after** the proven GitHub-to-Ubuntu static restore. The [read-only provider-loss gate](recovery/failover-readiness.md) records public authoritative DNS dependencies for both registered zones, mail preservation requirements, existing host routing, release/owner-trust blockers and a deliberately negative total-Hetzner-loss simulation. [Browser/runtime indicators](recovery/runtime-boundary-witness.md) are inferred from frozen published assets but are not tests of functioning external APIs, MIDI, audio, login or FountainStore.

Run `npm run recovery:failover:probe` only to refresh public DNS observations; `npm run recovery:failover:verify` and `npm run recovery:runtime:verify` validate the pinned evidence offline. Production DNS, registrar delegation, named tunnel, live Caddy and secrets are unchanged. A healthy static restore must not be mistaken for canonical-domain failover readiness.

## Owner continuity and Golden Key recovery programme

[ADR 003](docs/decisions/003-owner-continuity-golden-key-recovery.md) pins the private-state, authority and succession recovery programme following the successful GitHub-to-Ubuntu static restore. The [Recovery State Manifest](recovery/state/state-manifest.json), [state contract](recovery/state/CONTRACT.md) and [six-gate readiness report](recovery/state/README.md) classify 16 state classes and deliberately refuse to claim private backup or lost-root recovery without independent evidence. The first implementation slice has 18 offline positive/negative synthetic tests, wired into `npm run check`. No Store secrets, private data, production host credentials, unapproved backups or Cloudflare management are part of this slice.

## Stage 2 recovery: source capability audit versus live instance evidence

The [Stage 2 operational discovery report](recovery/state/OPERATIONAL-DISCOVERY.md) verifies two pinned FountainStore source interfaces, documents seven candidate operating-state classes, and enforces **zero accepted live-instance/private-backup claims** until an enrolled native, owner-authorized read-only adapter issues an independently verifiable redacted receipt. The Store's local backup API writes under the Store's own data directory, so its existence is not proof of off-host recovery. A new 21-test synthetic refusal suite is part of `npm run check`. No privileged service inspection, SecretStore credential read, private data export, or production mutation was conducted.
