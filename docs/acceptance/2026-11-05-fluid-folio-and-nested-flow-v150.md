# Fountain Press — fluid folio and nested typographic flow (v150)

**Date:** 5 November 2026  
**Authority:** writer-selected original Fountain Press Reader on private owner-WLAN staging; public production not changed.

## Observed failure

The deployed v149 nested specimens were semantically real text but were visually constrained by a hard **700 CSS pixel upper width** in `geometry()` of the existing `reading-first-press-engine.js`. Actual live WebKit 740–1200px portrait viewports returned a constant 700px outer folio, 624px parent measure and 568px inner specimen measure. Separately, `inFlowSpecimen()` attempted the entire specimen block and, if it did not fit, immediately moved it to a fresh leaf before attempting any source-addressed fragment. The old tests verified containment, not elastic page geometry and ordinary prose/specimen cohabitation.

## Smallest source-owned correction

- **Source:** `Fountain-Coach/fountain.coach` branch `codex/linotype-fluid-nested-flow-20261105`, commit `3ba1b0e826efcec947e243100c2925ad78d2953e`.
- **Measured parent:** existing `pageFrame` geometry now uses the whole Reader viewport width to compose one complete portrait leaf, or two complete landscape leaves, with **no hard 700px minimum/maximum intrusion**. Horizontal outer page stegs track 7.5% of physical leaf width with a 16px floor, not the previous 38px ceiling. Typography is recomposed rather than visually scaled.
- **Nested type:** real `inFlowSpecimen` source fragment compositor uses `fits(leaf.area)` against the *currently available* folio first. When the full specimen does not fit, it admits a measured source-character prefix after prose if at least approximately two readable lines can fit; only then continues into another authentic folio. Exact source addresses are preserved and the final captions stay at the final segment. The visual inner inset follows the available column by fluid CSS `clamp` rules.
- **Unaffected:** canonical v149 essay HTML, authored passage and all 12 figure identities, historical SVGs, original Reading app, other collections, private Vergil/Qwen auditions, all non-target asset inventory.

## Immutable release and fail-closed staging

- **Previous immutable active release, retained for rollback:** `shared-shell-20261105-v149-nested-specimen-ce0c1cd`.
- **New immutable stage:** `shared-shell-20261105-v150-fluid-nested-3ba1b0e`.
- **Only changed bytes:** `estate/assets/linotype/reading-first-press-engine.js` SHA256 `52f30f9fd36f3f1ccb24bd833b14f91289d270df394f8418a77cc672ee7c5342`; `estate/assets/linotype/reading-first-press-frame.css` SHA256 `8e175ccbdfdd71e506979772059c72fcfb85de8d3daa366a34544ccc7d4502e6`; `source-lock.json` SHA256 `f10275f49d5da6837d6572b6508bb51b9752a4a25ffcb08ed4f9835fa986eee0`. The root `estate/index.html` is **unchanged** at `8ca2c693f4ae275f16331f3989790016a7f0ba3d0a2c2dc34d58e3a4f432478f`. Existing immutable inventory count: 1320 files.
- **Stage guard:** `Fountain-Coach/estate` branch `codex/linotype-fluid-nested-stage-20261105`, initial guard commit `c3caa8a77b16e11107d9f5bcb4a1f42f67841ed8`. Existing fail-closed `ReaderProvenanceGate` extended by a pinned v149→v150 admission only; test refused four forged source-lock, Git-commit, engine and CSS identities. Guard SHA256 `1c24269dcd8f50b4c7f720ad443a09ce4cd75b6b2c2503f1822169fd2f213c90`; v149 guard preserved in `reader_provenance_gate_v149_backup_20261105.py` SHA256 `12296b76f086a0b247b9bde3f2e772b92c636ee6c545018997ade00390c5f13d`.
- **Activation:** installed the new gate while v149 remained the active release, independently read back exact *old* root over both HTTP `:8200` and HTTPS `:8243`; then atomically renamed the same `current` symlink to the v150 immutable release and restarted only the same two existing preview services. Independent HTTP/HTTPS readback accepted both exact revised Press assets, unchanged root and running services; no new server, alternate Reader or public deployment.

## Verification — separately distinguished

**Before release:** 18/18 Chromium/WebKit viewport profiles over nine meaningful portrait/landscape shapes, including 390×844, 600×950, 740×1050, 820×1120, 900×1280, 1024×1366, 1200×1500, 1200×860 and 1440×900. Verified distinct increasing parent/inner widths, positive proportional inset, both exactly reconstructed source specimens, all 12 figure identities, complete page turning, no JS exceptions, no clipping or horizontal overflow. Representative live measured parent fields: 390×844 → 312px, 820×1120 → 670px, 1024×1366 → 844px; landscape 1200×860 → two real leaves with 488px each.

**True source continuation:** WebKit and Chromium both tested 390×690, verifying the classical specimen starts after a real prose paragraph on leaf 5 with source chars 0–241, and continues onto leaf 6 with chars 241–444, no loss or clipping. The former all-or-nothing placement is removed.

**Text enlargement:** 4/4 Chromium/WebKit 34px stress cases across 390×844 and 820×1120 passed with source-perfect paginated fragments; portrait phone displayed 125 leaves and 10 specimen fragments without source loss.

**Unrelated routes:** 8/8 Chromium/WebKit checks reopened the First Readings collection, Essays collection, Teatro and `To Read Is Not to Remember`. A larger Solstice route remains unaccepted by this regression, as it previously timed out.

**Actual activated HTTPS:** 18/18 Chromium/WebKit browser/viewport profiles passed *without substituting HTML, CSS or JS*. Before each profile, the browser independently retrieved and verified the exact served root, engine and CSS SHA256. Full leaf traversal, measured parent and inset geometry, two source texts and all figure identities passed. Actual live 390×690 continuation passed in both browsers. Actual live visual screenshots were inspected for 820×1120 and 390×690. Automated browser contexts used `ignoreHTTPSErrors` for the owner-WLAN CA; this is not a claim about the physical iPad's certificate trust.

## Unresolved versus accepted

**ACCEPTED:** v150 native fluid folio geometry, nested-source placement and continuation inside the existing Reader, private WLAN staging only. **NOT TESTED:** physical iPad Safari portrait/rotation, native VoiceOver editorial review, new human `Self Out Loud` recording/MIDI features, large Solstice route, public production. This receipt is not a public publisher or source-rights authorization.

**Direct author-WLAN route:** `https://192.168.8.50:8243/estate/#/read/essay--what-makes-a-page-modern`.

**Rollback:** restore `/home/benedikt/estate-shell-acceptance-staging/current` atomically to `releases/shared-shell-20261105-v149-nested-specimen-ce0c1cd`, restart the same HTTP and HTTPS preview units and verify v149 root + old Press asset digests. The v150 guard itself retains v149 admission, with guard backup available.
