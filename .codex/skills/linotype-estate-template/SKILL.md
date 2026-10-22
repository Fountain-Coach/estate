---
name: linotype-estate-template
description: Audit, specify, build and verify Fountain Coach Linotype readers, Bookshelf state, the cross-domain EstateShell masthead/reel/footer and EstatePublisher acceptance. Use for site templates, CMS-like Linotype composition, inconsistently styled navigation or footers, source-to-live drift, responsive publication state, and multisite staging or publishing.
---

# Linotype Estate Template

**Separate the owners first.** Fountain Press owns measured Linotype book/Bookshelf composition; `Fountain-Coach/estate` owns the cross-domain shared shell contract; source owners retain their work; EstatePublisher owns governed publication and full evidence. A common set of navigation links does **not** make common rendered header/footer components.

## Always inspect

1. The real currently published site (root and deep routes), owner Git revision and local WLAN candidate independently. Never casually replace the public site with a newer unpublished owner `main`.
2. [Exact template and ownership definition](../../../docs/architecture/linotype-cms-like-template-v1.md). Cross-check Fountain Press `runtime/linotype-engine.js`, `book.js`, `book.css`, `bookshelf.py`, `reading-layout-policy.js` and publication-identity decision.
3. [Canonical estate reel](../../../navigation/canonical-reel.v1.json), legal/footer policy and actual on-iPad screenshots. Preserve one author-approved shell version for masthead, same nine-domain reel+Info, and identical legal footer structure. Status stays **footer-only**.
4. The existing Mac EstatePublisher tests: `testEstatePreviewScenarioIsWholeProductTemplateReproduction` checks scenario declarations, `estate.visual-mirror.compare` validates inputs, and neither alone proves live WebKit/CSS parity. Require a true cross-domain browser transition report.
5. Each domain's real body: Teatro Stage remains a tool, Satzfunk remains its original audiovisual archive, Solstice is writer-owned Linotype First Reading, and governance/other domains retain full authorship and rights. Do not manufacture books from tools, compilations or sound recordings.

## Two distinct publication lanes

**Reframe publishes an admitted work or edition *into its Bookshelf*.** Reframe owns the writer's source, the authorial permission to admit a work or edition, Bookshelf membership and containing-space relationships; FountainStore maintains source identity/revision and editorial/reading continuity. Fountain Press owns the genuine Bookshelf presentation and measured Linotype book pages; it neither invents membership nor writes the manuscript. `Bookshelf-admitted` does **not** mean `publicly released`.

**EstatePublisher publishes an authorized website/edition *onto the public estate*.** This is a separate release transaction requiring admitted public rights, exact host/route, publication receipt, DNS/TLS and independently observed HTTPS outcomes. Adding or changing a Reframe Bookshelf tile **does not create a new hostname, reel entry, or public deployment**. A private Reframe book may remain private indefinitely.

Inspect Reframe [R22 source/Bookshelf identity](https://github.com/Fountain-Coach/Reframe/blob/main/scenarios/022-git-authored-literary-estate-bookshelf.md), [R26 Empty and first writing act](https://github.com/Fountain-Coach/Reframe/blob/main/scenarios/026-empty-bookshelf-first-writing-act.md), and [Fountain Press composition owner boundary](https://github.com/Fountain-Coach/fountain-press/blob/main/docs/reframe-composition-owner-boundary.md) before implementing either lane. Distinguish **source known → Bookshelf member/admitted work → Press-composed readable edition → optional approved public release**, each with separate evidence. A selectable Empty slot is an authoring position, **not a published book**. Reject forged source/cover identity, inferred rights, nonadmitted corpus membership and premature public links.

## Implement and prove

- **Template:** single versioned site shell with one masthead, one accessible nav reel, and one typed, four-region legal/provenance footer. Each domain consumes the same structure/styles and contributes only typed identity, copyright/source credits, authorized destinations and release state. Local design themes apply to the body, not unversioned variations of common chrome.
- **Linotype:** use Press only for admitted source-bound book, real edition/collection, reader pages and measured gestures. A page number is not durable source identity. Never copy manuscripts into a shell or duplicate the compositor in Reframe.
- **Evidence:** source/DOM invariants, responsive computed styles, screenshot parity from actual WebKit/iPad and desktop, navigation/Info/footer/Back/keyboard/focus, CSP, negative drift tests, rights, receipts and replay. Don't call a passing navigation-inventory test a visual proof.
- **Release:** WLAN trial is reversible and private; do not expose archived Satzfunk media/translation or credentials. For public production, invoke the current EstatePublisher typed resolver, strict admission, exact route authority, receipt, independent HTTPS/DNS/TLS verification and rollback. No ad hoc SSH as production publisher, no GitHub CI.

## Implementation assignment and failure criterion

Read [the complete EstatePublisher implementation prompt](../../../prompts/linotype-estate-shell-acceptance.md). **Failure**: Fountain Coach, Teatro and Satzfunk still have different masthead/reel/footer geometry, markup hierarchy or legal/footer treatment in same-viewport actual iPad screenshots, even if the nine links are identical.

Report separately which evidence was source-reviewed, simulated/staged, visually accepted and publicly released; do not invent a final deployment receipt.
