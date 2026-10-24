# Book publishing production release v15 — independent estate witness

**24 October 2026; publicly active.** The author's direct request was to fix the Book-specific static host routing and promote the already reviewed `book.fountain.coach` publication. This estate witness preserves the independence of source, stage and public delivery authorities.

## Bounded release authorities

- Book source owner `Fountain-Coach/book-of-reframe` at content revision `1b7d887174e65a83159f7834f9bd7b91fb41f4bb`; native source-owned [full acceptance and final receipt](https://github.com/Fountain-Coach/book-of-reframe/blob/main/docs/releases/2026-10-24-book-v15-publication-acceptance.md).
- Predecessor `estate-20261024-v14-satzfunk-reel-book`; current immutable publication `estate-20261024-v15-publishing-books-1b7d887`. Both the active symlink and retained rollback were independently inspected over owner SSH.
- Existing EstatePublisher SSH delivery CLI prepared and preflighted the pinned **40-file** Book candidate; the typed public receipt subsequently reported `activated=true`, `state=active`, exact published bytes verified via HTTPS on eight required paths.
- Supporting four real public readers (not PDF handoffs) remain owned by `Fountain-Coach/works-benedikt-eickhoff` source `837510664fa90d2883d7670c13ecab287f6d4f49` and release `estate-20261024-v14-works-book-readers-8375106`, with original authorship, PDF provenance and source-domain URLs preserved. Works is not a new top-reel item or a new Bookshelf admission.

## Single Caddy defect and correction

The existing Book host matcher lacked its own `/assets/*` CSS/social/icon path and newly authorized `/publication/*`, `/history/*` paths. An independently downloaded production Caddyfile was hash-pinned at `bc2e60820fe9d77ee875a688e3c7a46a573bd2619be28c2e4db1292f4c5126cc`. The constructed replacement changed only the existing `@estateRailBook` matcher (host `book.fountain.coach`) by appending `/assets/* /publication/* /history/*`; all other host rules were byte-identical. The Caddy candidate was delivered with existing SSH, validated with `caddy validate`, and a remote original was retained at `/etc/caddy/Caddyfile.before-book-reading-routes-20261024`. The accepted configuration SHA-256 `277203a076bda8a3a1ff518d2efeb754c2dfec2554b647919e1c394fa018f110` was verified after the host-scoped activation. `systemctl reload caddy` succeeded; service remained active.

The previous attempt had been held due to that specific host matcher defect. Its hold record remains as historical evidence but is marked **resolved**. The user did not require a new publishing or security subsystem; none was added.

## HTTPS and browser observations

After the native publisher returned active, a separate public HTTPS/cache-busting source SHA check matched **all eight** source candidate/public bytes: homepage, site stylesheet, publishing social image, book SVG, First Reading publication case, historical Reframe development archive, legacy command inventory and Csound technical page. The current `book.fountain.coach` symlink matched v15 and retained v14 for rollback.

Actual public HTTPS browser testing with Chromium at desktop `1280×900` and phone `393×852`, browser cache disabled, showed the new publishing H1, four correct Works reader links, nine-item estate reel, Status legal-footer link, functioning publication and history routes, no missing images, no page errors and no horizontal overflow. The full set of four Works readers had already passed public desktop/mobile page-turn tests before promotion.

Works v14 and Instruments v16 production symlinks stayed unchanged; Status public root returned HTTPS 200; the canonical Ubuntu WLAN stage remained `shared-shell-20261024-v26-discreet-references-876b613`. No jobcase/private legal records or unreleased userland material were introduced. This confirms a **public Book release**, not admission to the private Reframe Bookshelf or native Safari/iPad-specific parity.

## Completion

Book is now a public publication-oriented entrance with source-bound, actually readable Works editions and explicit author/publication evidence. No future action or additional runtime needed for this authorized Book deployment. Future static Caddy config reconciliation must retain the accepted Book-only matcher path delta.
