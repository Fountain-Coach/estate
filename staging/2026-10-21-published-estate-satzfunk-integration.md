# Published-state Fountain Coach → Satzfunk integration

**Observed and staged:** 21 October 2026
**Authority:** the currently served live HTTPS estate was inspected first. This is a local **visual integration proof**, **not** an EstatePublisher public deployment, a switch to the local experimental bookshelf, or a media-release authorization.

## Observed actual production estate

| Host | HTTPS readback | Current experience |
| --- | --- | --- |
| [fountain.coach](https://fountain.coach/) | HTTP 200, `Last-Modified: Sun, 18 Oct 2026 07:59:56 GMT` | Existing future-facing portal: “Author the conditions for what comes next”, Fountain mark, nine illustrated/typed destination cards, Memory Vector/Teatro Score and a shared estate-navigation rail. **Not** the four-cover WLAN Linotype bookshelf. |
| [teatro.fountain.coach](https://teatro.fountain.coach/) | HTTP 200, `Last-Modified: Tue, 13 Oct 2026 04:33:41 GMT` | Existing compiled Teatro Stage Web, shared estate rail; **not** the newer standalone book/Score landing in current Git owner. |
| [works.benedikt-eickhoff.de/solstice/editions/first-reading/](https://works.benedikt-eickhoff.de/solstice/editions/first-reading/) | HTTP 200 | Real Solstice Linotype First Reading edition. Independent authorial source/route must not be folded into Satzfunk. |
| [governance.fountain.coach](https://governance.fountain.coach/) | HTTP 200 | Normative publication/governance book. |
| [satzfunk.fountain.coach](https://satzfunk.fountain.coach/) | DNS resolution failed from verified Mac | No public host, release or certificate witnessed. |

**Critical authority drift:** current Git owner `Fountain-Coach/fountain.coach/main/site/index.html` is already a newer Linotype bookshelf source, whose title is `Fountain Coach · Fountain Coach`, whereas the *actually public* root serves the future-facing portal. Likewise `teatro.fountain.coach/main/site/index.html` is ahead of its publicly served Teatro Stage Web entrance. A casual `git pull`, site deploy, or copying the four-front WLAN release would **replace** the observed public aesthetic and navigation rather than integrating into it. This must be explicitly reconciled before production.

## New separate local preview

**Review URL:** http://192.168.8.50:8197/  
**Service:** `fountain-live-state-satzfunk-preview.service` (user/systemd, Ubuntu Mac mini; `noindex,nofollow`; no-store; LAN-only)  
**Root:** `/home/benedikt/estate-published-state-staging/current`  
**Pinned local release:** `releases/20261021-published-portal-satzfunk-v1`

Source generator: [scripts/prepare-live-estate-satzfunk.py](../scripts/prepare-live-estate-satzfunk.py). Read-only server: [scripts/serve-published-state-preview.py](../scripts/serve-published-state-preview.py).

The generator fetched **the exact publicly served** `fountain.coach` home HTML, logo, Memory Vector artwork, current stylesheet, shared estate styles and runtime JavaScript to a separately named local root. It then changed only:

1. Added an **originally styled** `Satzfunk` entry immediately after Teatro in the existing top estate rail, addressing the protected LAN original archive `http://192.168.8.50:8194/`.
2. Added one matching original-portal-style destination card, `10 · AUDIBLE WORK`, “Satzfunk — an author's radio” in the **existing** `estate-grid` after `09 · NEW ESSAY`; the link points to the same protected archive. It is **not** a new cover/reel and does not invent a publicly released episode.
3. Added explicit `noindex,nofollow` and local-preview marker in HTML.

The central Memory Vector, existing site headings and cards, other live publication URLs, identities and typography remain in the same captured source. Media, text from copyrighted dramatic translation, cookies, authorized archive passwords/tokens, vendor bank material and archive MP4s were **never copied**. This preview uses no DNS/Caddy, public Store or external media-serving effects. A person without the private archive cookie receives 403 at the destination; **the preview does not bypass this**.

## Evidence

- Captured original public homepage SHA-256: `deee2ab39eac56511989f624911e3274db1aba657c197ce235f82a3353b13ca9`; hashes of the seven original captured files and change assertions are in `capture-lock.json` within the staged release.
- Local `http://192.168.8.50:8197/` returned **HTTP 200**, no-store, noindex. Live-mirrored CSS and the Memory Vector SVG assets returned **200**.
- Exactly one `data-estate-id="satzfunk"` and one `data-estate-addition="satzfunk-private-wlan"` were counted in the served HTML.
- Protected original archive `http://192.168.8.50:8194/` still returns expected **403** to anonymous requests.
- Chromium headless screenshots of the local portal at 1200×840 and 400×900 were captured on the Mac. The original live HTML/design is visually intact on desktop. The narrow screenshot showed **pre-existing horizontal overflow/clipping** near the mast/intro; this was not introduced by the new Satzfunk card, which is below that region. Native iPad visual acceptance is still pending.

## Decision to move toward actual public estate

The author wishes to develop and enliven the **already published** Fountain Coach website. The right final change is a **supporting** Satzfunk publication identity and site address in that site's authentic shared rail and existing editorial card system, **not** replacement with the local bookshelf. Satzfunk itself owns the original six-edition audiovisual radio/archive, not the rejected empty-cover reel. Teatro remains the producing/performance tool, `sing` a new voice instrument, Solstice the writing source.

Before publishing:
1. Reconcile live-public home HTML and current source-owned Git main into one **approved source revision** without losing current public features or newer book work; perform a meaningful diff, not a blanket static copy.
2. Admit Satzfunk's host/destination via the typed estate and publishing authority. A public `Satzfunk` link must target a **working HTTPS canonical hostname**, not an internal `192.168.8.50` address.
3. Publish from the accepted Satzfunk archive interface only public-admissible, rights-cleared media/transcript layers, retaining its credits and edition IDs. The historically restored Bandcamp videos and 7VST translation are **not** implicitly cleared by this staging exercise. An original Bandcamp source link/approved official embed can serve as a non-self-hosted transition when the specific use is reviewed.
4. Use native FountainStore / EstatePublisher exact-host and path-scoped route sync, then independent DNS, HTTPS, browser, audio and rights/credit readback.
5. Confirm accessibility, shared navigation and iPad Safari; preserve the prior live release and make rollback independent from local staging.

No production site was changed by this work.
