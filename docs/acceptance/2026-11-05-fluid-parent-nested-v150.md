# Fountain Press v150 — Fluid parent folio and nested typesetting
5 November 2026 · private owner-WLAN staging

## Reported failure and source diagnosis

The writer rejected the v149 “stage within a stage”: it still had an apparently fixed width, additional nested margins and unnatural transitions into/out of the surrounding Reader text. This was a **real compositor defect** rather than a missing specimen border.

Two exact source defects were read in `Fountain-Coach/fountain.coach` `scenarios/reading-first-20261101/reading-first-press-engine.js`: the screen-frame `geometry()` forced `Math.min(...,700)` on every single-folio Reader width, and `inFlowSpecimen()` tried the complete setting, then allocated a new folio before testing whether a readable prefix could fit the *existing remaining page*. The nested specimen's CSS inset was also a fixed em measure rather than a proportion of its parent type field.

An independent live v149 WebKit width series observed 740/820/900/1024/1200-pixel portrait viewports all retaining exactly 700px outer leaf, 624px type area and 568px nested text width. At 390×844 the first classical specimen occupied 555 of 645px vertical type area on a newly empty leaf. Prior v149 acceptance tested text preservation and bounding-box containment but **did not establish parent geometry elasticity or use of remaining page space**. The old claim of fully fluid composition is therefore withdrawn.

## Corrective source owner and bounded delta

- **Source:** `Fountain-Coach/fountain.coach`, commit `3ba1b0e826efcec947e243100c2925ad78d2953e`, branch `codex/linotype-fluid-nested-flow-20261105`.
- Changed ONLY `scenarios/reading-first-20261101/reading-first-press-engine.js` and `scenarios/reading-first-20261101/reading-first-press-frame.css`, plus source `PLANS.md` and focused tests. Original combined essay manuscript, the single authoritative specimen source, original illustration SVGs, Reader app/shell, private recording media, and all other book source files remain unchanged.
- The existing screen-frame compositor now derives each folio width from the **available Reader field**. On landscape, two complete book leaves continue to share the available field. No new Reader, template runtime or public route.
- The existing `inFlowSpecimen` now attempts a measured source prefix in *remaining folio space*, preserving a readable minimum of approximately two lines. It only starts a new folio when the remaining space cannot hold that beginning. Source-addressed continuation still reconstructs the exact passage.
- The outer page stegs use a proportional, uncapped ~7.5% inset; inner specimen stegs respond to the available type area (CSS proportional clamp). Historical figure assets continue through the unchanged image path.

## Immutable staging lineage and admission

- Exact predecessor: `shared-shell-20261105-v149-nested-specimen-ce0c1cd`. The v149 root HTML is SHA-256 `8ca2c693f4ae275f16331f3989790016a7f0ba3d0a2c2dc34d58e3a4f432478f`.
- New active private stage: `shared-shell-20261105-v150-fluid-nested-3ba1b0e`. The 1320-file stage copy changes exactly three files from v149:
  - `estate/assets/linotype/reading-first-press-engine.js` → SHA-256 `52f30f9fd36f3f1ccb24bd833b14f91289d270df394f8418a77cc672ee7c5342`;
  - `estate/assets/linotype/reading-first-press-frame.css` → SHA-256 `8e175ccbdfdd71e506979772059c72fcfb85de8d3daa366a34544ccc7d4502e6`;
  - `source-lock.json` → SHA-256 `f10275f49d5da6837d6572b6508bb51b9752a4a25ffcb08ed4f9835fa986eee0`.
- `estate/index.html` remains byte-for-byte identical. All previous accepted stage recordings, model derivatives, figure assets and Reader navigation assets remain present and unchanged.
- **Guard owner:** `Fountain-Coach/estate` branch `codex/linotype-fluid-nested-stage-20261105`, commit `c3caa8a77b16e11107d9f5bcb4a1f42f67841ed8`. An additive exception to the existing fail-closed `reader_provenance_gate.py`, never a replacement server/reader. Installed guard SHA-256 `1c24269dcd8f50b4c7f720ad443a09ce4cd75b6b2c2503f1822169fd2f213c90`; v149 guard retained as backup `12296b76f086a0b247b9bde3f2e772b92c636ee6c545018997ade00390c5f13d`.
- The independent candidate guard accepted the original production-derived v140→v150 lineage, the two revised Press assets, unchanged original Reader app, essay figures and two private Vergil/Qwen audition MP3s. It **refused four deliberately forged identities** (lock, commit and each asset digest).
- Current v149 served HTML SHA-256 was verified unchanged on HTTP :8200 and HTTPS :8243 under the new gate *before* activation. The existing `current` symlink was then atomically changed to v150, and only the same two existing preview services restarted.

## Actual acceptance

- **Pre-activation candidate:** 18/18 independent Chromium/WebKit profiles across 390×844, 600×950, 740×1050, 820×1120, 900×1280, 1024×1366, 1200×1500, 1200×860, 1440×900. All 12 figure identities reached, neither specimen displayed as an image, text source reconstructed exactly, no overflow or Reader JS failures. The single-folio area width increases as the viewport grows, unlike v149. Example WebKit measured type widths: 312px at 390px viewport, 670px at 820px, 844px at 1024px, 992px at 1200px. The nested type measure increased in step.
- **Pagination continuation:** independently tested WebKit and Chromium at 390×690. The classical specimen **begins after its actual introductory prose** on leaf 5 and carries characters 0–241; leaf 6 continues exactly 241–444. No clipping or source-character loss. This is the minimal repro of the previous all-or-nothing folio defect.
- **Enlarged type:** four tests at 34px forced typography in both browsers passed. At 390×844 the essay comprised 125 physical leaves and retained all source; at 820×1120 it comprised 43 leaves. Both authentic specimens kept continuous source offsets.
- **Unrelated routes:** First Readings and Essays collections, Teatro and the different essay `To Read Is Not to Remember` reopened in both Chrome and WebKit (8/8). A previously timed-out larger Solstice route is not claimed.
- **Live stage:** HTTP and HTTPS services independently served the exact unchanged root HTML SHA `8ca2c693...`, and HTTPS readback independently served the **new** engine SHA `52f30f9...` and CSS SHA `8e175ccb...`. Existing services both active. Actual live Chromium/WebKit page checks performed with no local asset substitution.
- **Boundaries:** Automated browser contexts bypass owner-WLAN self-signed certificate trust errors. This is *not* native physical iPad Safari or VoiceOver acceptance. No new human-voice recording/MIDI instrument or public release.

## Rollback

The immutable original v149 release remains available at `releases/shared-shell-20261105-v149-nested-specimen-ce0c1cd`. Restore the `current` symlink atomically to that directory and restart the *same two* user-level preview services; the extended guard still admits the unchanged v149 release. The precise guard backup is `reader_provenance_gate_v149_backup_20261105.py`. No public production release occurred.

**Canonical private WLAN reading route:** `https://192.168.8.50:8243/estate/#/read/essay--what-makes-a-page-modern`.
