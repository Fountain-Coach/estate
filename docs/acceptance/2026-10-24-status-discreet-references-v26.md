# Discreet references and editorial-backstage boundary — v26 WLAN staging

**24 October 2026** — author request: make Works' backstage/off-reel role a bounded long-term rule, and add a supporting Status section for recipient-directed documents without promoting private Jobcenter/legal correspondence or making government-office recipients subject to website tracking. No actual private document was supplied or approved for publication.

## Decision authorities

- Estate semantic boundary: `docs/decisions/2026-10-24-editorial-visibility-and-discreet-references.md`.
- Status authoring and privacy boundary: `Fountain-Coach/status.fountain.coach`, source Git `main` at `f4e1e2981e2bb6945a78e9c36ade6f50dd2f2a23`; Status site content last altered in `876b61389cf584d1e98db76592a3684e8086783a`.
- Source site route `site/references/index.html` is complete HTML with inline CSS, no JavaScript, cookies, remote fonts, analytics or third-party embedded content. `site/transparency/index.html` has the context entry link. Both include return navigation. Status `AGENTS.md` explicitly rejects publishing private correspondence in public Git or public static files.
- Current nine-entry editorial reel in `Fountain-Coach/estate/navigation/canonical-reel.v1.json` includes Book and separately selected Solstice but **not Works or Status**. Status is a legal/supporting footer destination. Existing live Status still has an older header snapshot with Status in its reel; the source owner's later unpublished legal/footer normalization is preserved rather than falsely claimed as deployed.
- Visibility is tri-state: featured-public, discreet-public, private-controlled. Off-reel and noindex never imply actual confidentiality, authorization, anonymity or absence of hosting network metadata.

## Source and production-first lineage

The original Status public snapshot is tagged `status-public-snapshot-20261014`; initial published inventory was 25 files and 12 HTML routes. The current authoring edition has 26 files, 13 HTML routes and passed `scripts/verify_publication.py` exact source SHA-256 inventory check. The public Status production `/`, `/transparency/` and `/assets/status.css` were independently verified against their original pinned snapshot Git blobs just before staging; these three exact payload digests matched, meaning the affected public baseline was preserved. The public site was not modified.

The **only existing canonical WLAN staging** is Ubuntu MacMiniDocker under `/home/benedikt/estate-shell-acceptance-staging/`, preview service on port `8200`. Its previously verified active release was `shared-shell-20261024-v25-works-folio-reader-8375106`. The v26 immutable copy, `shared-shell-20261024-v26-discreet-references-876b613`, retained all **940** predecessor files byte-for-byte, introduced **26** new `status/` files including 13 HTML pages, with a bounded WLAN prefix transformation of source absolute links to `/status/`. Only `source-lock.json` was additionally updated to witness the exact owner and stage lineage. Other Book, Works, Instruments and estate release bytes were preserved; v25 remains rollback.

Activation used the existing authenticated SSH, rsync, SHA-256 preflight, atomic `current` symlink and restart of the unchanged `fountain-shell-acceptance-preview.service`. No new DNS entry, runtime, private-document host, login gate, CI pipeline or EstatePublisher security ceremony was invented. This is independent static staging/readback, **not a typed EstatePublisher WLAN stage receipt**.

## HTTP and browser acceptance

Live `http://192.168.8.50:8200/status/references/` returned HTTP 200 with SHA-256 `a89283259ea81afcf99c59d1f747760a1c801f4f01491792dcec09eaa5207434`, identical to pre-activation candidate. `/status/transparency/`, `/status/`, `/status/company/`, `/status/assets/status.css`, `/book/` and `/works/books/` all returned 200. Staging served `Cache-Control: no-store, max-age=0` and `X-Robots-Tag: noindex, nofollow`.

Chromium readback at 1280x900 and 393x852 navigated `/status/transparency/` → `/status/references/` via real ordinary link, then `/status/` via return link. Both widths had no horizontal overflow; the destination had no scripts/iframes/cookies/linked PDFs and loaded only its one same-origin HTML request, no external resources. Browser title, breadcrumbs/return, no-referrer and noindex metatags were observed. Screenshots retained privately in the Mac scratch directory `.status-reference-stage-20261024/`, not deployed. Native Safari/iPad and reverse proxy log policy were not audited and no zero-logging guarantee is made.

**Sensitive-data boundary:** zero Jobcenter, legal-case or identifiable administrative documents were uploaded, committed to public source or published. A later recipient-specific sanitized document needs explicit author selection, redaction review and independent delivery/publication approval; a privately shared original remains in private storage.

## Release status

Status, Book and Works public production unchanged. v26 is only private WLAN staging. Public promotion, access/logging guarantees and case-specific document release require separate authority.
