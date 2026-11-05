# Fountain Press: semantic two-leaf spread — v151 owner-WLAN staging

**Date:** 5 November 2026. **State:** ACTIVE PRIVATE STAGING. **Public production:** unchanged.

## User outcome and observed defect

The writer supplied an actual large-screen Safari photograph: the illustrated essay `What Makes a Page Modern? / Self Out Loud` displayed a large apparently accidental empty field on one leaf while the subsequent illustration and supporting passage were moved elsewhere. The requested correction is semantic spread composition, not smaller margins or another Reader.

On the accepted predecessor `shared-shell-20261105-v150-fluid-nested-3ba1b0e` the existing `inFlowFigure` routine used a source image's aspect ratio and an up-to-66%-leaf ceiling, then required another 76px/four font sizes of unused prose reserve **on the same leaf**. If the complete image+reserve could not fit, it moved the entire image to the next leaf. Live WebKit geometry at 1440×900 showed the relevant proof passage ending a leaf at approximately 41% fill; placing the original proof illustration at 80% of its preferred size demonstrably fitted the remaining folio with the prior full reserve. The compositor also allowed a subsection heading to be stranded at the foot of a leaf.

## Bounded compositor change

- **Single owner/source:** `Fountain-Coach/fountain.coach`, branch `codex/press-semantic-spread-balance-20261105`, commit `17e32af5b875ec5356ddfa8a9680711d60aaa4eb`; changed only `scenarios/reading-first-20261101/reading-first-press-engine.js` in the deployable Reader assets.
- On facing leaves only, if an inline secondary illustration cannot fit at its preferred size, measure the largest fitting version down to **72%** of its preferred width. Maintain intrinsic aspect ratio, original source identity, original reading order and meaningful scale; fall back to ordinary next-leaf placement if no permissible size fits.
- **Verso/recto semantic field:** a figure on the left leaf may use more of its folio when an authored following paragraph can continue on the visible right leaf. The right leaf retains the original 76px/four-font-size prose reserve. No screenwide image shrinkage or source redistribution.
- An authored subsection heading is kept with a measured readable opening of its following paragraph. If a preceding secondary illustration prevents that, its existing displayed size may be reduced by at most 25%; otherwise the heading moves with its paragraph. This avoids a visually orphaned title without editing prose.
- The existing responsive portrait reader path, manuscripts, original SVGs, media, shell, original frame CSS, and all other assets are unchanged. No second compositor or invented publishing service.

## Exact stage/provenance

- **Predecessor:** `shared-shell-20261105-v150-fluid-nested-3ba1b0e`, retained immutable and rollback ready.
- **Active release:** `shared-shell-20261105-v151-semantic-spread-17e32af`, inherited **1,320** files. Only two bytes-level changes relative to v150:
  - `estate/assets/linotype/reading-first-press-engine.js` SHA-256 `e38301452ef0f07aa9440953d898dcf9ae13fcb828a7d4a97fac163976261d9a`.
  - `source-lock.json` SHA-256 `ad15c096e83c4695c1b0feb1ec85a3f5f354498baf3a3ffc42d05cff1cad97b9`.
- Unchanged Reader root `estate/index.html` SHA-256 `8ca2c693f4ae275f16331f3989790016a7f0ba3d0a2c2dc34d58e3a4f432478f`; unchanged frame CSS SHA-256 `8e175ccbdfdd71e506979772059c72fcfb85de8d3daa366a34544ccc7d4502e6`.
- **Guard owner:** `Fountain-Coach/estate` branch `codex/press-semantic-spread-stage-20261105`; initial code commit `eada2f562f751def2d603fbbe71e029b1fa56cbf`. Installed v151 guard SHA-256 `48e9a777ed876b1fb09d79f4dbd38514a0cd2606f3eae5f2c2ba851999ad0ef4`; exact v150 guard saved as `reader_provenance_gate_v150_backup_20261105.py`, SHA-256 `1c24269dcd8f50b4c7f720ad443a09ce4cd75b6b2c2503f1822169fd2f213c90`.
- The prospective v151 gate admitted the candidate through its original Reader lineage, including all private listening/MP3 assets unchanged, and **refused three forged** lock/commit/compositor-file identities.
- The new guard was installed while v150 was still live. Both the existing HTTP :8200 and HTTPS :8243 services returned the exact **v150** engine hash after guard installation. Then the existing `current` symlink was atomically switched to the immutable v151 release and the **same two** user preview units restarted. Both reported active.
- Independent readback from HTTP and HTTPS returned the expected **v151** engine digest, original root HTML digest and original CSS digest. No public production publication or extra stage host.

## Real browser evidence

- **Candidate:** 14/14 WebKit and Chromium before/after comparisons at 390×844, 820×1120, 1194×834, 1200×860, 1280×720, 1440×900, and 1920×1080. Exact order of source-addressed blocks and **all 12** figure identities preserved. At 390×844 and 820×1120, complete composed page markup and leaf count remain **identical to v150**, not just superficially similar. The affected 1440×900 right leaf changed from approximately **41%** fill to approximately **98%** and now carries the proof illustration with its surrounding argument. A stranded heading on the original large spread is eliminated.
- **Actual activated HTTPS, no candidate asset substitution:** 14/14 WebKit/Chromium profiles passed again with a digest readback of the deployed v151 compositor, compared against the pinned v150 baseline. The same exact compact HTML/source preservation and large-spread geometry results passed. Live WebKit screenshots of the 1440×900 spreads were independently opened and visually inspected.
- **Other-book smoke:** 8/8 live WebKit/Chromium selected routes reopened: `first-readings`, `essays`, `teatro`, and `essay--to-read-is-not-to-remember`. The first two are navigational collections (0 body folios), not full-book visual acceptance.
- **Not proved:** physical iPad Safari, VoiceOver, arbitrary works such as the larger Solstice route, public release, or the still-separate human-voice/MIDI instrument. The private WLAN CA was bypassed in browser automation; this does not certify its device-level trust state.

## Rollback and canonical Reader

To roll back, atomically repoint the existing `/home/benedikt/estate-shell-acceptance-staging/current` symlink to retained `releases/shared-shell-20261105-v150-fluid-nested-3ba1b0e` and restart only existing `fountain-shell-acceptance-preview.service` and `fountain-shell-acceptance-preview-https.service`. The installed guard admits v150, and its exact previous revision remains backed up if needed.

**Owner-WLAN reading route:** `https://192.168.8.50:8243/estate/#/read/essay--what-makes-a-page-modern`

**Final scope:** v151 ACTIVE PRIVATE WLAN STAGING, independently browser-verified. Public production unchanged.
