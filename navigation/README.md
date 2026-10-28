# One estate reel, one owner, many domains

**Authorial decision:** 21 October 2026. The estate's top reel must have **identical membership, order, labels, destinations, icon shapes and active identity semantics on every domain**, including Satzfunk. A one-off link on `fountain.coach` is a failure.

## Canonical semantic contract

[canonical-reel.v1.json](canonical-reel.v1.json) is the one authority for these **nine editorial destinations**:

| Order | ID | Public address | Editorial role |
| --- | --- | --- | --- |
| 1 | estate | https://fountain.coach/ | Public estate entrance |
| 2 | book | https://book.fountain.coach/ | Development story |
| 3 | governance | https://governance.fountain.coach/ | Rules and authority |
| 4 | midi2 | https://midi2.fountain.coach/ | Typed MIDI 2.0 relations |
| 5 | instruments | https://instruments.fountain.coach/ | Instrument capabilities |
| 6 | teatro | https://teatro.fountain.coach/ | Performing and staging |
| 7 | satzfunk | https://satzfunk.fountain.coach/ | The original audiovisual author radio/archive |
| 8 | works | https://works.benedikt-eickhoff.de/ | Writer-owned work, books and production context |
| 9 | solstice | https://works.benedikt-eickhoff.de/solstice/ | Writer-owned source |

**Status is a supporting legal/footer address** at `https://status.fountain.coach/`, not an editorial top-reel item. The reel also has one **Info** footer jump that is not an estate domain. Only the active editorial domain has `aria-current="page"`; on Status there is no active editorial item. At the local archive the Satzfunk identity is active.

**Current as of 24 October 2026:** Satzfunk is publicly released at https://satzfunk.fountain.coach/ on its dedicated Hcloud server, with all 43 recorded Bandcamp video items served from owned storage and independently verified via TLS and byte-range readback. The public reel destination is now a normal focusable HTTPS anchor. The earlier WLAN-only condition below documents the historical 21 October state.

## Why this change was required

Direct HTTPS readback on 21 October 2026 revealed **nine independently rendered estate reels**, different HTML bytes, different active markers, and an inconsistent Status membership: most pages displayed Status in the top rail and Governance did not. **None** displayed Satzfunk. Older `estate-core.js` differs between owners and some domains enforce strict Content Security Policy.

The source owners remain separate, and the currently deployed roots differ from their latest GitHub main branches. Consequently, a blanket `git pull` to production or replacing the whole public estate with the Linotype staging bookshelf is explicitly **not** an acceptable fix.

## Current verified local presentation

**Unified nine-domain comparison:** [http://192.168.8.50:8198/estate/](http://192.168.8.50:8198/estate/) (LAN only)

This single local service serves snapshots of the **actual publicly deployed** entry page from each of nine editorial/supporting hosts, with precisely the same projected nine editorial links. Selecting an editorial reel item moves between the local mirrors, retaining each domain's own original design. The Satzfunk item points to the **actual protected historical audiovisual archive** at `http://192.168.8.50:8194/`, *not* a copied player, an empty-cover reel or a fake public domain. The album catalogue and original 7VST historical page both receive the same shared navigation in their private Ubuntu staging HTML.

- Stage server: `fountain-canonical-reel-preview.service`, Ubuntu user systemd, port **8198**.
- Stage source: `/home/benedikt/estate-unified-reel-staging/current` → `releases/20261021-canonical-nine-entry-v7`.
- Stage media/access: no copied WAV, MP3, MP4, dramatic translation, bank, credential or auth cookie. The original archive continues on 8194 with 403 for an anonymous caller.
- Source replayer: [../scripts/prepare-unified-estate-reel.py](../scripts/prepare-unified-estate-reel.py). **Do not call its published-byte input Git ownership**: these are immutable audit samples of currently deployed public bytes.
- Stage proof: [../scripts/verify-unified-estate-reel.py](../scripts/verify-unified-estate-reel.py); nine sites, nine ordered editorial identities, consistent Info, active identity, no top Status, and Status in each footer; HTTP response/asset integrity, noindex, private archive gate.
- Private Satzfunk staging projection: [../scripts/stage-satzfunk-canonical-reel.py](../scripts/stage-satzfunk-canonical-reel.py), modifying only two HTML entry pages and their presentation CSS after versioned backup.
- Archive backups on Ubuntu: `/home/benedikt/services/satzfunk-private-video-browser/branding-backups/20261021-pre-canonical-reel/` and `20261021-pre-footer-only-reel/`.
- Previously deployed stage on port **8197** represents the earlier **one-site-only** integration and is **not** the canonical multi-domain acceptance artifact.
- Earlier `8180/8181/8182` release is a separate experimental Linotype edition bookshelf and must not be confused with the currently published public estate.

The shared preview itself uses the original sites' CSS. The Solstice entrance forbids inline scripts by Content Security Policy; its **active marker uses an external same-origin `reel-preview-state.js`**, so there is no security-policy relaxation.

## Admission to public production

1. Admit/serve the intended Satzfunk hostname with actual rights-cleared source/credit media under FountainStore/EstatePublisher, or designate a truthful accessible first-stage authorized landing. No bare public link to a non-existent domain.
2. Reconcile the actual public source bytes for every domain with its Git owner and manifest, preserving existing content and newer unreleased features separately.
3. Project the common navigation fragment from this one owner into **every navigation-bearing page**, not merely each domain's homepage. A deep route must pass the same semantics or expressly identify a permitted book/reading presentation exception.
4. Validate the exact same nine IDs/URLs/order, one Info, Status in the legal footer, correct `aria-current`, keyboard/mobility and iPad browser behavior. Fail release on a missing/duplicate item. Use each domain's existing Content Security Policy.
5. Deploy through each authorized source-owner publication route, with verified rollback and independent public HTTPS readback on all nine domains **plus** the new Satzfunk domain.

Until all release predicates hold, this is **a verified local integration**, not a claim of fixing the live public estate.
