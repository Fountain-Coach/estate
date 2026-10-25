# FCIS Chapter 158 — public EstateShell repair candidate

**22 October 2026 · source-owner branch only · NOT PUBLISHED**

The actual issue is the *public* masthead/reel/footer mismatch. Governance still has eight editorial items, while other public owners retain Status as a top-reel item. Passing the former Estate/Teatro/First Reading WLAN proof did not certify the entire public estate.

Fountain Press Linotype owns books and bookshelf composition; the versioned `Fountain-Coach/estate` EstateShell owns masthead, nine-identity editorial reel and the four legal-footer slots; EstatePublisher alone owns publication effects. This change does not introduce a fourth CMS, staging server or server-side helper.

## Changes in this branch

- `scripts/project_public_estate_shell.py`: a source-faithful public-candidate adapter using the **existing** `estate_shell.project`. Normalizes Governance's `header.topbar` and ordinary `header.site-header`, avoids duplicate mastheads, removes only the *generated* staging noindex instruction, and retains original owner legal/source material within shared footer provenance. Original intentionally private/noindex sources are refused.
- One nine-identity reel in the contract order `estate, book, governance, midi2, instruments, teatro, satzfunk, pointer, solstice`; Info jumps to the one footer. Status stays exclusively in the legal footer.
- Unpublished Satzfunk remains visibly identified but inert: `aria-disabled=true`, a pinned intended canonical identity, **no broken public or private WLAN href**, and no private audiovisual archive bytes.
- `scripts/build_public_estate_candidate.py`: pure deterministic candidate assembly from the owner's complete SHA-256 file inventory and pinned 40-character Git source revision. Refuses unlisted, changed, secret, or symlinked files; verifies declared routes; copies untouched assets; emits a receipt with `publicReleased=false`. No network or deployment effects.
- `scripts/check_public_estate_shell.py`: reject partial public coverage. Requires all eight admitted public editorial owners and every Governance HTML route, matching CSS/logo bytes, nine identities, correct active state, complete four-slot footer and no bad private links. Success is **structural-only**, never Safari or terminal publication.

## Reproducible tests

From a normal checkout with BeautifulSoup available:

```sh
python3 scripts/test_public_estate_pipeline.py
```

11 synthetic tests were exercised in a separate local workspace and passed; 24 additional adapter/gate/builder checks passed. These are **not** claims that all actual public owners have passed. A complete public production build and native WebKit witness were not possible from the present connected runtime.

Governance's known Git owner revision was `03f15306a018eddd85fab491e592d2fdffd61528` at this audit. To create its candidate without publishing:

```sh
python3 scripts/build_public_estate_candidate.py \
  --site ../governance.fountain.coach/site \
  --source-manifest ../governance.fountain.coach/publication-files.sha256 \
  --source-revision 03f15306a018eddd85fab491e592d2fdffd61528 \
  --identity governance \
  --reel navigation/canonical-reel.v1.json \
  --route-manifest ../governance.fountain.coach/site/route-manifest.json \
  --out /absolute/path/new-governance-candidate \
  --receipt /absolute/path/new-governance-candidate-receipt.json
```

**Do not assume Governance Git main is identical to production.** The prior independent 294-file readback found two real Git-to-live differences at `index.html` and Chapter 7, reflecting newer FCIS material not yet present in the retained October 20 production release. Source/editor approval must determine whether those changes are part of the next authored edition; do not smuggle them into a chrome-only repair.

## Live eight-domain source variants and browser-state correction

The 22 October independent public HTML inspection found:
- Estate, Book, Teatro and Pointer use `header.site-header`.
- Governance and MIDI2 use `header.topbar`.
- Instruments uses `header[role=banner]` without `.site-header` or `.topbar`, and has an unrelated `header.catalog-heading` inside its own content. The adapter selects the publisher header by the canonical reel; it never removes the source-owned catalogue heading.
- Solstice uses `footer.solstice-footer#footer`, not `footer.footer#footer`. The adapter retains its original imprint and removes the old root footer before inserting the one common footer.

The pure builder now names its three **same-origin** shared assets with their SHA-256 digests (16 hex characters): `estate-shell-<digest>.css`, `estate-shell-state-<digest>.js` and `estate-shell-logo-<digest>.png`. The output HTML refers to those exact byte-named files. Safari can keep ordinary history/cache state: a changed shared component has a different URL, rather than silently reusing the previous release's styling.

The per-owner source revisions, immutable production predecessor, complete content inventory, browser screenshots, authorized publication and independent HTTPS receipts remain distinct from these source-level improvements.

## Remaining public gates

1. Build and review actual source-locked owner candidates for all eight domains and every Governance chapter, including historical routes outside the ordinary route manifest.
2. Run the structural public gate on those real outputs, not synthetic fixtures; ensure editorial work, media, CSP, status/legal links and source-digest receipt remain intact.
3. Test all same-size common chrome surfaces and deep routes in browser and native iPad Safari, including Info/footer/back and book/page/Teatro interactions; verify protected Satzfunk archive is still inaccessible anonymously.
4. Invoke the authorized typed EstatePublisher public release lane on exact approved hosts. Keep predecessor, conduct independent DNS/TLS/HTTPS readback and terminal receipt **for every affected site**, and rollback on a failed gate.

**Current state:** source candidate in Git. The public Governance Caddy release remains `static-20261020-923d5f9` until a properly authorized and independently witnessed release occurs. No public host or URL was changed in this operation.

See [public Governance failure evidence](2026-10-22-public-governance-reel-failure.md) and [Linotype Estate Template contract](https://github.com/Fountain-Coach/estate/blob/main/navigation/canonical-reel.v1.json).
