# Fountain Coach — the three-publication estate

This registry owns public editorial roles and GitHub ownership references, not the content of other repositories or deployment credentials.

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
