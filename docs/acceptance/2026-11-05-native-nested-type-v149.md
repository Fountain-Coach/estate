# v149 — Native nested type in the existing Fountain Press Reader
5 November 2026 · private owner-WLAN staging · exact technical acceptance

## The rejected v148 composition

The same historical specimen passage was intentionally set in two different typographic styles. In v148 each style was a fixed-dimension SVG (742×602 and 649×598) treated as ordinary figure artwork. The original Press viewport composer scaled those images from intrinsic aspect ratios and capped their height against the physical leaf; the specimen's words, line breaks, inside margins and typography did not respond to changes in the surrounding Satzspiegel. An essay-local `padding-inline:0!important` figure reset also overrode the nested inset. Decorative borders could not correct those faults. The author rejected v148's apparent result.

## The scoped change

The new **v149** composes the passage twice as **actual source-addressed text** under a single parent Fountain Press paginator. Classical setting uses centred serif heading and measured justified text; modernist uses bold asymmetrical sans and ragged-right text. Both inherit the available sheet width and font scale and use responsive font-relative margins and padding. They create no page inside an image, fixed width, fixed height or new compositor.

The existing `inFlowFigure` dispatch calls a narrowly-scoped `inFlowSpecimen` path for actual `figure[data-typographic-specimen]` elements. It uses `fits(leaf.area)` and source-character fragments when even a full leaf cannot contain the setting, then verifies reconstructible source identities. Ordinary images still use the established image path. The essay-local zero-padding override applies only to actual artwork, not the nested type. Historical SVG assets remain unchanged and are retained for provenance, but are not displayed as text substitutes.

## Git source, stage ancestry and file inventory

- Source owner `Fountain-Coach/fountain.coach`, branch `codex/linotype-nested-specimen-measure-20261105`, commit **`ce0c1cd704664027d94d6dd4c196b9c06e037e38`**. The combined essay manuscript is unchanged at SHA-256 `8f7d60f9ae3cfd1dd6e95a92d869c050241a93482ab00688be7ad3422d2786d6`.
- Single authoritative specimen passage: `site/essays/what-makes-a-page-modern/specimen-source.txt`, SHA-256 **`693ca56d01757d03d2210234def136256cd04145efce95fc1fc205cf15c6658a`**. The two settings render identical source characters.
- Staging predecessor (retained immutable): `shared-shell-20261105-v148-specimen-boundary-a9575ba`, original root SHA-256 `532dbdf6603fb1300a974418130c50cbc17636262d9dcf7c0a802c3aabfdd81c`.
- New active, independent 1320-file candidate: **`shared-shell-20261105-v149-nested-specimen-ce0c1cd`**. Existing Reader, shell, navigation, source books, all 12 figure identities and private audition media remain in place.
- Exactly four files changed from v148: `estate/index.html` → `8ca2c693f4ae275f16331f3989790016a7f0ba3d0a2c2dc34d58e3a4f432478f`; `estate/assets/linotype/reading-first-press-engine.js` → `67a3c842c92e86839a35cbee44c533d143f893eda954d750c0eddfffcad64058`; `estate/assets/linotype/reading-first-press-frame.css` → `f7a85b7e573655bee124dc4218c0cb9ecdc4300b433b5ab0237e734507a03c03`; and `source-lock.json` → `935275ea1f3971a4307d6df445c7c925e005e8ce3be50ea0d25fa9dd309932e2`.
- Stage guard owner `Fountain-Coach/estate`, branch `codex/linotype-nested-specimen-stage-20261105`, initial gate commit `44084cd1f8a9c96ae5669d94f3628f8221f5227b`. Installed v149 gate SHA-256 `12296b76f086a0b247b9bde3f2e772b92c636ee6c545018997ade00390c5f13d`. The exact v148 guard was backed up with SHA-256 `765606ce63c53a3b2cef69ecd20d6f1117a0d2a58247193b65af16edf478d351`.

## Verified tests and source authority

- **Before deployment:** the v149 prospective ReaderProvenanceGate accepted the full v140→v149 lineage, the exact three new Reader assets, unchanged original v145/v146 private Qwen media and existing stage inventory; four deliberately forged source-lock, source-commit, manuscript-SHA and specimen-SHA configurations were refused.
- **Continuity:** the new guard was installed with v148 still active; existing HTTP :8200 and HTTPS :8243 independently returned **the exact v148 bytes** after restart, before activation.
- **Atomic activation:** `current` symlink switched only from the immutable v148 directory to v149, restarting the same two existing user-level preview services. Both HTTP and HTTPS independently returned the exact v149 root digest `8ca2c693...`; both services were active. No new hosting route or alternate Reader.
- **Source and compositor QA before activation:** 6/6 Chromium/WebKit viewport profiles at 820×1120 (17 portrait leaves), 1200×860 (26 leaves) and 390×844 (36 leaves); all 12 figure identities reached, exactly two nested text settings, source reconstruction exact, zero specimen SVGs or fixed image dimensions, text and frame inside actual parent `linotype-area` with no horizontal overflow. The larger-type stress at a forced 34px page-font passed 4/4 Chromium/WebKit profiles: 390×844 produced 120 leaves and 12 source-contiguous specimen fragments; 820×1120 produced 46 leaves and 4 fragments, none clipped or lost.
- **Actual activated HTTPS, with NO HTML/JS/CSS interception:** all 6/6 Chromium/WebKit profiles independently checked the served root, Press engine and Press CSS digests, traversed all leaves, reached all 12 semantic figures and proved the exact specimen text. WebKit actual-live visual readback showed both in the parent 624px type area at x=98…722px, positive 15.3px fluid inset, and no image/canvas/SVG nested type. Unrelated First Readings collection, Essays collection, Teatro and `To Read Is Not to Remember` reopened in 8/8 Chrome/WebKit route checks. A larger Solstice route timed out in a broader preview, so that route is **not** independently accepted by this effort.
- **Limits:** Browser automation bypassed the private WLAN CA trust errors. Physical iPad Safari, VoiceOver, real microphone/MIDI instrument and publication production are **not** accepted or claimed. Preexisting background audio preload cancellations were separate warnings, not new audio acceptance.

## Recovery and direct stage

The original v148 release remains untouched. To roll back, atomically restore `/home/benedikt/estate-shell-acceptance-staging/current` to `releases/shared-shell-20261105-v148-specimen-boundary-a9575ba` and restart only the two existing preview services. The installed v149 guard still admits v148. Its v148 backup is available should guard rollback itself be necessary.

**Exact private WLAN Reader URL:** `https://192.168.8.50:8243/estate/#/read/essay--what-makes-a-page-modern`

**Status: v149 ACTIVE PRIVATE STAGING, independently browser-verified. No public production effect.**
