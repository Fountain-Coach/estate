# What exactly is the Linotype (CMS-like) template?

**Owner-boundary and shared-shell specification · 22 October 2026 · architecture candidate**

## Not a CMS skin

Linotype is Fountain Press's *measured, source-bound book compositor*. Its input is an admitted, versioned work/edition. It outputs a measured reader, accessible original HTML fallback, contents, responsive leaves and book transitions. Its **Bookshelf** is a presentation state of that same composition system; books have source-owned identity, cover, reader path, revision and release status. It is **not** a dynamic CMS, shared navigation implementation, authoring database, audio host, or deployment manager.

The “CMS-like template” is actually **five independently owned components**:

| Layer | Authoritative owner | Contract |
| --- | --- | --- |
| Authored source/identity/rights | Independent Git owner, Reframe for writer/editorial acts | Source revision, work/edition/collection IDs, credits, passage IDs, licensed media |
| **Linotype composition** | [Fountain Press](https://github.com/Fountain-Coach/fountain-press) | `runtime/linotype-engine.js`, `book.js`, `book.css`, `reading-layout-policy.js`, `mobile-page-navigation.js`, `bookshelf.py`, `bookshelf.css` |
| **Shared EstateShell** (currently incomplete) | This estate contract, consumed by each domain owner | One identical masthead, navigation reel, Info behavior, semantic/visual legal footer and versioned CSS at every route |
| Edition-specific experience | Each domain (Satzfunk, Teatro, Solstice etc.) | Genuine authored sound/media, work, stage, book or governance chapters, without identity coercion |
| Publication | FountainStore + EstatePublisher and Git owner | Rights/admission, typed plan, rollback, exact DNS/TLS/HTTPS receipts and independent readback |

The term *template* must **not** collapse these into a single HTML file or a new ungoverned site generator. The shared shell can surround a real Linotype book or something deliberately **not** a book, such as the original Satzfunk audiovisual radio or Teatro Stage Web.

## Source-inspected Linotype mechanics

- **Unmodified content:** `#book-flow` retains original full source; `window.SolsticeLinotype` measures and projects fixed-size leaves, preserving a no-JavaScript accessible HTML fallback. Folios are ephemeral; source passages/edition revision are durable.
- **Layout:** `reading-layout-policy.js` selects a facing spread only at `width >= 900`, `height >= 500`, `width/height >= 1.12` and leaf width `>= 380` with the measured gutter. Do not apply those rules to site masthead/footer or arbitrary video players.
- **Paper:** `book.css` defaults to book-paper `#f4f0e7`, outer `#ddd8cf`, ink `#26241f`; Iowan Old Style/Charter/Georgia. These are *reader*, not global chrome colors. Phone atlas is derived from composed leaves, not duplicate content.
- **Shelf:** `render_bookshelf()` accepts source-admitted books with id/title/author/edition/reader/source revision/cover/host/status, or distinct admitted structural spaces. Its six-column grid has twenty inert vacant cells, and a recognized publisher circle. `data-linotype-state="bookshelf"` describes this **specific state**. An audio source, Score or tool is not automatically a book.
- **Identity:** Publisher decision [Publication Identity and Cover Navigation](https://github.com/Fountain-Coach/fountain-press/blob/main/docs/publication-identity-and-cover-navigation.md) distinguishes work, edition, collection, cover, page, Score and tool. A cover is not an arbitrary link or first page.

## EstateShell — missing reproducible template

The author provided 22 October iPad screenshots showing **warm-light Satzfunk, dark Teatro and dark Fountain Coach with different mastheads/reel spacing and differently structured footers**. Equal reel IDs alone do **not** mean equal template rendering.

A single, versioned `EstateShell` must export:

1. **Masthead:** publisher/open-hand mark, estate identity and typed domain subtitle, fixed logo measurements, spacing, typography and accessible labels.
2. **Reel:** one semantic `nav`, nine editorial identities and Info. Reuse [the canonical manifest](../../navigation/canonical-reel.v1.json), but additionally own icon vectors, spacing, selection, contrast, keyboard focus and rendered geometry. **Status is footer-only.** On owner-only WLAN, Satzfunk opens the authentic protected archive; a public site must not link to private IPs or unresolved hosts.
3. **Work slot:** any genuine domain-owned experience, including Press book/Bookshelf, Teatro stage, Satzfunk historical player. Its body styling does not redefine the shell.
4. **Footer:** one semantic version and visual structure with four ordered typed regions: publisher/imprint; edition and source provenance; legal/privacy/accessibility/Status and applicable credits; truthful operational/release state. No duplicate independently maintained top-domain menu. Preserve extra legally mandatory copy inside its owner slot.

Publish `data-estate-shell-version`, `data-reel-contract` and `data-footer-contract` plus a component digest; every source owner consumes the same pinned renderer and CSS. Actual measured common chrome must be visually indistinguishable at the same viewport. Source-specific content may remain visually different. Do not relax Solstice Content Security Policy to repair navigation with inline scripts.

## EstatePublisher already has a template test, but the observed parity proof is missing

The Mac package `apps/estate-publisher` contains `testEstatePreviewScenarioIsWholeProductTemplateReproduction`. It asserts the `estate.preview` scenario's purpose, `same admitted shell order`, Safari/WebKit evidence, `shell-order-drift` negative predicate and `header/footer transition report` required evidence. Operation inventory includes `estate.visual-mirror.compare`; VisualMirror route input is validated. These are useful **contract tests**, **not actual whole-site visual equality evidence**.

**Required new EstatePublisher acceptance:** `estate.shared-shell.cross-domain-acceptance`. Compare exact pinned rendered root and deep routes for all owners; check one header/reel/footer version, all ordered targets/Info, active state, footer legal links, SVG paths, CSS computed geometry/typography/contrast, Safari/WebKit desktop + iPad portrait/landscape + phone snapshots, browser Back/focus/Info, no overlap with player or folio, rights/security gates. Negative controls: missing/reordered link; missing Status footer; Status in top reel; wrong active state; mismatched footer; light/dark token drift; CSP-blocked controls; private archive leak; unapproved remote publication. Block public promotion on any failure.

**Release evidence:** Git SHA/source digest, shell version, screenshot diff/transition report and actual browser witnesses, Store/typed EstatePublisher terminal receipt, exact DNS/TLS/HTTPS readbacks, and rollback. A localhost/Ubuntu HTTP 200, Git push, static manifest equality or one screenshot is insufficient.

## Implementation guidance

Use the [Linotype Estate Template Skill source](../../.codex/skills/linotype-estate-template/SKILL.md) and [reproducible implementation prompt](../../prompts/linotype-estate-shell-acceptance.md). The portable validated skill bundle and full reference contract have been provided separately to the author. No production mutation is authorized by this document.
