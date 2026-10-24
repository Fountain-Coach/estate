# Instruments semantic edition — public release v16 verified

**24 October 2026.** Author explicitly selected **Instruments** during the public-release conversation. Scope: exactly `https://instruments.fountain.coach/` and its own source-backed assets; Book, Works, Status and all other public domains are outside this operation.

## Authorities and predecessor

- Canonical Git author: Fountain-Coach/instruments.fountain.coach, pinned **website source** `5ac718ed67bd9d528a294d3d4e94ef2514efd67e`; subsequently recorded owner release and typed receipts in Git [2026-10-24-semantic-instruments-public-release.md](https://github.com/Fountain-Coach/instruments.fountain.coach/blob/main/docs/releases/2026-10-24-semantic-instruments-public-release.md).
- Canonical previous public release: `releases/estate-20261024-v14-satzfunk-reel-instruments`. Before mutation, public HTTP SHA-256 independently matched this on the homepage, stylesheet and all three historical deep pages.
- Staging source witness: immutable WLAN v21 Instruments edition (standard Lucide microphone, ear, clapperboard icons), retained in combined v26. Its main editorial text matches owner Git source, while publication preserves the already correct production nine-entry common reel and footer.
- Immutable v16 candidate = eleven verified original public-release files (no deletes, only root index and `assets/site.css` changed) plus nineteen Instruments-owned images/styles/scripts and the Lucide ISC license. No copying of Book/Works/Status staging or unpublished records.
- Exact-host publication profile: existing SSH root and original Caddy static release directory; one source SHA, thirty-file complete digest manifest and seven public HTTPS readback witnesses. Native publisher: standalone EstatePublisherSSHDelivery at tested/reviewed source commit `b5e279eaa216859477073bd71263f39dcfd38b27`.

## Correctly observed failure, not invented blocker

The first typed release `estate-20261024-v15-semantic-instruments-5ac718e` briefly activated, verified the new index, and failed its public stylesheet SHA check. The publisher automatically rolled back, retained its failure receipt, and the old symlink and old public HTTPS index/CSS were independently verified restored.

The real source was Caddy's existing `@estateRailInstruments` path matcher. It matched homepage, historical routes and shared-shell fingerprints but failed to match the Instruments-owned `/assets/site.css`, icon and social assets, which fell back to a different reverse-proxy origin. **The only host-config correction** added `/assets/*` to this one host-scoped path matcher; no host root, TLS config or unrelated route changed. See the exact live-host Caddy source diff [2026-10-24-instruments-caddy-assets-route.diff](2026-10-24-instruments-caddy-assets-route.diff). Root Caddyfile backup remains at `/etc/caddy/Caddyfile.before-instruments-assets-20261024`. Original config SHA `8c001a5929cd3f2033b7679cea9ae09c1ac37d1b83318eb9d1bef55ca18d7e1d`; fixed SHA `bc2e60820fe9d77ee875a688e3c7a46a573bd2619be28c2e4db1292f4c5126cc`. `caddy validate` and `systemctl reload caddy` passed; service remained active.

This is a real demonstrated one-line asset routing defect on the existing public host, not a new server, helper, security ceremony or speculative prerequisite. A future Caddyfile regeneration must retain this exact host-scoped matcher change to prevent drift.

## Successful native exact-host public release

After the Caddy correction, the **same preflighted 30-file source candidate** was delivered as a new immutable release `estate-20261024-v16-instruments-assets-5ac718e`, declaring old v14 as predecessor. The typed EstatePublisher public receipt reported `state=active`, with independently verified seven HTTP 200 exact SHA-256 witnesses:

- `/index.html` `68f654280e64b15b0c1c04585b47c05c0b1a067bc95112d55c261786ace18d4d`.
- `/assets/site.css` `bad09263355e590adfe73d975828e3e08a2067cc5a4afa275b19f2c1877145fc`.
- `/assets/instrument-sing.svg` `ad2b3766d5dd8f83f8d8eb0047d81717a3a624195fa2e81ff2e59a68ff064a29`.
- `/assets/instrument-ear.svg` `59987946969574248eb6fe94518ed1555644582c03be7ff3f308c63224c93b31`.
- `/assets/instrument-satzfunk-player.svg` `869662c633d086ebce56a504fb51eae9ab82daff4d6c5e57903e1b6eb1eebf32`.
- `/assets/instruments-triad-social.png` `96868e1c2240a4cfe892f58233f18c22af17375cf8c4a80ad0cc8a85dfb0171e`.
- Preserved `/instruments/codex-auth-instrument/index.html` `56a65da13f63a2c8c568e9d8f9ecfcfe92bafd0f69b02fcfab8018893d1a11a0`.

The exact typed JSON is owned by [Instruments public release receipt](https://github.com/Fountain-Coach/instruments.fountain.coach/blob/main/docs/releases/2026-10-24-instruments-v16-public-receipt.json) with [source inventory manifest](https://github.com/Fountain-Coach/instruments.fountain.coach/blob/main/docs/releases/2026-10-24-instruments-v16-manifest.json); the first rolled-back receipt is retained beside them.

Independently, a new no-cache public HTTPS check confirmed all nine affected/protected items: homepage, CSS, three icons, social PNG and **all three old historical deep pages**, byte-for-byte against the release candidate. Live public production symlink `current` points to `releases/estate-20261024-v16-instruments-assets-5ac718e` with old v14 and inert v15 retained for rollback.

Chromium browser tests against **actual HTTPS production**, at 1280x900 and 393x852 with cache disabled, observed the correct 9-entry reel (Satzfunk yes, Status footer-only), real loading Sing/Ear/SatzfunkPlayer vector images, working historical links, no missing images, no JavaScript errors or horizontal overflow. Native Safari and physical iPad visual acceptance are **not** claimed.

## Non-effects and lingering checks

Combined WLAN staging remained `shared-shell-20261024-v26-discreet-references-876b613`; Book public production remained `releases/estate-20261024-v14-satzfunk-reel-book`, and public Status and Works routes still returned HTTP 200. No sensitive document, Reframe Bookshelf content, unrelated estate artifact or runtime instrument implementation was deployed.

An attempted optional `swift test` suffered concurrent local Swift build object-file races while the same CLI build artifacts were in use; do not claim a fresh successful test-suite run. This did not change the independently successful preflight, native exact-host typed public release and subsequent HTTPS/browser witnesses. This release verifies the static publication, **not** MIDI 2.0 instrument hardware/realtime acceptance.
