# Fountain Coach estate template: bounded composition and acceptance reference

**Reconciled procedural note - 23 October 2026.** The 22 October proposal used "single EstateShell renderer" language. This reference now distinguishes the accepted direct-static Fountain Coach Publication Core described in Governance Chapter 127 from earlier unadmitted implementation proposals. Reconcile the *current adopted* source at execution; neither this document nor the example JSON is normative on its own. Read [FCIS authority reconciliation](fcis-authority-and-reconciliation.md) before acting.

## 1. Five ownership seams

| Layer | Owner | Valid effect / claim | Never implies |
| --- | --- | --- | --- |
| Authored work/edition | Git source owner; writer/Reframe for admission | Original text, revision/hash, edition, cover/rights intent | Measured page, public DNS, publication grant |
| Bookshelf membership and durable evidence | Reframe plus FountainStore | Admitted work/edition in containing shelf, writer authorization, reading/source records | Website release, new reel icon |
| Measured document composition | `Fountain-Coach/fountain-press` (Linotype) | Source-faithful pages/folio, responsive book, Contents, covers, return | Global estate header/footer, Store admission, release |
| Web authoring / publication | Fountain Coach Publication Core, domain Git source, FountainStore, EstatePublisher | Direct-static authored complete route; admitted immutable artifact and typed publication receipt | A new CMS or site generator, proof by Git push |
| Deployed browser observation | Native WebKit/AX, deployed HTTPS and Chapter 128 mirror | Route-scoped read-only comparison and witnessed visual state | Mutating release or author source |

Page content is owned by its domain. Teatro stage, Satzfunk audiovisual archive, Solstice book and Governance chapters need not look like each other. Shared publication chrome is a common *approved authoring contract* and must not erase editorial independence.

## 2. Direct-static route contract (Chapter 127)

For a website change, inspect the actual Fountain Coach Publication Core and checked-in owner route. The admitted output is complete human-inspectable HTML and referenced CSS, JavaScript and assets. It renders without content hydration, an intermediate site compiler, remote runtime wrapper, or rebuilding shell/source at request time. Authoring-time tools may compose static files; that does not make their editor or an additional template runtime the publication authority. Reframe Semantic Browser mirrors existing route bytes. FountainStore stores candidate/route/provenance/receipt. EstatePublisher is the one publication authority.

Maintain current approved shared visual elements: publisher identity, accessible masthead, canonical edition reel, focus/active/Info semantics, coherent footer legal/provenance/Status, responsive safe areas, and typed publication state where supported. Preserve owner-specific copyright, verified authorship, translators/credits and accessibility. Source rights and technical correctness are separate gates.

Do not assume that the nine-item `navigation/canonical-reel.v1.json` snapshot is eternally the live public set. Check its revision and current adopted route/rights policy first. The 22 October sample contained an *intended* `satzfunk.fountain.coach` destination that was not publicly resolvable in a later check. Private WLAN and public rights are different states. An unresolved hostname is not an approved public route merely because it appears in a fixture.

One shared versioned contract is different from one injected global renderer. Compare actual emitted HTML/CSS/JS and exact committed authoring source. Use `data-*` version labels only if the adopted release actually defines them; a missing label from an older *proposal* is not automatically a runtime defect. The full route and its media must remain usable without Reframe running.

## 3. Linotype composition boundary

Linotype is a **source-bound measured document compositor**, not the global shell. Confirm current `runtime/linotype-engine.js`, `book.js`, `book.css`, `reading-layout-policy.js`, `mobile-page-navigation.js` and `bookshelf.py` in `Fountain-Coach/fountain-press` before changing implementation details. Historic 22 October reader implementation used `#book-flow`, `#book-viewport`, `#book-pages`, `window.SolsticeLinotype`, a fixed measured leaf and source-preserving semantic HTML. Its portrait/landscape decision used actual geometry, not browser name, and page breaks are projections rather than durable source addresses.

A work/edition/source digest and semantic passage identity persist; a folio/page index does not. Covers and thumbnails must remain source-owned. Empty is a selectable inert potential, not a fabricated book or counted publication. Do not manufacture a book around a Teatro tool, private recording, score or unpublished text. When admitted, prove cover-to-reader and return/reopen on the same source revision; preserve author's text, style and media order.

Historical reader paper tokens (`--book-paper`, serif fonts) belong to the Press reader, not the common estate chrome. Do not force Teatro Stage, Satzfunk archive or public Governance body into a book-paper aesthetic to make them visually uniform.

## 4. Development/source, staging and publication are also distinct

Git is the development authority and does not require a DNS-based `dev` environment. A local Store-backed preview of that Git revision remains local. The registered Ubuntu Mac mini is the canonical private staging executor and public HTTPS is a separate production observation. The user's explicit production-first requirement means a **canonical development-to-staging transition** must first independently capture production into an immutable, nonactive staging baseline, apply only a pinned Git delta, refuse undeclared loss and require native publisher enforcement plus staging readback. This does not mean temporarily replacing the live stage with bare production. See [development / staging / production](development-staging-production.md). A source owner/rights decision remains separate from a production byte observation.

## 5. Distinct publication states

1. Source candidate: identified authentic owner/revision, not admitted by discovery alone.
2. Reframe Bookshelf member: explicit writer/editorial admission and FountainStore membership; not publicly released.
3. Press readable edition: authentic measured projection of that source and a supported reading/return path.
4. Local estate draft preview/check-in: Chapter 147's existing `estate.preview.draft-refresh` and `estate.preview.draft-check-in` with exact displayed digest; still local.
5. Public estate release: separate rights and publisher approval, immutable built artifact, typed EstatePublisher promotion/rollback, Store receipt and independent public HTTPS/DNS/TLS readback.

Do not collapse these states. One estate publication state under Chapter 145 does not make Reframe or a browser a second publisher. A logo signal or HTTP 200 never certifies Store synchronization.

## 6. Accept the goal, not an invented harness

Start by defining the requested observable outcome. For a mere viewing task, verify the registered staging URL and provide it; no new browser matrix required. For a reported reel/footer defect, compare the affected transitions on the accepted release/version and only relevant viewports. For a full cross-domain visual-parity request, use the already-admitted WebKit mirror/native browser capability and capture both semantic DOM/AX plus settled screenshot facts at declared profiles; include deep routes and relevant content interactions. Evidence must refer to the same route, source revision and shell contract. If no executor exists, describe that gap as PROPOSED unless it demonstrably blocks the user goal.

`scripts/check_shell_snapshot.py` accepts a deliberately supplied static schema and HTML files. It can reject missing expected links/order/version labels of *that schema*. It does not prove adopted contract status, visual parity, legal rights, accessible interactions, WebKit behavior, Store authorization or production. The bundled `contract.example.json` is a historical **fixture only** and must never be used as the authoritative public manifest. A mismatch between public Governance HTML and an unadopted fixture is not by itself a site failure.

When release is in scope, honor Chapter 148: build/test/sign/digest away from production; production runtime verifies/activates/serves/rolls back a prebuilt immutable artifact. Recheck exact source and host/routes; never rebuild source on a Hetzner runtime. No Github CI requirement is introduced.

## 7. Source pointers (verify freshness)

- Goal fidelity: `Fountain-Coach/.github/docs/FCIS-Non-Invention-and-Goal-Fidelity.md`.
- Governance: `https://governance.fountain.coach/`; sources under `Fountain-Coach/governance.fountain.coach` and relevant reviewed FCIS chapters.
- Canonical estate: `Fountain-Coach/estate/AGENTS.md`, `navigation/canonical-reel.v1.json`, `staging/environment.json`.
- Publishing contracts: `Fountain-Coach/midi2-gpu-fabric/apps/estate-publisher`, `.codex/skills/estate-publisher-deployment`; FountainStore-owned Chapter 127 Publication Core.
- Composition: `Fountain-Coach/fountain-press` and its Reframe boundary docs; Reframe R17/R22/R24/R26 for Bookshelf.

Record precise commit and published status for every cited decision. Do not quietly treat an old snapshot, local branch or skill ZIP as the owner of a new capability.
