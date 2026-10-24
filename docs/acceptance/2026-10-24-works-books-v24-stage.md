# Published Works become books — WLAN staging v24

**24 October 2026.** User direction: the previously job-acquisition-facing published Works should now become visible and readable as books.

## Owners and evidence

- Works owner revision: Fountain-Coach/works-benedikt-eickhoff 3c31eea2fa1493c47903c8d648438c5665332b41.
- Works public baseline: revision 27f2fadbdf6eb1b3d60ab744d0f277a92a797260; production homepage SHA256 5d5de0ce48b571523800b0d3a5573efb26b9a9c427c59fd711300682407e47da, independently observed unchanged after staging.
- Book owner revision: Fountain-Coach/book-of-reframe 184052d47b2b8ade5f7c9de990627671376bd333.
- Book public production stayed on releases/estate-20261024-v14-satzfunk-reel-book.
- Works source decision: docs/decisions/2026-10-24-published-works-become-books.md. Catalogue source: content/book-catalogue.v1.json, with original and facsimile SHA-256 digests.

## Actual books and their existing readers

- Between Gardens: 2026 source score, paginated 15-image reader; Benedikt Eickhoff.
- Ballern Gehen: FCKFRG & MI 2023 treatment; existing eight-page Linotype documentary facsimile of six original pages.
- A Midsummer Night's Dream: FCKFRG & MI/Shakespeare source comparison; existing 110-page Linotype facsimile of 108 original pages. No invented translation.
- Above the Line: English original five-page essay; no separately typeset Linotype edition claimed.

The unsent application, diploma and legal records remain non-books. No private Reframe Bookshelf membership or rights clearance is inferred.

## Staging lineage

- Canonical existing Ubuntu Mac mini WLAN stage, port 8200; verified predecessor shared-shell-20261024-v23-book-publishing-be231f7.
- Activated immutable v24 release shared-shell-20261024-v24-works-books-3c31eea. v23 remains available for rollback.
- All 747 predecessor files retained; only book/index.html and book/assets/site.css changed. Exactly 68 new Works static files added, including 38 bilingual HTML routes. Other estate routes, legal/footer and original Book publication case preserved.
- The Works owner provides /works/, /works/books/, four /works/books/<slug>/ book readers, plus their English equivalents. Book links to these same local WLAN routes at /book/. The former public Works site remains unchanged.
- Used existing authenticated SSH, rsync, verified source hashes and atomic symlink activation, plus restart of the existing preview service. No new service, runtime store, DNS, CI or cloud resource.

## Independent acceptance

- Works authoring validation: 38 HTML pages, 10 PDFs, zero broken local links.
- Active staging HTTP 200: /book/, /works/, /works/books/, all four German book entrances, English books index, representative facsimile/essay PDFs with application/pdf MIME, and preserved /instruments/.
- Exact staged source-to-PDF SHA-256 joins and repository owner revisions independently checked before activation. The book programme cards open the Works-owned staged routes.
- Browser inspection at 1280 and 393 pixel widths passed Book portal, book grid, Ballern Gehen PDF reading link and Between Gardens score reading link without horizontal overflow.
- Staging is noindex/no-store. This is a source/Git-to-WLAN staging outcome, **not** public publication, a new private Reframe admission, native Safari acceptance, or a typed EstatePublisher WLAN receipt.

Public promotion of the new book routes requires separate author authorization. 
