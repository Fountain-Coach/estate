# v150 — Fountain Press fluid folio and nested typographic flow
5 November 2026 · owner-WLAN private staging

## What failed in v149

The user rejected the nested type-stage because its margins and page transitions did not behave as part of the surrounding Linotype book. Actual v149 WebKit geometry proved two specific compositor defects:

1. `reading-first-press-engine.js` capped every `pageFrame` folio at 700 CSS px and its side stegs at 38px. At 740, 820, 900, 1024 and 1200px portrait widths, the real `linotype-area` therefore remained 624px and the classical specimen remained 568px. A valid source string and no CSS overflow did **not** make this responsive.
2. `inFlowSpecimen` attempted the *entire* nested figure first; if it could not fit the remaining folio, it immediately opened a new leaf rather than compose an actual readable prefix beside preceding prose.

The earlier v149 tests covered containment and source reconstruction but not elastic parent measure or usable remaining folio space. Those acceptance claims were therefore insufficient for the user's reported problem.

## The bounded correction

The **existing** production-derived Fountain Press Reader remains the host. The revised `pageFrame` code derives width from the actual measured Reader viewport: single complete leaf in portrait or two complete folios in eligible landscape. Side margins are proportional to the resulting leaf width, rather than capped at 38px. Classical and modernist inner type paddings scale with their live parent measure; neither has a hardcoded image viewport or transform.

`inFlowSpecimen` now measures prefixes in the *current* folio using the same `fits(leaf.area)` check as ordinary text. When the opening prefix contains fewer than two actual lines, it moves to a fresh leaf; otherwise it remains after the preceding prose and continues in the next folio using contiguous source-character addresses. Genuine image illustrations still follow their established intrinsic-image path.

No manuscript paragraphs, original SVG/source assets, private audio, reader app, header, library membership, publisher domain or public production bytes changed.

## Exact authorities

- Source implementation: `Fountain-Coach/fountain.coach`, branch `codex/linotype-fluid-nested-flow-20261105`, commit **`3ba1b0e826efcec947e243100c2925ad78d2953e`**. This is the accepted **stage-specific Reader projection**, not a claim that the separate `Fountain-Coach/fountain-press` main branch has been changed.
- Stage provenance/guard: `Fountain-Coach/estate`, branch `codex/linotype-fluid-nested-stage-20261105`, first guard commit **`c3caa8a77b16e11107d9f5bcb4a1f42f67841ed8`**.
- Immutable predecessor, preserved for rollback: `shared-shell-20261105-v149-nested-specimen-ce0c1cd`.
- Immutable **active private staging**: `shared-shell-20261105-v150-fluid-nested-3ba1b0e`, 1320 files copied from v149 without adding or removing any.
- Exactly three files changed against v149:
  - `estate/assets/linotype/reading-first-press-engine.js` SHA-256 **`52f30f9fd36f3f1ccb24bd833b14f91289d270df394f8418a77cc672ee7c5342`**
  - `estate/assets/linotype/reading-first-press-frame.css` SHA-256 **`8e175ccbdfdd71e506979772059c72fcfb85de8d3daa366a34544ccc7d4502e6`**
  - `source-lock.json` SHA-256 **`f10275f49d5da6837d6572b6508bb51b9752a4a25ffcb08ed4f9835fa986eee0`**.
- Unchanged `estate/index.html` SHA-256 `8ca2c693f4ae275f16331f3989790016a7f0ba3d0a2c2dc34d58e3a4f432478f`; combined manuscript and author-owned source-addressed specimen unchanged. Historic SVG plates remain in the original asset inventory.
- Installed v150 Reader provenance guard SHA-256 `1c24269dcd8f50b4c7f720ad443a09ce4cd75b6b2c2503f1822169fd2f213c90`; exact v149 guard backed up as `reader_provenance_gate_v149_backup_20261105.py`, SHA-256 `12296b76f086a0b247b9bde3f2e772b92c636ee6c545018997ade00390c5f13d`.

## Independent acceptance and negative evidence

**Source and candidate:** 18 Chromium/WebKit viewport profiles across 390×844, 600×950, 740×1050, 820×1120, 900×1280, 1024×1366, 1200×1500, 1200×860 and 1440×900. The measured portrait `linotype-area` expanded 312px → 490px → 602px → 670px → 738px → 844px → 992px, rather than stalling at 624px. Both nested settings remained inside the live parent measure with proportionally positive insets, no fixed SVG, no horizontal overflow, all 12 semantic figure identities and exact specimen source reconstruction. The 34px enlarged-type stress passed **4/4** (Chrome and WebKit at 390×844 and 820×1120) with character-perfect paginated continuation. Unrelated First Readings, Essays, Teatro and another essay paths passed in both engines.

**The exact previously missing flow:** At 390×690, both browser engines showed an introductory `P` followed by a first classical-specimen fragment on **leaf 5**, source positions **0–241**, followed by the exact remaining **241–444** on **leaf 6**. This is real geometry-dependent continuation, not a whole-specimen displacement.

**Reader provenance:** The prospective v150 guard admitted the actual candidate, the complete inherited v140→v149 Reader release chain, unchanged HTML/other assets and the original private audition page/MP3s. Four forged source-lock/commit/engine/CSS identities were independently refused. Guard installed while v149 remained active; after restart, HTTP :8200 and HTTPS :8243 still returned exact v149 bytes. The active symlink was then switched **atomically** to v150, restarting only the two existing user preview services.

**Actual activated HTTPS:** Both HTTP and HTTPS independently served exactly the new JS and CSS SHA-256 digests; root HTML remained unchanged. **18/18** actual live Chromium/WebKit profiles re-read those served asset hashes, traversed the book and verified both nested source strings, no horizontal overflow and 12 figure identities. **2/2** live continuation cases matched source positions 0–241 and 241–444 across leaves 5/6. **2/2** runtime-resize cases recomposed 820×1120 → 1024×1366 → 820×1120: measure 670 → 844 → 670px, folios 17 → 13 → 17, with source identity intact. **8/8** other-book route checks (First Readings, Essays, Teatro, `To Read Is Not to Remember`) reopened under the actual v150 server. Actual live portrait and large-page WebKit screenshots were visually inspected, including the two-page source-contiguous specimen at 390×690.

## Limits, rollback and link

These are browser and remote-server witnesses, **not physical iPad Safari, native VoiceOver, certified TLS trust on the test browser, global Press-main promotion or public-production publication**. The older full Solstice route has not been newly admitted by this bounded test; no claim about it follows from the other-book smoke checks. Private media remains stage-only.

Rollback requires restoring the existing `current` symlink atomically to `shared-shell-20261105-v149-nested-specimen-ce0c1cd` and restarting the same two existing preview services; the installed v150 guard still admits v149. The exact prior guard backup remains available if separately needed.

**Existing owner-WLAN Reader route:** `https://192.168.8.50:8243/estate/#/read/essay--what-makes-a-page-modern`

**Status:** v150 ACTIVE PRIVATE STAGING, source- and browser-verified. No public production changes.
