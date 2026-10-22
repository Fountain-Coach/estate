# EstatePublisher — canonical Ubuntu WLAN staging v11

**22 October 2026, 20:00 CEST · typed terminal receipt ACTIVE · PUBLIC PRODUCTION UNCHANGED**

## Environment and exact identity

- Logical environment authority: `Fountain-Coach/estate/staging/environment.json`
- Canonical author-facing entrance: `http://benedikt-Macmini.local:8200/estate/`
- Governance entrance: `http://benedikt-Macmini.local:8200/governance/`
- Direct-IP fallback: `http://192.168.8.50:8200/estate/`
- Existing host: `MacMiniDocker` (Ubuntu Intel Mac mini)
- Existing service: `fountain-shell-acceptance-preview.service`
- Source lock: `47e7ac71115a16cf7b73a595a554b9d37a93964b` in `Fountain-Coach/estate` (branch `fix/public-estate-shell-all-domains-20261022`)
- EstatePublisher typed-stage implementation: `1036e4cc18cf07e41301ffeddb43ed470ff67022` (`Fountain-Coach/EstatePublisher` PR #1)
- Active immutable release: `shared-shell-20261022-v11-eight-owner-47e7ac71`
- Preserved immutable predecessor: `shared-shell-20261022-v10-editorial`
- Stage service provides `X-Robots-Tag: noindex, nofollow` and `Cache-Control: no-store, max-age=0`.

## EstatePublisher actual outcome

**[Exact terminal receipt](2026-10-22-estatepublisher-wlan-v11-terminal-receipt.json)**:

- `state=active`
- `activated=true`
- `stagingIdentity=UbuntuEstateShellWLANStage`
- `sourceRevision=47e7ac71115a16cf7b73a595a554b9d37a93964b`
- `sourceInventorySHA256=5d601f09d646e477bde0fa992596bb404a17f054f129fcbc79f7214a37398ec2`
- **356 static files** uploaded and independently SHA-256 verified on Ubuntu before activation.
- **11 direct HTTP witness routes** fetched independently by EstatePublisher and SHA-256 identical to the manifest after the atomic activation. These include all 8 entrances, First Reading, and Governance Chapters 158 and 159.
- The existing `current` symlink and service were independently checked after publication; previous v10 directory remains intact for rollback.
- `publishedPublicly=false`: this is a **WLAN staging release**, not a Hetzner production publication. No remote program, Caddy configuration, DNS, public TLS, FountainStore prerequisite or extra host service was introduced.

## Source and acceptance gates

- Source-owned Governance Git revision `03f15306a018eddd85fab491e592d2fdffd61528`: 294 files and **160 chapters**, with authored content preserved in the stage-only projection. This edition contains two newer Governance source changes compared with the currently public October 20 release; the stage does not silently publish those changes.
- The other seven public front doors were independently fetched over HTTPS and SHA-256 locked; their site-owned assets were reused from the pre-existing October 21/22 stage mirrors. Private Satzfunk audiovisual media were never copied.
- **174 HTML paths** across 8 editorial owners pass the new structural stage gate: exactly one shared publisher masthead/reel/footer, 9 identities in canonical order, one Info action, Status in legal footer, domain active identity, and only explicitly WLAN-local editorial URLs. Satzfunk is visible but inert because it is not yet a cleared public domain.
- EstatePublisher Swift tests: **14/14 passed**, including wrong stage scope, no Store dependency, active staging not public, readback failure rollback.
- Public-candidate source suite: **14/14 passed**.
- Chromium browser evidence: **32 site/viewport combinations** (8 owners × desktop/iPad landscape/iPad portrait/phone). Common shell computed background and geometry are identical across all eight domains at the same viewport, with readable footer text and no shell overflow. Governance → Book navigation, browser Back, and inert Satzfunk behavior passed.
- Browser evidence and screenshots: [browser report](https://github.com/Fountain-Coach/estate/blob/fix/public-estate-shell-all-domains-20261022/docs/acceptance/evidence/2026-10-22-v11/browser-evidence-v11.json), [Governance iPad-sized entrance](https://github.com/Fountain-Coach/estate/blob/fix/public-estate-shell-all-domains-20261022/docs/acceptance/evidence/2026-10-22-v11/governance-ipad-portrait-v11.png), [Governance iPad-sized footer](https://github.com/Fountain-Coach/estate/blob/fix/public-estate-shell-all-domains-20261022/docs/acceptance/evidence/2026-10-22-v11/governance-1032-footer-element-v11.png), [Governance phone footer](https://github.com/Fountain-Coach/estate/blob/fix/public-estate-shell-all-domains-20261022/docs/acceptance/evidence/2026-10-22-v11/governance-390-footer-element-v11.png), [Estate iPad-sized entrance](https://github.com/Fountain-Coach/estate/blob/fix/public-estate-shell-all-domains-20261022/docs/acceptance/evidence/2026-10-22-v11/estate-ipad-portrait-v11.png).

## Known defects and withheld acceptance

**Not a full visual/performance PASS**:

1. Four browser cases reported content-asset requests with 404: Pointer's two author-owned landscape image URLs were absent from the older stage asset mirror (affecting desktop and iPad viewports), while the live public Pointer host currently returns HTTP 200 for those files. This is stage source-asset fidelity drift, **not** a shared header/footer regression. Do not hide it by changing the authored content.
2. The Solstice landing requests `/solstice/assets/solstice-mark.svg`, which is absent on this staging projection; the corresponding public author URL also returns 404. This is a source-owned asset issue, not evidence that EstatePublisher failed its hashed promotion.
3. Native **iPad Safari acceptance remains OPEN**: Simulator's `simctl openurl` returned LaunchServices code 115 on this Mac, including independent Safari start attempts. A simulator screenshot captured after attempted keyboard navigation showed the home screen, **not a successfully loaded webpage**. The Chromium iPad-sized captures are correctly labeled Chromium, not native WebKit. Do not claim physical iPad acceptance.
4. Full 160-chapter independent HTTP byte readback was not performed: all 160 passed the **local structural gate**, while EstatePublisher's independent HTTP readback covered the declared 11 representative routes.

## Promotion and rollback rule

**Current staging may be proofread at its canonical URL.** The immutable v10 predecessor is retained. If the new stage is rejected, use the same typed EstatePublisher staging rollback for its exact v11 release and verify v10 readback. Do not deploy to public Hetzner production until author acceptance, complete owner source/rights decisions and a separately authorized EstatePublisher public receipt.

**FCIS Chapter 158 respected:** persistence and static publication remain decoupled; no helper-server installation, forced enrollment, GitHub CI, Store sync, or production source rewrite.
