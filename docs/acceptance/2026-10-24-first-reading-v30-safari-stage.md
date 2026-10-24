# First Reading — macOS Safari and functional icon staging v30

**Accepted staging observation: 24 October 2026.** The author showed a native macOS Safari screenshot of `https://works.benedikt-eickhoff.de/solstice/editions/first-reading/` with a linear manuscript and a cut-off opening page behind nonfunctional page controls. Subsequently the author requested that the recognized Lucide icon convention and this First Reading correction be **staged**, not promoted publicly. No browser refresh/caching actions are required from the author.

## Scoped authority and finite goal

- User-visible target: a genuinely measured, complete First Reading opening sheet with Next/Previous; no intermittent flash of raw HTML as if it were a finished book; an accessible, continuously scrolling original document if composition/JavaScript is unavailable; consistent already-approved functional Lucide icons without replacing original book or brand marks.
- Edition owner: `Fountain-Coach/solstice.fountain.coach` (private), `main` **`39904c52aefcbde20a0d0f8ddf14e5f04ecb3a1e`**.
- Measured reader/Compositor owner: `Fountain-Coach/fountain-press` (private), `main` **`8a57e6fa10a3d0acde8a9ff79608663afcdbbef5`**.
- Estate governance icon decision: `docs/decisions/2026-10-24-lucide-icon-and-brand-identity.md`, pinned `Lucide Static v0.468.0 (ISC)`. The Book entrance already uses the exact source-owned `lucide-book-open` SVG, the three Instruments icons use Lucide microphone, ear, and clapperboard, and the edition's own authored star/mark is intentionally not replaced. No unrelated logo, shared reel, Book page, icon file or artwork was mutated.
- Actual edition content: all **30 original authored works and 41 original images** preserved, in their prior order, with no text or image rewrites. The source owner's already-authored **Vergil series preface** and phone folio atlas are included in the staged edition, not claimed as separately newly authored by this repair. Book and Reframe Bookshelf are different publication roles.

## Production-first source lineage

**Public source observation before staging** confirmed exact same SHA-256 for the five relevant files as the canonical Ubuntu WLAN predecessor v26, independently over HTTPS:

| Affected live First Reading resource | Original public and v26 SHA-256 |
| --- | --- |
| `solstice/editions/first-reading/index.html` | `3faddbff97117fbe4e528ead6b714a093932d6f425806517d9c0ee8c18fb0e09` |
| `solstice/assets/book.css` | `a2b335a3b2b3ecf3a34dc84bf7c309409b9acf073b142970c15ad2c4fcff661d` |
| `solstice/assets/book.js` | `205d8c1fb36a81df21c0ff4895a5c545f8ce9ba623b9f56528d22f0d9a1c7b39` |
| `solstice/assets/linotype-engine.js` | `09cb3a9d94668abbf26d4cf4639be15999e153b364f2a8fa39337f28e8c34d6f` |
| `solstice/assets/reading-layout-policy.js` | `f098b7faf814fc7faa027bc5a5b9a24969dc181064beebbe7a4597ba335f001b` |

The existing single canonical environment stayed at `MacMiniDocker`, staging root `/home/benedikt/estate-shell-acceptance-staging/`, existing preview service `fountain-shell-acceptance-preview.service`, and the existing `http://192.168.8.50:8200/` entrance. No new DNS, editor environment, service, publisher identity or CI job was introduced.

The source-owned initial v27 overlay over immutable v26 modified exactly four Solstice files (original First Reading HTML, `book.css`, `book.js`, `linotype-engine.js`) and added exactly three owner files (`book-boot.js`, `mobile-page-navigation.css`, `mobile-page-navigation.js`). The initial preflight verified all **966** predecessor files preserved except that exact four-file delta; image and work order matched, and original provenance URLs remained available.

## Measured fixes, in original owners

1. The current Solstice source emits a synchronous first-paint bootstrap in the document head. It masks the unmeasured manuscript until the real measured sheets are admitted, with a bounded 12-second escape hatch if the scripts fail; with JavaScript disabled, full original HTML remains present.
2. Fountain Press and Solstice `book.css` make the **uncomposed/fallback state** a vertically scrolling document instead of an incomplete page. Page-turn controls and the mobile atlas are withdrawn in this state; the composed state and print mode are left unchanged. Exact Solstice source digest inventory (101 files) was refreshed.
3. At narrow phone widths, `book.css` removes the observed 5–78-pixel toolbar overflow by reducing the column gap. At widths at or below 390 pixels, the existing authored edition mark represents the identity where the full label cannot fit; proof, contents and appearance controls remain accessible. No replacement icon invented.
4. With the phone landscape folio atlas visible, the viewport's size can change **after** the Linotype leaf has been composed. Press and Solstice `book.js` now call the **existing** `engine.reframe()` immediately after atlas synchronization, so the accepted leaf fits the final available viewport without changing its page breaks or semantic source position.

All changes are checked in and pushed to their independent owner Git repositories. No Fountain Coach logo or Lucide path changes were needed.

## Exact live staging release and rollback

Current witnessed active staging release: **`releases/shared-shell-20261024-v30-first-reading-safari-39904c5`**. Retained predecessor: v29 `shared-shell-20261024-v29-first-reading-safari-f803c5c`. Immutable v26 production-baselined source, v27 owner edition, and v28/v29 intermediate cuts remain available. From v29 to v30, all **969** staged files were unchanged except for the single source-owned `solstice/assets/book.js` update, whose SHA-256 is `9550996d61bc229f082af630ae0a033e25707236edf6cc4128da0d5e35dbbfbc`. The accepted `book.css` digest is `68be4cce8b694d12d13ad5b47f11e91b725770f231ca849b4f3605f5df6ebaa6`.

Activation used the existing authenticated SSH, rsync, SHA-256 comparison, prechecked immutable candidate, atomic `current` symlink and restart of the pre-existing preview service. The stage `source-lock.json` retains origin and revision data, but no native typed EstatePublisher WLAN release receipt is claimed; the independently witnessed static SSH contract was used.

## Native Safari acceptance on macOS

A fresh native **macOS Safari** tab (not a Chromium impersonation) loaded `http://192.168.8.50:8200/solstice/editions/first-reading/#book-cover`. Browser JavaScript readback showed:

- `body.dataset.bookReady = true`, no book error, no residual first-paint admission overlay, and the original `#book-flow` hidden when the composed reader is shown.
- Landscape facing-page mode; a real single title-sheet cover inside the viewport; original 30 works and 41 source image references present. **Inner cover content** exactly fitted the measured `.linotype-area`, and the physical sheet fit the visible viewport. An earlier provisional diagnostic had incorrectly compared the outer sheet to the inner content area and is superseded by this more specific native measurement.
- Page position `1 / 183` accepted, **Next → 2–3 / 183 → Previous → 1 / 183**. Font and WebKit metrics can legitimately produce page counts differing from Chromium; this is not a textual truncation.
- The original user screenshot remains an independently observed failure of the previously published state. This native stage witness verifies the new staged projection, not a production Safari repair.

## Independent Chromium / absent-JavaScript checks

Chromium headless tested the actual staging HTTP route with cache disabled at desktop **1600×900**, phone portrait **393×852**, phone landscape **852×393**, including real Next/Previous behavior (visible buttons on desktop; keyboard on phone), complete source identity (30 works, 41 images), stage cover within actual measured inner leaf bounds, and **zero horizontal overflow**. The recorded working page counts were 204, 244 and 217 respectively; every tested view entered the composed state with no JavaScript exceptions.

In a separate page per size, JavaScript was disabled. In all three sizes, the complete 30-work source remained visibly and vertically scrollable, the viewport's overflow was visible, page-turn and atlas controls were absent, and there was no horizontal overflow. These are Chromium negative tests, **not** a claim of a physical iPhone or iPad Safari witness. Actual macOS Safari passed the composed-view test above. The author does not need to become a browser-matrix operator.

The live URLs `/solstice/editions/first-reading/`, the four new reader support assets, the pre-existing proof, `/book/`, `/works/books/` and `/status/references/` returned HTTP 200. The canonical stage sent `Cache-Control: no-store` and `X-Robots-Tag: noindex`. Static assets were read back at exact expected SHA-256 digests.

**Production and approval boundary:** public `https://works.benedikt-eickhoff.de/solstice/editions/first-reading/` still returned SHA-256 `3faddbff97117fbe4e528ead6b714a093932d6f425806517d9c0ee8c18fb0e09`, and its unchanged original `book.js` was independently read back. No production Solstice, Book, Works, Status or Instruments route was promoted, and no private documents or Reframe Bookshelf state were published.

## Completion / next separate decision

This acceptance closes the requested **WLAN staging** work only. The author can directly proofread the staged First Reading edition in Safari. A future public rollout is a separate release approval and needs an exact immutable artifact, route-specific typed EstatePublisher release/rollback receipt, and independent public HTTPS/Safari readback.
