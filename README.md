# Fountain Coach — the three-publication estate

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
