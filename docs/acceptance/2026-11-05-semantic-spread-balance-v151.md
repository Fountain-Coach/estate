# Fountain Press v151 — semantic balance in the measured two-leaf spread

**Date:** 5 November 2026. **Scope:** original `What Makes a Page Modern? — Self Out Loud` essay on the existing private owner-WLAN Fountain Press Reader. **Release status:** ACTIVE PRIVATE STAGING, not public production.

## Observable defect and decision

The author photographed a wide-screen spread in which the second leaf became a largely unoccupied container, weakening the relation between an illustrated proof and its explanatory prose. A reproduction on **live v150 WebKit at 1440×900** showed the affected recto `008` at approximately **41% vertical content occupancy**, with the next proof figure delayed to folio `009`.

Source inspection of the actual Press `reading-first-press-engine.js` identified the defect: `inFlowFigure` selected a preferred intrinsic-aspect-ratio secondary image size, but if the full image + four-line (minimum 76px) *same-leaf* prose reserve did not fit, it moved the image in its entirety to the next leaf. The existing compositor also allowed a subsection title to remain alone at a leaf foot. The previous v150 source-reconstruction/overflow tests did not assert spread-level semantic attachment.

**Approved correction:** the two leaves together are one visible field, **without inventing a new spread renderer**. Retain the same original Press paginator and source-addressed writer manuscript. When an authored paragraph follows a secondary illustration on a left/verso leaf, its prose may begin on the right/recto of that SAME spread, so the image needs only its measured bottom inset on the left. Right leaves and single-page views retain the original four-line reserve. If an image still does not fit at preferred width, search for the **largest fitting natural-aspect scale** down to 72% of its selected width; below that, prefer the existing next-leaf behavior, not a thumbnail. Bind a subsection heading to a measurable readable beginning of its next paragraph. If an already placed secondary image prevents that binding, shrink that image by at most 25% before moving the heading. No source paragraph is redistributed or silently revised.

The edition and its principal illustration rules, Book shell, pages, source addresses, color/typographic stylesheet, private listening assets and other author content remain intact. White space is permitted where source structure requires it; no artificial text fill or arbitrary equal-height columns.

## Exact owner, ancestry, and immutable file delta

- **Source:** `Fountain-Coach/fountain.coach`, branch `codex/press-semantic-spread-balance-20261105`, implementation commit **`17e32af5b875ec5356ddfa8a9680711d60aaa4eb`**.
- **Guard owner:** `Fountain-Coach/estate`, branch `codex/press-semantic-spread-stage-20261105`, guard implementation commit **`eada2f562f751def2d603fbbe71e029b1fa56cbf`**.
- **Exact active release:** `shared-shell-20261105-v151-semantic-spread-17e32af`; directly copied from previously admitted immutable `shared-shell-20261105-v150-fluid-nested-3ba1b0e` (retained unchanged for rollback).
- **Inventory:** 1,320 files in both releases; only **two** file digests differ. `estate/assets/linotype/reading-first-press-engine.js` is **`e38301452ef0f07aa9440953d898dcf9ae13fcb828a7d4a97fac163976261d9a`**; `source-lock.json` is **`ad15c096e83c4695c1b0feb1ec85a3f5f354498baf3a3ffc42d05cff1cad97b9`**.
- **Preserved:** original Reader root `estate/index.html` SHA-256 `8ca2c693f4ae275f16331f3989790016a7f0ba3d0a2c2dc34d58e3a4f432478f`; existing `reading-first-press-frame.css` SHA-256 `8e175ccbdfdd71e506979772059c72fcfb85de8d3daa366a34544ccc7d4502e6`; original 12 essay figure identities and all private Vergil/Qwen auditions.
- **Stage guard:** installed SHA-256 `48e9a777ed876b1fb09d79f4dbd38514a0cd2606f3eae5f2c2ba851999ad0ef4`. The exact prior v150 guard is backed up at `reader_provenance_gate_v150_backup_20261105.py`, SHA-256 `1c24269dcd8f50b4c7f720ad443a09ce4cd75b6b2c2503f1822169fd2f213c90`.

## Independent evidence — preflight, negative, activation, actual live

1. **Scoped candidate QA:** 14/14 WebKit/Chromium source-and-layout comparison profiles at `390×844`, `820×1120`, `1194×834`, `1200×860`, `1280×720`, `1440×900`, `1920×1080`. Every original source-block sequence and 12 illustration identities matched v150. No browser page errors or horizontal overflow. The `390×844` and `820×1120` single-page layouts had **identical generated page HTML** to the v150 Reader, not just similar screenshots.
2. **Photographed large-screen case:** at `1440×900`, recto folio `008` went from approximately **41%** to **98%** content occupancy while remaining within the measured type area. The authentic proof illustration and next section now enter the same spread. The following `009–010` spread contains the actual web-reader illustration and source-address explanation, with approximate 98% / 92% occupancy. No orphaned section headings at this profile. Book folios recomposed from 26 to 23; original content and figures unchanged.
3. **Unrelated route check:** 8/8 selected Chromium/WebKit route openings passed for First Readings collection, Essays collection, Teatro and `To Read Is Not to Remember` at 1440×900. These checks prove opening/geometry only, not whole-book semantic acceptance.
4. **Fail-closed provenance:** read-only `verify_semantic_spread_stage_gate_v151.py` accepted the **actual 1,320-file candidate** through the whole production-derived v140→v150 chain, the unchanged Reader shell/assets, private audition page and MP3s. Independently refused forged source-lock digest, forged source Git commit, and forged engine digest.
5. **Safe activation:** installed the amended existing provenance guard while v150 was still active, restarted only the two existing preview user services, and verified **the exact old v150 engine bytes** over HTTP `:8200` and HTTPS `:8243`. Switched the already-existing `current` symlink atomically to v151 and restarted those same services. Independently read back exact v151 engine over both protocols and verified root/CSS original digests; services were active.
6. **Actual running HTTPS, no asset substitution:** the 14/14 WebKit/Chromium profile comparison was repeated on the **activated site**, with the v150 baseline injected only for *before* comparison; the *after* run fetched the unmodified actual v151 JS from HTTPS and verified its SHA-256 before traversal. Source order, image IDs, mobile markup identity, spread recto occupancy and no orphan headings all passed. Independent WebKit screenshots of actual live spreads `007–008` and `009–010` were inspected. The 8/8 other-book opening checks also passed on the **actual unmodified v151 site**.

## Limits and recovery

These are strong source/remote-browser witnesses, not physical iPad Safari, native VoiceOver, physical external-monitor Safari pixel proof, or publication to public DNS. Browser automation explicitly bypassed the private owner-WLAN CA trust warning; the host certificate was not modified. Source implementation is on the `fountain.coach` branch, **not an implied merge into `Fountain-Coach/fountain-press` main**. The larger `Solstice` route was not part of this bounded regression. No self-voice recording, MIDI 2.0 control stream, public estate media or production release was implemented.

**Rollback:** atomically repoint `/home/benedikt/estate-shell-acceptance-staging/current` to `releases/shared-shell-20261105-v150-fluid-nested-3ba1b0e`, then restart `fountain-shell-acceptance-preview.service` and `fountain-shell-acceptance-preview-https.service`. The installed v151 guard continues to admit v150; its exact backup is retained separately.

**Existing private WLAN Reader:** `https://192.168.8.50:8243/estate/#/read/essay--what-makes-a-page-modern`

**Result:** STAGED / BROWSER-VERIFIED / ROLLBACK-PRESERVED. Public production unchanged.
