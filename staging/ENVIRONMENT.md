# Fountain Coach Estate — one named WLAN staging environment

## Current observed private stage — spatial color v65 (29 October 2026)

The existing owner-WLAN `http://192.168.8.50:8200/estate/` serves immutable `shared-shell-20261029-v65-reframe-color-8b4e961`, with `shared-shell-20261029-v64-reframe-app-ef6e193` retained for immediate rollback. **Root: neutral**; the verified source-owned `First Readings` collection is `/estate/collections/first-readings/`, its single contained work is `/estate/editions/essays/teatro-an-unfinished-composition/`. The collection manifest digest fixes the author-directed teal membership color, carried in DOM and accessible named landmarks and applied by original Fountain Press CSS only. New v65 differs from v64 solely in those two static HTML routes, two style assets and source lock; all art/source pages/other routes remain unchanged. Stage symlink, existing preview service, SHA readback, Press 15-test source witness and live Chrome 3/3 iPad-sized/mobile navigation+color checks are recorded in [v65 evidence](../docs/acceptance/2026-10-29-r28-semantic-color-v65.md). Physical iPad Safari/VoiceOver, matching historical native numeric token and public HTTPS release are **not accepted**.

Earlier v64, v63 and v62 sections below remain historical release/visual evidence; their `current` claims do not supersede the observed active v65 symlink.

## Current WLAN staging — Fountain Press immersive app surface (29 October, v64)

Current `/home/benedikt/estate-shell-acceptance-staging/current` resolves to immutable `shared-shell-20261029-v64-reframe-app-ef6e193` and the registered owner-WLAN endpoint is `http://192.168.8.50:8200/estate/`. Previous v63 remains rollback-ready. Fountain Press itself supplies `app_surface=True` and the complete responsive grid; the site's source builder selects that owner mode and the stage projection changes only the two byte-identical Press shelf entrances, First Readings shelf, and the owner Press CSS. No visible marketing header, "Bookshelf / Author" nav, text outside cover tiles or nine-site collection shell remains. Browser/AX/cover links passed at iPad landscape/portrait, phone and desktop; 14 Press tests passed. Supporting rights/links are accessible as nonvisual focus-revealed links. Exact route and source SHA: [R28 v64 evidence](../docs/acceptance/2026-10-29-r28-press-app-surface-v64.md). Full iPad Safari/VoiceOver and public two-host production are **not accepted**.

The v63/v62 records below are preserved as **historical predecessor observations**, not current stage status.

## Current Reader stage update — open hand returns to root (29 October 2026)

The actively serving **owner-WLAN Reader** is now immutable `shared-shell-20261029-v63-reframe-hand-29fb917` at `http://192.168.8.50:8200/estate/`; v62 remains rollback-ready. The original Fountain Press hand artwork is now an explicit named, keyboard-operable **Reader-root/Bookshelf link** on the root, First Readings collection, continuing Essays reader and its nested *An Unfinished Composition* reader. Chrome CDP verified **8/8 desktop/mobile keyboard Enter journeys**, AX root-link names and ≥44 px touch targets with fully loaded artwork, no overflow and zero JS exceptions. Exact source checksums, release/predecessor and remaining boundaries: [v63 root-hand evidence](../docs/acceptance/2026-10-29-r28-open-hand-root-v63.md). Fountain Press owns the reusable behavior, not the stage assembly script. The nested First Readings historic domain header remains, native iPad Safari/VoiceOver and public two-domain alias are not asserted. Earlier v62/v10 reports below are historical evidence, not currently selected release claims.

## Current observed reader stage — 29 October 2026

The author-directed first Reframe Reader scenario **R28** now runs on the **existing** canonical owner-WLAN staging service at `http://192.168.8.50:8200/estate/`. The active `current` symlink resolves to immutable release `shared-shell-20261029-v62-reframe-r28-20015e9`; the immediately preceding complete `shared-shell-20261029-v61-sing-folio-e613dd4` remains retained for rollback. The existing `fountain-shell-acceptance-preview.service` was restarted after activation because its previous process had cached the old resolved stage root. HTTP readback verified the new Press Bookshelf and exact seven-essay deep route; desktop 1024px / mobile 390px Chrome CDP, AX name/role and keyboard cover-to-book-to-shelf behavior were observed. The first two genuine Press covers remain, and existing other routes were preserved. This stage is **private** and no public domain DNS, content or publication effect is claimed.

The root now shows **Bookshelf · Reframe Reader**, not the historic nine-domain shell. Technical path `/estate/` and the publisher's `EstatePublisher` identifier persist only for backward compatibility; neither is user-facing branding. **First Readings' nested route still has the historical header**, native iPad Safari/VoiceOver and exact two-public-host alias are not accepted. The present source of truth for release identity is [environment.json](environment.json), including `surfaces.estate-shell-acceptance.currentReaderStage`; [R28 v62 independent evidence](../docs/acceptance/2026-10-29-r28-first-reader-wlan-v62.md) records source/artifact SHA-256 and staged readback.

The historical 22 October state described below is preserved for provenance; it does **not** supersede the observed v62 activation.

**Binding estate-specific FCIS rule.** Source owner: `Fountain-Coach/estate`; machine-readable identity: [environment.json](environment.json). This is an **existing environment registration**, not a new server, additional release service, or requirement to build another test harness.

**Current accepted staging release (22 October 2026):** `shared-shell-20261022-v10-editorial` is the observed active `current` target of the canonical author-facing service on port 8200; `shared-shell-20261022-v9-local-links` remains available for rollback. Three editorial roots returned HTTP 200 with the exact v2 shell marker after activation. The v10 shell improves the shared masthead, visible editorial reel labels and legal-footer hierarchy; the unchanged source work digests and test results are documented in [v10 correction and stage readback](../docs/acceptance/2026-10-22-estate-shell-v10-editorial-correction.md). This remains **WLAN staging**, not production.

## The identity is not the release

The owner-controlled estate staging environment is the already existing **Ubuntu Intel Mac mini**, SSH alias `MacMiniDocker` and hostname `benedikt-Macmini.local`. Its **observed reachable WLAN** address on 22 October 2026 is `192.168.8.50` via `usb0`. This machine is the staging environment. Neither its IP address, its numerous services, nor any active symlink release separately constitutes a different *estate staging environment*.

The current **author-facing EstateShell entrance** is [http://benedikt-Macmini.local:8200/estate/](http://benedikt-Macmini.local:8200/estate/) (verified HTTP 200 by machine name); the currently reachable direct-IP alternative is `http://192.168.8.50:8200/estate/`. It is provided by the **existing** `fountain-shell-acceptance-preview.service`, whose active release is read through `/home/benedikt/estate-shell-acceptance-staging/current`. At this audit the resolved release is `releases/shared-shell-20261022-v9-local-links`. Teatro and First Reading are available at the same origin under `/teatro/` and `/solstice/editions/first-reading/`.

Other services on the **same staging machine** have separate purposes, not equal precedence: `8202` is the distinct 22 October shared-shell `v5` proof, `8201` the browser-release-continuity instrument, `8198` the public-byte nine-domain reel comparison, `8180`–`8182` the Linotype book/reader presentation, and `8194` the **access-controlled** authentic Satzfunk archive. An agent MUST NOT select one as "the current estate" because it responds first, carries a later timestamp, or shares the machine.

The older `192.168.8.11:8443` is an earlier estate service on that Ubuntu host, **not** the current canonical author-facing EstateShell entrance. Historical `192.168.8.249` stage links were superseded by the current reachable `.50` interface. Both remain historical evidence only.

## Mandatory discovery before answering "show me staging"

1. **Read** `staging/environment.json` from the current `Fountain-Coach/estate` owner branch. Use `canonicalEntrySurface`, not arbitrary page names or historical README snapshots.
2. **Check** the named service and `activeReleaseSymlink` using existing SSH to `MacMiniDocker`. The current symlink is the authority for *which staged release is active*, not the `observedRelease` field or a Git timestamp.
3. **Verify** the declared entry URL by real HTTP readback (with its staged route and at least one relevant asset/deep route). On a material discrepancy, report **stage drift against the named canonical surface**, not a new environment, invented blocker, or an unrelated old service.
4. **Provide the direct author entrance and a copyable URL.** Say what is staged and distinguish staging from independently published production. Preserve the real active stage; do not redeploy, switch a symlink, restart services, copy media, or change DNS just to answer a viewing request.

A new accepted stage release updates the **existing canonical service's** `current` link, with prior release retained. If the author intentionally changes the canonical entrance, update `staging/environment.json` with an evidenced transition, retain the previous binding as historical, and update root `AGENTS.md`. Do not silently nominate whichever prototype is newest.

**FCIS Goal Fidelity and Non-Invention** applies. Lack of a test or browser screenshot is not authority to invent a new staging server, enroll an agent or force a new dependency. For publication to the public estate, apply the distinct existing production publication authority.

## Read-only evidence, 22 October 2026

- SSH `MacMiniDocker` succeeded; host reported reachable address `192.168.8.50` on `usb0`.
- `fountain-shell-acceptance-preview.service` reported active; its current symlink pointed to `shared-shell-20261022-v9-local-links`.
- HTTP GET on `8200/estate/`, `8200/teatro/`, and `8200/solstice/editions/first-reading/` returned 200.
- `8202/estate/` also returned 200, but is the distinct proof service `fountain-estate-shared-shell-proof.service` with release `20261022-v5`.
- Original private Satzfunk `8194` returns 403 anonymously, as intended.
- **No production publication or stage symlink change** was carried out to establish this contract.

This corrects the earlier conflation of an old `.11:8443` estate service and the owner-facing current staging entrance without creating new infrastructure.
