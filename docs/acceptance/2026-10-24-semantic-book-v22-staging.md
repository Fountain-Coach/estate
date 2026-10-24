# The Book of Reframe — v22 semantic staging acceptance

Date: 24 October 2026. Scope: the canonical owner-WLAN staging Book route at http://192.168.8.50:8200/book/. Public production unchanged.

## Decision and source authorities

The user requested a semantic update of the more complex book.fountain.coach domain, following the new Instruments semantics and its preference for recognizable symbols over invented branding.

- Editorial owner: Fountain-Coach/book-of-reframe, revision 7737c9b59d6cddb86e8bf44c84f94d73e6938c7f.
- Current public Book release: estate-20261024-v14-satzfunk-reel-book, from the original Hetzner static server.
- Source publication law: book-of-reframe/AGENTS.md and PUBLICATION-POLICY.md. Public Book explains reviewed development, not private runtime execution, author's admitted Reframe Bookshelf, manuscript rights or App release.
- Source gate: book-of-reframe/scripts/build-publication-manifest.py --check passed, leaving the exact August 15 published numerical snapshot claims and empty App release allow-list unchanged.
- Visual identity: existing Lucide book-open glyph v0.468.0 (ISC, locally licensed), with typographic 1200x630 social image. Neither is represented as an admitted manuscript's edition cover.

## Real production-first reconciliation

Before transforming staging, the production and v21 staging Book homepage main text were independently normalized and found **exactly identical**, SHA-256 prefix 2e689d5363afd66f. The Git source homepage has separately evolved writer-facing content (different normalized main), and was *not* silently substituted as a production baseline.

The v22 staged Book entrance is the verified stage/public Book baseline with a declared, source-owned Git semantic homepage/CSS/art delta. The current checked Git record sections (scope, evidence, governance) are retained in the appendix without inventing new acceptance values. All 21 independently pinned public production deep HTML routes were restored into staging from the unchanged public release, which previously had only the Book homepage and six assets. This includes scenario-driven-development, scenarios, commands/commands and the public Csound Teatro route. The latter is deployed public content but is absent in the current book-of-reframe Git site tree; do not mistake the live route for evidence that latest main controls its underlying article.

### Staging state and preservation

- Existing registered staging: Fountain-Coach/estate/staging/environment.json; MacMiniDocker Ubuntu WLAN server with existing fountain-shell-acceptance-preview.service at port 8200.
- Immutable predecessor: shared-shell-20261024-v21-standard-icons-5ac718e.
- Active v22 release: shared-shell-20261024-v22-semantic-book-7737c9b.
- Prior 719 files kept; only book/index.html and book/assets/site.css changed, plus source-lock.json recording the exact delta; 24 new files (21 published deep HTML routes and three author-sourced icon/social assets). Other estate pages, shared masthead, reel, footer and assets preserved.
- Authenticated existing SSH, rsync, SHA256 inventory checks and an atomic current symlink; the existing preview service was restarted because it pins current at process startup. No new service, DNS, GitHub CI, extra store, or public publication.
- The activation used this proven SSH static path, not a native typed EstatePublisher WLAN stage receipt. That receipt must not be claimed.

## Independent readback

- /book/ HTTP 200, SHA256 cc6f10b1e9d02f3af81f7c3969261380f597673c87a6a0dc67d5ae0b2c315fed
- /book/assets/site.css HTTP 200, SHA256 dab8f595cdfdea971dc7660b41f080d996f55657ad379e0324603b054a0404b3
- /book/assets/book-open.svg HTTP 200, image/svg+xml
- /book/assets/book-reframe-social.png HTTP 200, PNG 1200x630; SHA256 d2aacae876b59a9af6ba0ec362d2186811afbd87f1d21d2f7c662e051f5b64b4
- /book/scenario-driven-development/ HTTP 200
- /book/scenarios/ HTTP 200
- /book/commands/commands/ HTTP 200
- /book/csound-teatro/ HTTP 200
- /book/privacy/ HTTP 200
- /book/governance/default-semantic-manuscript-projection/ HTTP 200
- Headers: Cache-Control no-store, X-Robots-Tag noindex,nofollow
- Public book.fountain.coach/current symlink remained estate-20261024-v14-satzfunk-reel-book.

Independent local Chromium read-only browser inspection at 1280x900 and 393x852: HTTP 200, one main title, all four table-of-contents URLs internally resolved to the WLAN stage, the open-book SVG loaded, no horizontal overflow, no JS page errors, and a click into the method chapter loaded the actual local /book/scenario-driven-development/ route. The nine-member common reel was present. Two full-page PNG screenshots retained privately in the Mac working directory .semantic-book-stage-20261024 as local visual evidence, not promoted to the public estate.

No physical Safari/iPad acceptance and no public release authorization are claimed.
