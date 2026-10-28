# Author-led estate: private WLAN release v57

**Released 28 October 2026, WLAN staging only.** The active immutable release on `benedikt-Macmini` is `shared-shell-20261028-v57-author-led-aa38389`, available at `http://192.168.8.50:8200/estate/`. This is not a production publication.

The author-approved editorial decision is reflected across the stage: the parent Fountain Coach homepage names the one-person practice and selects four original illustrated essays; `/estate/essays/` remains the complete seven-work reading room; `/estate/editions/` contains the source-owned, independent Fountain Press catalogue. Works is the primary personal editorial entrance. The personal pointer remains a pointer rather than a duplicate top-level reel identity.

## Source and stage authority

- Fountain Coach author source commit: `aa38389ba2ef9070d91a36c169e74902ed3b096b` on `editorial/2026-10-28-author-led-estate`; owner test `npm run check` passed.
- Estate registration baseline: `81cdf15ee26e37fd8d0008ab624e41f3e966c421` on the companion estate editorial branch.
- The staging publisher composed the edit over the *actual* pre-existing private v56 release, preserving newer public essays, recordings, Works, governance, historical archive and Teatro material. It did **not** overwrite the stage from the older Fountain Coach Git snapshot.
- Predecessor, retained unchanged for rollback: `shared-shell-20261028-v56-modell-wirklichkeit-e3753d7`.
- Owner-approved WLAN transport: existing `MacMiniDocker` SSH and rsync, verified remote immutable release inventory, atomic `current` symlink change, restart of existing `fountain-shell-acceptance-preview.service`, independent client readback. No new publisher/daemon, DNS, Caddy or public production mutation.

## Release inventory and exact provenance

The transferred release has **1,138 files, 249,543,543 bytes and 509 HTML routes**, verified file by file on Ubuntu. Canonical SHA-256 digest of the sorted path/hash inventory:

`d08e41aa9b21332efb2aa01f8c95f869f7763551c8a6c2a78cb82b36e2c3ab6e`

The independently fetched `/estate/` HTML has SHA-256:

`542def51c68988cc77cb1e7279b7e6172dbcf85fb357498a7d48ae37767daf8e`

It equals both the staged file and local release inventory witness. The running service was confirmed active with `current` targeting v57; v56 remains in `releases/`.

## Acceptance

- **509/509 independently served HTTP routes passed** exact content SHA-256, HTTP 200, one canonical masthead, ordered nine-entry reel, Info action, one shared footer, Status/legal/provenance. The `/pointer/` legacy alias intentionally serves the identical `/works/` projection and is independently verified against the Works SHA rather than a stale pointer root body.
- **509/509 structural HTML source checks passed**, with exactly one retained common footer variant and all original article/reader bodies preserved.
- **30/30 live Chrome checks passed** across 15 representative routes and 390 px / 820 px viewports, with no horizontal overflow or missing assets in those samples; Teatro First Hearing and Solstice First Reading retained their controls.
- The Fountain Coach canonical author-source tests passed: seven source-gallery works; three complete original Linotype essays with 77 original source paragraphs and their original figures, 106-file SHA inventory, reading-continuity PDF and Ear/Sing source assets.
- This is **not** evidence of native iPad Safari acceptance or secure-origin Csound AudioWorklet acceptance. HTTP alone does not create an AudioWorklet-capable secure context; those are separate capabilities and were not silently certified.

## Every staging route, machine-readable receipt, and rollback

The **complete 509-route table** is recorded on the owner-controlled Mac mini rather than exposed as a public Git catalogue of internal/historical stage routes:

`/home/benedikt/estate-shell-acceptance-staging/receipts/20261028-v57-author-led/wlan-http-509.md`

Its matching JSON is `wlan-http-509.json`. The same directory holds `wlan-v57-activation-receipt.json`, `release-inventory.json`, `release-inventory.sha256`, `browser-checks.json`, and the source-structural route ledger. The typed receipt's SHA-256 was independently verified across the author Mac and Ubuntu:

`f83589c029e1be03e55af30d89b3b8e5c5c18de3034701bdca7371784f3335d5`

The route JSON's independently matched SHA-256 is:

`9b175787ef741214843483496a6df12fcdea8ab882ca8a8b946103d12b15a3f5`

The previously published [325 Git-tracked source routes](2026-10-28-editorial-route-register.md) are a **different source inventory** from the 509 routes present in the private WLAN v57 release. Source and compiled-stage counts must not be conflated.

Rollback identity is the retained `v56` directory. If rollback is required, use the same owner-controlled atomic symlink and `systemctl --user restart fountain-shell-acceptance-preview.service`, then independently reread `/estate/` and compare to the pinned v56 root. No rollback was executed; v57 passed the stated staging acceptance.

## Distinguish stage from publication

This v57 release has **no public deployment receipt**. No changes were made to `fountain.coach` or other production HTTPS domains. A public release would need a separate source-owner reconciliation and native EstatePublisher permission, evidence and readback.

## Repeatable current-stage check

The former staging verification script targeted retired 8180–8182 preview ports and asserted the superseded Bookshelf-at-root model. It is preserved as `scripts/verify-wlan-staging-legacy-8180.py`. The current `npm run staging:verify` reads the actual `MacMiniDocker` `current` symlink, the private manifest and the adopted Works/Satzfunk reel, and independently re-fetches all 509 HTTP routes. This new source command passed **509/509** on 28 October 2026 without requiring write access.

The full general-purpose `npm run check` still requires all adjacent owner Git checkouts at the configured development root. It was not a pass in the isolated temporary checkout; the concrete failure was a missing local owner repository (`git remote get-url origin`), not a v57 HTML or WLAN defect. The focused `node scripts/verify-estate.mjs`, `npm run staging:verify`, the Fountain Coach `npm run check`, and the deployed 509-route readback all passed.
