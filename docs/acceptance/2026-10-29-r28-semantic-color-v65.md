# R28 v65 — Source-bound containment color on canonical WLAN Reader

**Date:** 29 October 2026.  
**Scope:** Restore the spatial color language of the author's 15 October Fountain Press / Reframe reference without restoring ordinary website chrome or fabricating new books or containers. **Result:** immutable private-WLAN stage active and independently browser/AX observed. **Not** public publication, native Reframe Store admission, or physical iPad Safari/VoiceOver acceptance.

## Meaning and source ownership

The earlier [Reframe R21 scenario](https://github.com/Fountain-Coach/Reframe/blob/main/scenarios/021-basic-entrance-and-situated-estate.md) establishes the distinction **color follows current containing space, never book title, genre, Score or artwork**. Its native test showed one source-backed teal membership context; it did not authorize arbitrary additional colors. The author reiterated the importance of color after reviewing the 15 October screen and instructed proceeding on 29 October.

For this bounded WLAN projection, the existing *First Readings* source collection at `Fountain-Coach/fountain.coach/site/collections/first-readings/collection.json` is the authority for the one verified displayed membership `teatro-an-unfinished-composition` (SHA-256 `8cbaa8cf73400602d0d61520f18d3b8f2e7885e2570981e941a6184b29d91314`). A separate author-directed [presentation record](https://github.com/Fountain-Coach/fountain.coach/blob/main/site/collections/first-readings/containment-presentation.v1.json) binds the named teal tone to **this exact digest and member identity**, rather than to the book's title or the global root. Its tone values are a **staging visual reconstruction** (teal `#4a8982`, containing field `#d4d8cf`), **not an independently verified numeric color-token readback from the historical 15 October native binary**.

Fountain Press `runtime/bookshelf.py` accepts `containing_context` only in a real collection `app_surface=True`, and refuses an unmatched collection ID, member list, malformed source digest, unknown hue or color on the neutral root. Press `runtime/bookshelf.css` owns the collection field, 5px left rule and circular open-hand boundary. Press `runtime/book.css` owns **only** a narrow containing-space signal on the member reader toolbar and pagination. The book's manuscript, source-art cover, page sizing, score and real Press runtime remain unchanged. `Fountain-Coach/fountain.coach/scripts/build_edition_hierarchy.py` now validates the **generated exact collection-manifest bytes before rendering or applying color**, so stale preexisting collection files cannot silently authorize an unrelated newly generated book. Focused Press tests **15/15 passed**, including negative root/membership cases.

## WLAN release and lineage

| Field | Verified value |
| --- | --- |
| Registered Mac mini | `MacMiniDocker` at `192.168.8.50:8200`; existing `fountain-shell-acceptance-preview.service` |
| Reader root | `http://192.168.8.50:8200/estate/` |
| Colored collection | `http://192.168.8.50:8200/estate/collections/first-readings/` |
| Contained book | `http://192.168.8.50:8200/estate/editions/essays/teatro-an-unfinished-composition/` |
| Active immutable release | `shared-shell-20261029-v65-reframe-color-8b4e961` |
| Retained immediate predecessor | `shared-shell-20261029-v64-reframe-app-ef6e193` |
| Stage source code | `Fountain-Coach/estate/staging/r28_semantic_color.py` at `8b4e96156d799375355c0b71ee25238da813a4cf` |
| Server state | Active `current` symlink points to v65; existing preview service restarted, independently reported `active` |
| Production effects | **None** |

The builder checked the exact immutable v64 predecessor and source HTML/CSS digests, collection membership and identified source CSS, then constructed v65 without modifying the active release until activation. An initial **nonactive** candidate ending in `d21c324` exposed 120+ lines of unrelated later Press book CSS when a whole file was copied. **That candidate was not activated.** The builder was corrected to append **only the two Press-owned teal reader rules** to the exact previous book.css, with no unrelated pagination, typography, toolbar or fallback changes. A complete `diff -qr` of final v64/v65 shows exactly four changed route/assets plus `source-lock.json`.

| Artifact | Live v65 SHA-256 |
| --- | --- |
| Root Bookshelf HTML (preserved identical to v64) | `c9d8fb59fcd4fc9079124bc2a04c9b58b6c5a5d4cda534b173be3b0a535f386d` |
| First Readings HTML | `7190fcb230e5a94b7800fd056b7b1a3d86b921d8981c131adff6b9ae31e24d26` |
| Nested `An Unfinished Composition` reader HTML | `281b37e8e1a7a82ad6ac168702a7b687441fb38a6403a6f5629f42f6aa2e0a4a` |
| Fountain Press Bookshelf CSS | `f6a93b5b5e78697d5b92fdf862d9640b7e81923b2564a32667f9fe66215c792c` |
| Reader book CSS (old bytes + two color rules only) | `2c2a80839da91f6e83a21a317e2f7404da2881b6c9fec6f3136dbad823ba8afb` |

## Dynamic evidence

The actual Chrome DevTools Protocol browser on the authorized Mac read the *served* WLAN stage, not the candidate directory alone, at **iPad landscape 1024×768**, **iPad portrait 768×1024**, and **mobile 390×844**. All **three full root → First Readings → An Unfinished Composition → hand/home root** journeys passed (browser test exit code 0), with no failed resource responses, JavaScript exceptions or horizontal overflow.

In every profile: root `body` retained neutral `rgb(223,217,206)`, **no containing-space attributes**, two original covers and 20 inert vacancies. The real First Readings collection exposed `data-containing-space-id="first-readings"`, the original collection SHA and `data-containing-space-tone="teal"`; its Press field measured `rgb(212,216,207)`, left inset border `rgb(74,137,130) 5px`, matching circle boundary, one original sourced member cover, 20 vacancies, and named AX heading / hand link. The contained edition bore the **same context SHA/tone** and a computed teal inset on its native book toolbar; its real book viewport and root hand were intact. The screenshots at iPad-landscape and phone size were visually inspected; the colored field is unmistakable without recoloring cover art.

**Known open:** the nested contained book still displays its **historic nine-domain website masthead** above the genuine book toolbar. That layout defect existed before v65 and remains an independently actionable Reader-wide app-surface correction. The root presents First Readings through its historical source-owned collection *cover*, not the fully reconciled R21 native structural-space relation; do not mark the whole R21 product journey accepted. Color is supplementary orientation alongside accessible collection labels, original work identity and keyboard/hand navigation. Numeric historical color-token parity, physical iPad/Safari/VoiceOver and public HTTPS two-domain alias/redirect remain unverified.

Public readback stayed unchanged: `https://fountain.coach/` returned HTTP 200 with the older 18,449-byte portal, and `https://benedikt-eickhoff.de/` still returned HTTP 308 to `https://works.benedikt-eickhoff.de/`. The staging route `/estate/` and `EstatePublisher` remain *internal historical compatibility names*, not public Reader branding. **No typed public publisher receipt, public distribution right or Store admission is claimed.**
