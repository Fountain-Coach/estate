# v25 Works Books — folio reader replaces PDF handoff

**24 October 2026.** User observed that the v24 Books merely propagated **Open PDF**, without featuring the reader. This is a verified mismatch between the proposed book programme and its actual reading action. v25 fixes that bounded defect in the existing Works source and WLAN stage.

## Actual software and source ownership

- Source Git: Fountain-Coach/works-benedikt-eickhoff revision 837510664fa90d2883d7670c13ecab287f6d4f49 (parent 3c31eea2fa1493c47903c8d648438c5665332b41).
- Works authoring files: book_editions.py (source-bound book routes), assets/folio-reader.js (existing score-reader pattern extended to four books), assets/site.css, render_book_folios.py (authoring-time image extraction), content/folio-facsimiles.v1.json (SHA-256 of existing PDF and individual folio image bytes).
- Ballern Gehen: eight already Linotype-composed documentary PDF pages; A Midsummer Night's Dream: 110 existing facsimile pages; Above the Line: five source-original essay pages. 123 leaves were reproduced as static WebP images without changing the PDFs.
- Between Gardens retains its 15 original image pages and source PDF; its new Works book entry presents those already owned leaves directly.
- The existing printed pages are the source presentation. In-page previous/next, landscape-facing spread, mobile single leaf, arrow-key and touch gestures, source-digest-bound local reading continuity and folio permalink live in the Works static reader.
- The browser PDF plug-in and embedded iframe are removed from all eight Works book-entry routes. PDF remains a secondary archival/source link.
- Explicit limitation: these are source-faithful image-facsimile leaves, NOT proof of a fully measured/reflowable Fountain Press text reader, a Reframe writer/editor workspace, or a FountainStore Bookshelf admission. The prior PDF source and authorial credit remain separately available.

## Staging lineage

- Exact verified immutable predecessor: shared-shell-20261024-v24-works-books-3c31eea; rollback retained.
- Active immutable owner-WLAN release: shared-shell-20261024-v25-works-folio-reader-8375106, on existing Ubuntu Mac mini port 8200.
- Pre-activation diff: all 815 predecessor files retained; exactly 10 existing Works files modified (eight bilingual book entrances, Works CSS and catalogue), exactly 125 new files (123 WebP leaves, one reader JS, one manifest). Book domain HTML/CSS, other estate pages and previous technical chapters preserved byte-for-byte.
- Existing OpenSSH, rsync, SHA-256, symlink activation and preview-service restart were used. No new DNS, service, cloud store or GitHub CI. The native typed EstatePublisher WLAN receipt was not obtained, and such a receipt is not claimed.

## Exact pre-activation source evidence

- Staged Works /books/ballern-gehen/index.html SHA256: 6d1b01ec16503bb0f420f1e9963572bc3371a03ce5c8fdb14af5b589bc5a565f.
- Reader JS SHA256: 94069215aa2531892e9890fa2c73c8b6cbf2a4129f36aac553d2f4f51606c79e.
- Digested folio manifest SHA256: ce28271a8f53c58dc16e183abf9b3afa39b24631dcaba035c00ef87d777c2cf1.
- All 123 individual page image digests matched the authoring manifest, and its PDF source SHA-256 digests matched the actual original PDF bytes.

## Live browser witness on the canonical WLAN stage

Browser tested source at http://192.168.8.50:8200/works/books/ with Chromium at desktop 1280×900 and mobile 393×852 for each of four books. All eight book entry readbacks returned HTTP 200; no horizontal overflow, no PDF iframes, reader present, first folio image loaded. Starting at explicit #folio-1 and using the actual Next control:

- Desktop: cover 1/N opens measured 2–3/N facing leaves, with BOTH page images loaded, no JS errors.
- Mobile: cover 1/N opens single leaf 2/N, with the opposite leaf hidden.
- Counts verified: Ballern Gehen 8, A Midsummer Night's Dream 110, Above the Line 5, Between Gardens 15.
- Folio address updated to #folio-2; local source-hash reading continuity was observed between visits. The browser QA script was corrected to use explicit #folio-1 after stored continuity initially caused a false expectation about starting position. Both profiles then passed without modifying the reader.
- Desktop/mobile full-page screenshots retained privately in the owner Mac source-work scratch directory .works-folio-reader-stage-20261024, not passed off as native Safari/iPad testing.

Current production Works homepage remained byte-identical to its pinned baseline, SHA256 5d5de0ce48b571523800b0d3a5573efb26b9a9c427c59fd711300682407e47da. Public Book release symlink remained releases/estate-20261024-v14-satzfunk-reel-book. Production unchanged.

## Acceptance boundary

This stage provides a *real static in-page folio reader* for all four previously PDF-first books, not just a prettier Open PDF link. It does not yet provide Fountain Press's full semantic text composition and editing/reflow contract. User proofing on native macOS Safari and iPad and separate public production authorization remain open.
