# Fountain Coach Shared EstateShell — WLAN acceptance checkpoint
**22 October 2026 · implementation branch `feature/shared-shell-acceptance-20261022`**

## Current scope and admission
This is a **source-owned, reversible local shell prototype**, not a remote publication receipt. The public Fountain Coach, Teatro and First Reading pages were independently read over HTTPS and their owned content kept intact while rendering one versioned common masthead, reel and four-region footer. Reframe's Bookshelf admission remains separate from EstatePublisher domain deployment.

**Live WLAN inspection:** http://192.168.8.50:8202/estate/ (on local author network only). Other staged editorial routes: `/teatro/` and `/solstice/editions/first-reading/`. The authentic private Satzfunk station remains `http://192.168.8.50:8194/`, not copied into this release; anonymous requests continue to return HTTP 403.

**Installed service:** `fountain-estate-shared-shell-proof.service` on the Ubuntu Mac mini, binding only `192.168.8.50:8202`. Immutable release: `/home/benedikt/estate-shared-shell-proof/releases/20261022-v5/`; current is a symlink. No production DNS, Caddy or public Store state was changed. No private media, manuscripts, credentials or 7VST translated source were copied.

## Distinct identity levels
The three primary editorial entrances from earlier AGENTS constraints (Fountain Coach, First Reading, Teatro) do **not** imply only three estate destinations. The nine-item cross-domain reel is an independent navigation level; `Status` remains a **footer-only** transparency destination. Satzfunk is its own author audiovisual radio and, on WLAN, resolves to the authentic protected original archive. The reel is not a Reframe Bookshelf; Bookshelf membership does not register a hostname or permit public release.

## Tested implementation
- One source-owned renderer: `scripts/estate_shell.py` and one versioned CSS under `shell/`, using the **actual published Fountain Coach logo** and a same-origin Content Security Policy-safe active-state adapter.
- Three published roots mirrored with the real original CSS/JS/images; `scripts/build_shared_shell_preview.py` emits per-owner content SHA-256, source-lock and asset provenance. Solstice retains its own book pagination and original owner-supplied WebKit-compatible assets. Teatro's original Stage WebGL view is present.
- `scripts/check_shared_shell_release.py` is an executable **fail-closed** structural preflight. It does not accept arbitrary unsigned JSON as a native EstatePublisher approval or screenshot witness. Website publication mode stays blocked until the native executor has independently admitted the actual WebKit and public deployment receipts.
- Local branch `scripts/test_shared_shell_acceptance.py`: **15/15 PASS**, including deliberate failures for missing/incorrect reel items, Status wrongly inserted at top, inconsistent footer slots and version, wrong active identity, CSS/logo drift, and unauthorised public release.
- Structural preflight against the three actual captured editorial pages: **3/3 PASS** with exactly one common reel and footer. Source-owned body retained; full public-source asset capture reports zero missing assets.
- Mac Chromium browser regression at four viewports × three pages (12 observations) confirms matching measured masthead and reel geometry and equal shared footer geometry after the style isolation fix; the previously observed false-positive “link background mismatch” is **expected**, because Estate marks Estate active while other domains do not.
- A real local browser journey **Estate → Teatro → First Reading → Estate** succeeded. All show nine editorial targets and their own active state; the book retains Contents, previous/next controls and pagination; Info targets the footer.
- Anonymous `http://192.168.8.50:8194/`: **403 Forbidden**, as required.

## Open failures / honest boundary
- The First Reading owner's **phone-size book toolbar** still causes ~8 pixels of document horizontal overflow at 390px. This originates in `.book-tools` beyond the viewport, not from the common shell. Do not fix Press-owned reading gestures by manipulating shared shell styles; route to Press as a separate source-owner acceptance issue.
- Browser witness is **Chromium on authorized macOS**, not a native iPad Safari/WebKit capture. An iPad Safari author acceptance and independent screenshots remain open.
- The nine domain destinations exist in the navigation manifest, but **only three true published-site body projections** are integrated in this bounded release. No claim of nine-domain full parity. Other owner root/deep routes and Satzfunk's common shell remain separate admission steps.
- Existing public HTTPS pages remain unchanged. No new `satzfunk.fountain.coach` public host, author rights clearance, publication-authority operation, signed receipt or independent public readback is claimed.
- The isolated runnable prototype and the structural check are **not yet integrated as a typed native EstatePublisher production operation**. A published domain release must fail until independent native verification is available.

## Reproduction and rollback
Run locally with Python and BeautifulSoup:
```
python3 scripts/test_shared_shell_acceptance.py
python3 scripts/build_shared_shell_preview.py --out <new-empty-staging-release>
python3 scripts/check_shared_shell_release.py --mode structural --manifest navigation/canonical-reel.v1.json --site estate=<estate.html> --site teatro=<teatro.html> --site solstice=<solstice.html> --css ... --logo ...
```
The release is versioned under `releases/20261022-v5`. To roll back the local proof, stop or disable **only** `fountain-estate-shared-shell-proof.service` and restore the prior preview pointer; never touch any production service or the original Satzfunk archive. No GitHub CI.

**Definition of Done for production is still OPEN.** Structural and desktop-browser work is meaningful evidence; native WebKit, deep-route parity, full site-owner integration, rights and EstatePublisher approval are necessary before publishing.
