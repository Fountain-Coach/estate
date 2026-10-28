# The Composable Book — source-owned stylesheet restored on WLAN staging

**28 October 2026 · private staging only · accepted**

The user reported the Linotype presentation at `http://192.168.8.50:8200/estate/essays/the-composable-book/` as broken. This was reproduced in the actual running `v57` release: the page's local stylesheet `assets/essay.css` returned **HTTP 404 as text/html**, and Chrome refused to apply it because of the MIME mismatch. The original published route at `https://fountain.coach/essays/the-composable-book/assets/essay.css` returned HTTP 200 `text/css`, **7,393 bytes**.

The existing page was otherwise present, with intact article paragraphs and original illustrations; this was a **missing deployment asset**, not a reason to rewrite Linotype, add a new layout engine, or regenerate the essay. The previous estate-wide pass checked HTML and global chrome, but did not verify route-specific CSS. A structural 509-route PASS did not prove that this particular article rendered correctly.

## Smallest owner-authorized correction

Recovered the *byte-identical published stylesheet*, SHA-256:

`05b3915a0f37d5f83df06af31081bfe661c7b792c8a83c2c4f952c7f03b4011c`

into Fountain Coach's current source branch at `site/essays/the-composable-book/assets/essay.css`. **Source commit:** `72c0cc9d3d0353b708c1d1b6329b864f12932d64`. The entire published essay body remains preserved as a production/stage baseline; it is **not** misrepresented as present in the older Git article source snapshot. The source `npm run check` now asserts the exact 7,393-byte original CSS, selectors and 107-file SHA inventory.

The immutable private WLAN candidate was derived from the **actual active v57 release**, not from a stale Git site tree. All 509 HTML files and original media were retained, with exactly one added file (`estate/essays/the-composable-book/assets/essay.css`) and one changed private source-lock metadata file. The publisher's existing staging inspector accepted it. It was atomically activated using the established owner SSH transport, retained rollback, and existing `fountain-shell-acceptance-preview.service`.

Active: `shared-shell-20261028-v58-composable-css-05b3915`.

Rollback: `shared-shell-20261028-v57-author-led-aa38389` (preserved unchanged).

The private v58 artifact has **1,139 files**, **249,551,716 bytes**, **509 HTML routes** and release inventory digest:

`07b1d5fce9bf86ad8e0f31f84e66d392d2502eb4f860b436c5942164b395e358`.

## Independent live verification

- Direct staging readback: article HTML HTTP 200, **29,403 bytes**, identical to v57; stylesheet HTTP 200, `text/css`, **7,393 bytes**, exact published SHA-256.
- **509/509** independent staged HTML route readbacks passed, with original HTML hashes unchanged, including masthead/reel/footer. The legacy `/pointer/` alias remains the intentional Works projection.
- **3/3 targeted live Chrome viewports** passed at widths **390, 820 and 1280 px**, with the correct responsive essay column layout, five original image decodes, usable table-of-contents anchors, no page errors and no missing stylesheet.
- Estate's **`npm run staging:verify`** now additionally checks the exact stylesheet URL's HTTP status, `text/css` MIME, byte count and SHA-256, so another missing CSS cannot hide behind a 509-route HTML success.

## Receipt and ownership

All detailed, full-length route reports and machine-readable evidence are preserved on the owner-controlled Mac mini:

`/home/benedikt/estate-shell-acceptance-staging/receipts/20261028-v58-composable-css/`

The principal receipt is `v58-composable-stage-receipt.json`. Its transferred SHA-256 is:

`44c6abe2e52e67e5a77b39abb2c10148b2e5a660b09d1e75930d71153980cebf`.

The source-only stylesheet revision is in `Fountain-Coach/fountain.coach`'s `editorial/2026-10-28-author-led-estate` branch; the current stage release registry and regression check are owned by `Fountain-Coach/estate`.

**No public production release occurred.** The published CSS was read, not modified. Native iPad Safari acceptance was not claimed; the exercised browsers were headless macOS Chrome at the stated viewports.
