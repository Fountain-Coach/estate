# Conditional remediation playbook - shared estate chrome and Linotype

**Procedural guide, revised 23 October 2026.** Use this only after the user's task genuinely requires a source, shell, reader, or publication change. It is NOT a standing order to build infrastructure, a universal cross-domain test service, a new renderer, or a new EstatePublisher gate. Consult [FCIS reconciliation](fcis-authority-and-reconciliation.md), the [Invented-Prerequisite Loop](invented-prerequisite-loop.md), the [development / staging / production contract](development-staging-production.md) for environment transitions, and the [template contract](template-contract.md) first.

## Decision record before any code change

Write four answers in the task record:

1. What observable result did the user request, and what finite evidence will establish it?
2. What exactly fails on the existing named route/device/owner revision? Provide an observed result, not only a screenshot interpretation or hypothetical test gap.
3. Why can the existing Publisher/Store/Press/static projection not satisfy that result after the smallest reasonable reuse/configuration?
4. What minimal owner-scoped correction and nearest same-path acceptance will repair it?

If answers 2 or 3 are absent, the proposed mechanism is non-blocking. Do not transform the requested fix into a broader system overhaul.

## Existing owners to inspect (only when relevant)

- Estate registry: `Fountain-Coach/estate/AGENTS.md`, `staging/environment.json`, declared navigation/route revision, actual running WLAN `current` identity.
- Static authoring: current checked-in owner route and Fountain Coach Publication Core (Governance Chapter 127); not a generated runtime wrapper.
- Fountain Press: real Bookshelf and measured-reader modules and tests; preserve source and existing reading position.
- Reframe/FountainStore: writer consent, admitted work identity, containing shelf, current typed Store facts and relevant R17/R22/R24/R26 scenarios.
- EstatePublisher: `apps/estate-publisher` current operation catalog, preview refresh/check-in, `estate.visual-mirror.compare`, `estate.publication.sync`, resolved approval and strict inspections. Reuse existing operations before proposing additions.
- Browser: actual target WebKit/Safari and deep routes, source and release SHA, AX and settled visual witness when the reported defect is visual.

## Bounded action by problem

### A. Viewing or inspecting staging

Read the canonical stage registry and verify the actual running lease/service/route. Return a direct copyable URL. Do not build, install, alter source, launch more preview servers, demand production credentials or claim production publication.

### B. Shared navigation/header/footer discrepancy

Observe the exact affected domain transition and current accepted contract. Compare the existing direct-static authored HTML/CSS/JS, icon vectors, assets, active/Info behavior and legal/provenance slots. Fix at the *owning source* and rerun the smallest existing affected-route test. Same nav labels alone never establish visual parity; a discrepant historic proposed `data-*` version label alone never proves a defect. Preserve body content and rights.

If the request explicitly covers whole-estate parity, broaden to the declared routes and profiles, using existing WebKit/AX/visual mirror evidence and a correlated transition report. A new `estate.shared-shell.cross-domain-acceptance` operation is NOT automatically required. Propose one only on a proved missing executor seam, after checking the existing preview/visual mirror and typed Kit contract.

### C. Bookshelf or Linotype defect

Prove candidate vs admitted work, writer authorization, exact source digest, cover identity, measured reader and return/reopen. Resolve it within Press or Reframe/FountainStore; never create a fourth CMS, public site, navigation identity, fake cover, or authored text from an Empty slot.

### D. Author-controlled local preview/change

For admitted route work, use existing Chapter 147 `estate.preview.draft-refresh` for disposable preview and `estate.preview.draft-check-in` for explicit digest-bound local candidate. Keep preview, durable candidate and public release distinct. Do not invent CRUD APIs or a second source database.

### E. Canonical Git development → WLAN staging transition

Use [development / staging / production](development-staging-production.md) for the author-selected Git-to-canonical-staging transition. Production is observed public reality, not a Git branch; reuse a trustworthy immutable production baseline for the selected scope. Apply the pinned authored Git delta to a nonactive candidate and preserve other routes/assets and accepted stage-specific transformations. Verify production and staging predecessors before the existing EstatePublisher SSH delivery operation and independently read back the result. A staging predecessor check alone does not establish production lineage. If native lineage checking is absent, **do not claim guaranteed production-first promotion**; identify the smallest correction in the existing delivery client. Do not turn that missing enhancement into a block on unrelated, previously authorized SSH publication, and do not demand new host agents, restricted accounts, signature enrollment or production Store synchronization as a speculative fix.

### F. Public production publication

Verify approved source/rights/host/route and exact immutable artifact digest. Run existing EstatePublisher resolver, current authorized instrument and terminal receipt. Builders perform build/test/package away from production (Chapter 148); production verifies and atomically activates artifact only. Preserve rollback and independently verify selected public HTTPS routes, source credits, Store and TLS/DNS as applicable. Never turn stage success, remote SSH transfer, process start or Git push into a publication claim.

## Evidence report

Use these separate lines in the final work record: SOURCE (owner + SHA); CONTRACT (version, applicability, published or draft); OBSERVED FAILURE; CHANGE (or none); UNIT/STATIC (what the helper checks); WEBKIT/AX/PIXELS (if required); STAGING (host, current predecessor, production baseline/delta receipts, native enforcement status and resulting release); PUBLIC (receipt and independent readbacks, if requested); RESIDUAL (unproved vs proposed follow-up). Mark observed, proven, documented, inferred and proposed correctly. Stop once the originally agreed acceptance is met.
