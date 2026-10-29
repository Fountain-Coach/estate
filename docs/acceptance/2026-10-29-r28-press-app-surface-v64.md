# R28 v64 — Fountain Press app-first Bookshelf, owner-WLAN stage

**Date:** 29 October 2026  
**Scope:** A visible design correction to the existing private-WLAN Reframe Reader/Bookshelf; **not a new book admission, native iPad Safari acceptance, public two-domain release or new publishing platform**.  
**Author's criterion:** First contact must feel like **an app, not a normal website**. No text appears outside the authentic rounded-square publication covers; the open hand stays the root action.

## Exact source and stage

| Field | Independently observed |
| --- | --- |
| Source compositor | `Fountain-Coach/fountain-press/runtime/bookshelf.py`, app-surface mode commit `ea0b2d4ab20096a30143e318bc2a43c3bd359fbc` |
| Source stylesheet | `Fountain-Coach/fountain-press/runtime/bookshelf.css`, with app surface and focus-reveal reference accessibility at `05d1bfcc2c3f287f2c343fbf2f0cfae2dfdd30c2`, SHA-256 `abf39bf95ff3057bd627fe5427131235964bf17896f02ae166cb36f7c17539fd` |
| Press verification tests | `Fountain-Coach/fountain-press/tests/test_bookshelf_collection_identity.py`, 14/14 relevant tests passed in the isolated source-owner runtime |
| Future source-owned publication assembly | `Fountain-Coach/fountain.coach/scripts/build_edition_hierarchy.py` `59bdad5a56954d3829b4e4c2588d80a74fdfd5ca` and corresponding changed test `6d6e9223b8f245cf6a500d4fd7f2f3a8103ae3fa` (full site owner build/test **not** claimed) |
| Stage-only projection tool | `Fountain-Coach/estate/staging/r28_immersive_bookshelf.py`, commit `ef6e1933ebf91963872525e06eb067c55690dcae`; a deterministic transform of existing Press-constructed static documents, **not** a replacement runtime compositor |
| Canonical existing WLAN host | `http://192.168.8.50:8200/estate/` via `MacMiniDocker`, existing `fountain-shell-acceptance-preview.service` |
| Current immutable release | `shared-shell-20261029-v64-reframe-app-ef6e193` |
| Retained immediate rollback | `shared-shell-20261029-v63-reframe-hand-29fb917` |
| Serving witness | Current symlink to v64, existing service restarted and active, root HTTP 200; all affected deep routes independently returned HTTP 200 |

The v64 builder refused any alternate current symlink, checked exact v63 input SHA-256s and the owner Press CSS digest, copied v63 to a **new nonactive immutable release**, and replaced only `estate/index.html`, the byte-identical `estate/editions/index.html`, `estate/collections/first-readings/index.html`, `estate/assets/linotype/bookshelf.css` plus its appended source-lock record. `diff -qr` confirmed this exact bounded set; 20 inert vacancies, the two original main-cover images, one nested First Readings work, unchanged original manuscript/media, existing book.js/book.css and all remaining source routes are preserved.

### Byte witness

| Changed output | Staged SHA-256 |
| --- | --- |
| Bookshelf root, also `/estate/editions/` | `c9d8fb59fcd4fc9079124bc2a04c9b58b6c5a5d4cda534b173be3b0a535f386d` |
| First Readings collection | `dc0540087350f1a26b58519b2bcbaa176d553b037268482f2796396fb4a3df84` |
| Fountain Press Bookshelf CSS | `abf39bf95ff3057bd627fe5427131235964bf17896f02ae166cb36f7c17539fd` |
| Continuing Essays original source-bound reader | **Unchanged:** `c24303fbe864f48c88c144c06f085f713208475728f8b39512fb1541221b506b` |

The actual source-owned Press `.bookshelf-paper` and `.shelf-cover` are retained, not replaced by a new grid. `app-surface` CSS removes extra page spacing; the original circular hand is the universal root control, the two genuine covers retain their original images/text **inside their rounded squares**, and the twenty empty rounded squares remain inert.

## Real browser witness — one continuous app page

Actual Chrome DevTools Protocol (CDP) navigation and browser screenshots on the Mac over the WLAN staging route:

- Profiles: **1024×768 iPad landscape**, **768×1024 iPad portrait**, **390×844 phone**, **1440×900 desktop** (browser-emulated device metrics; **not** physical iPad/Safari).
- In **all eight profile × route cases** (root Bookshelf and nested First Readings): actual `body.app-surface`, actual Press paper grid, correct **2/1 real covers**, **20 source-inert vacancies**, original art loaded, no horizontal document overflow, exactly one hidden but AX-exposed book/collection heading, no website masthead, explanatory title band, navigation bar or legacy nine-site shell. All individual visible cover labels have bounding boxes **inside** their rounded cover frames. Press Grid has **4 columns** at iPad/desktop and **2 columns** at phone widths.
- The first content row begins at about **31 px** on iPad landscape, **23 px** on iPad portrait, and **16 px** on phone; no previous giant headings, paragraphs or navigation strip pushes the source-covered books down the page.
- On all four root profiles, clicking the existing Essays cover opens `/estate/editions/essays-continuing/` and its source-born hand returns to the **same** `/estate/` root. Home hand remains a genuine large reachable button on both kinds of shelf.
- Browser and AX headings remain named `Bookshelf` / `First Readings` in one-pixel clipped `h1.press-visually-hidden` nodes. The root's original publisher/rights/references footer still exists as a semantic, keyboard-accessible resource but occupies **one clipped pixel** by default, not visible website furniture. An additional actual-browser keyboard-focus check confirmed the seven legal/reference links become visible in a compact panel **only when one receives focus**, then return to invisible state when focus leaves (`width 1 → 1000 → 1`, CSS `clip-path inset(50%) → none → inset(50%)`).
- R28 CDP visual DOM/AX checks: **8/8 passed, exit code 0**. Browser screenshots for iPad landscape, portrait and nested shelf were independently visually reviewed against the author's screenshot. The fullscreen warm neutral background, hand, genuine cover tiles, empty slots and no surrounding text were observed.

The CSS and semantic role support reading without inventing a PWA/offline service, fake native app or custom mobile domain. Browser toolbars may still be visible in Safari; a standalone installed web app is **not** implied by this visual correction.

## Scope boundaries

The **public** `https://fountain.coach/` and `https://benedikt-eickhoff.de/` have **not** been changed or published. The previous immutable v63 stage is retained for rollback. Physical iPad Safari and VoiceOver acceptance, complete Reader-wide accessibility certification, actual two-public-domain alias/redirect behavior, complete Governance/Works book admission and paid Writer capability remain **open**. The original texts, book editions, scores and media were not modified to achieve the visual change.

**Result:** the author can now inspect the requested app-first Press Bookshelf on the same canonical owner-WLAN address, without the former website-like textual superstructure.
