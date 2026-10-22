# Fountain Coach Estate — one named WLAN staging environment

**Binding estate-specific FCIS rule.** Source owner: `Fountain-Coach/estate`; machine-readable identity: [environment.json](environment.json). This is an **existing environment registration**, not a new server, additional release service, or requirement to build another test harness.

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
