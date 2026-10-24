# Book: publishing-led staging v23, grounded in a real readable edition

**Date:** 24 October 2026. **Author direction:** Replace v22 obsolete development-manual reading links. Book must explain what publishing books means, demonstrate it through a real work, and verify what can be truthfully witnessed. The user explicitly said: "Document and stage accordingly."

## Editorial decision and source

The governing proposition is **Publishing makes an authored work independently encounterable without losing the identity of its source**. A book is not a page, a file, a command inventory, or a private Bookshelf admission inferred from a public URL.

Source owner: Fountain-Coach/book-of-reframe, revision be231f7a033d1da60337b3168615a89f3da78c40. Read the source-owned decision at docs/decisions/2026-10-24-book-publishing-purpose.md and complete static routes in site/index.html, site/publication/first-reading/index.html and site/history/reframe-development/index.html.

New editorial topology:

1. **The actual published reading:** First Reading — Solstice at https://works.benedikt-eickhoff.de/solstice/editions/first-reading/, not a simulated new book or decorative cover.
2. **How a book is published:** authored source, selected edition, source-faithful composition and separately authorized public release. Fountain Press, Reframe/FountainStore and EstatePublisher remain different authorities.
3. **What can be witnessed:** measured HTTP route availability, source-labelled entry, the edition's own author and content statements, and explicit evidence that remains unknown.
4. **Historical reference only:** the older August 2026 Reframe command/scenario manual survives at /book/history/reframe-development/; none of its technical article routes has been rewritten, rebranded as an admitted book or promoted to current product capability.

On 24 October the original First Reading, a standalone original-entry page from 22 December 2025, and a second standalone entry from 6 September 2026 all returned HTTP 200 over public HTTPS. The edition describes itself as a selection of thirty works with forty-one original images and identifies Benedikt Eickhoff. These self-descriptions have not been inflated into independent source-rights certification, a specific FountainStore admission or a typed EstatePublisher receipt.

## Development / staging / production lineage

- Git source owner: Fountain-Coach/book-of-reframe, parent 7737c9b59d6cddb86e8bf44c84f94d73e6938c7f, new revision be231f7a033d1da60337b3168615a89f3da78c40.
- Independently verified public production Book site: book.fountain.coach/current -> releases/estate-20261024-v14-satzfunk-reel-book, unchanged throughout this operation.
- Canonical registered WLAN staging: MacMiniDocker / home/benedikt/estate-shell-acceptance-staging/current, served on port 8200 by the existing fountain-shell-acceptance-preview.service.
- Verified v22 staging predecessor: shared-shell-20261024-v22-semantic-book-7737c9b.
- **Activated v23 staging:** shared-shell-20261024-v23-book-publishing-be231f7.
- v22 had already incorporated the actual production Book deep HTML routes; the candidate was a full copy of v22 plus the explicit Git development delta. All 743 predecessor files were preserved: only book/index.html and book/assets/site.css changed; four files were added (Book publication-case HTML, historical-reference HTML, social SVG and matching 1200x630 PNG). source-lock.json gained the bounded semanticPublishingBookStage receipt. All other estate pages and static assets retained exact predecessor bytes.
- Existing authenticated SSH, rsync, SHA256 comparison, atomic symlink activation and preview-service restart were used. No new service, DNS, GitHub CI, Store, remote helper or sidecar was introduced.
- This stage activation was **not** issued as a typed EstatePublisher WLAN receipt. The actual source-lock observation and independent HTTP/browser witnesses below are what were obtained. No public release authority is claimed.

## Stage HTTP acceptance (all exact SHA256 matched)

All live HTTP readbacks at http://192.168.8.50:8200, status 200:

| Route | SHA-256 |
| --- | --- |
| /book/ | df44a6fdb94ba167570b83e11f40decaaf90a442682c83526719d987cffa5f6f |
| /book/assets/site.css | 877661283fc9ed731b7227fae5456277fd7df44ce1f8a74a5292ff2407dbcb83 |
| /book/assets/book-publishing-social.png | 63967dd2ed58318efe7535a2c65d229d9baa8af271b0234156fce85845d83c15 |
| /book/publication/first-reading/ | 2be6fec49378cce2e4d71ce6be6fdcb723dcd49d0614479b8c00fb91015c2f82 |
| /book/history/reframe-development/ | 7922b989141ae01b9b478620b3a5ff35d0412d5f83c66fe107addc3e120405ee |

Existing retained routes /book/scenario-driven-development/, /book/scenarios/, /book/commands/commands/, /book/csound-teatro/, /instruments/ and /governance/ each returned HTTP 200. WLAN staging headers remained Cache-Control: no-store and X-Robots-Tag: noindex, nofollow.

## Browser-level acceptance

Existing local Chromium automation opened the canonical WLAN entry at 1280x900 and 393x852. Both yielded HTTP 200, one main/one H1 ("A book, published."), no horizontal overflow, loaded standard book-open logo, present estate reel and legal footer, no JavaScript page errors, direct live edition link, correct publication-case and historic route links. Clicking the actual case link navigated to /book/publication/first-reading/; its public source references and independent-witness text were present. Navigating to /book/history/reframe-development/ found the old technical 95-entry inventory and a clear historical/not-admitted statement. Full-page desktop/mobile screenshots were retained privately in .semantic-book-publication-stage-20261024 on the owner's connected Mac, not falsely claimed as native Safari/iPad or public assets.

## Open acceptance

The author may proofread and revise the v23 staging editorial text and visual hierarchy. Native Safari/iPad QA and separate authorization for public production promotion have not yet occurred. The unchanged prior v22 immutable release is retained for rollback.
