# Shared EstateShell — three-source WLAN acceptance witness

**22 October 2026 · Fountain Coach · preview release, not public publication**

## Scope and ownership

Implement one pinned common masthead, estate reel and semantic four-region legal footer around the **actual public HTML bodies** from `fountain.coach`, `teatro.fountain.coach` and delegated Solstice First Reading. Do not mutate their manuscripts, Linotype compositor, Teatro stage, or private Satzfunk media. Reframe's author-approved Bookshelf membership is independent of EstatePublisher public website publication.

**Source branch:** `Fountain-Coach/estate:feature/shared-shell-acceptance-20261022` at feature implementation commit `f6c603d39bef924a47c99e1a2ff658d499278b84` (prior to this receipt). Core files: `scripts/estate_shell.py`, `shell/estate-shell.css`, `shell/estate-shell-state.js`, `shell/assets/estate-shell-logo.png`, `scripts/build_shared_shell_preview.py`, `scripts/check_shared_shell_release.py`, `scripts/test_shared_shell_release.py`, `scripts/test_shared_shell_browser.py`, and `scripts/serve_shared_shell_preview.py`.

## Source and asset custody

| Exact public readback | SHA-256 | Preserved source |
| --- | --- | --- |
| `https://fountain.coach/` | `deee2ab39eac56511989f624911e3274db1aba657c197ce235f82a3353b13ca9` | Original future-facing portal and its work body |
| `https://teatro.fountain.coach/` | `71308fe02d4df6e0237884aeccccd8b040c0df2d32e2ea05e4243f93a008d996` | Original Teatro WebGL performance stage |
| `https://works.benedikt-eickhoff.de/solstice/editions/first-reading/` | `3faddbff97117fbe4e528ead6b714a093932d6f425806517d9c0ee8c18fb0e09` | Original Fountain Press measured Linotype First Reading |

Public asset snapshot: Fountain Coach six resources, Teatro four, Solstice 45, with **zero missing assets** in the pinned capture. The source-owned 460×460 logo is byte preserved, SHA-256 `8c5fad1c3db56138d5959da75991dc8034a0be537ce46da6ffcc0d9655e7f729`. Solstice original CSS and compositor JavaScript remain same-origin in the **private preview**, so its strict Content Security Policy is not relaxed. No private Satzfunk videos, 7VST translation, access cookies, Store records or other restricted material were mirrored.

## Actual local stage

- **Entrance:** `http://192.168.8.50:8200/estate/`.
- **Teatro:** `http://192.168.8.50:8200/teatro/`.
- **First Reading:** `http://192.168.8.50:8200/solstice/editions/first-reading/`.
- **Satzfunk:** `http://192.168.8.50:8194/`, protected existing author archive; anonymous readback **403**.
- Source-locked path: `/home/benedikt/estate-shell-acceptance-staging/current` → `releases/shared-shell-20261022-v9-local-links`.
- Ubuntu service: `fountain-shell-acceptance-preview.service` running on port 8200; `noindex,nofollow`, no-store and no directory listing. `source-lock.json` returns **404** externally. The previous release `shared-shell-20261022-v4` is preserved for rollback, as is the separate candidate on port 8199.
- The publisher's nine public HTTPS destinations remain untouched. The local stage overrides **only** four explicitly permitted navigation targets and retains the exact public canonical target in `data-canonical-href`: Estate, Teatro, Solstice, and Satzfunk. Cross-domain public mirror destinations remain public HTTPS only where no local preview exists.

## Tests actually run

| Gate | Outcome |
| --- | --- |
| Source/negative unit suite, `scripts/test_shared_shell_release.py` on authorized macOS host | **13/13 passed** |
| Cross-domain structural/asset/logo/source revision gate, `scripts/check_shared_shell_release.py --mode structural --stage-bindings source-lock.json` | **3/3 passed**, all four LAN bindings verified |
| macOS Google Chrome headless real HTTP browser integration, `scripts/test_shared_shell_browser.py` | **12/12 passed**: three site owners × desktop 1180×800 / iPad landscape 1024×768 / iPad portrait 768×1024 / phone 390×844 |
| Same masthead/reel/footer computed CSS + nine editorial identities + typed footer and Status placement | **Passed** in above bounded browser comparison |
| Active identity and clickable Info-to-footer once smooth scroll completes | **Passed** |
| Real Teatro canvas and Solstice's four original Linotype reader controls present | **Passed** |
| Existing Solstice source-owned book toolbar at narrow phone width | **Known upstream issue: 8px overflow**, independently reproduced on original public source |
| Native iPad Safari writer/editorial acceptance | **OPEN**, Chrome viewport sizes are not equivalent |
| Remaining six/nine estate owners, site deep routes and public Satzfunk rights/host | **OPEN** |
| EstatePublisher actual current-owner native cross-domain acceptance and authorized public release | **BLOCKED**, not simulated as passed |

Native macOS browser iPad-portrait screenshot SHA-256 (three separate witnesses):
- Estate `9c57ce7d39e30165d3be97679d3c5f4dd16af6a037b0a21c5fffce7db4c2865c`
- Teatro `937ad9cf223bd34462885e1ac4ffef89e5efbcfea1a061678504de145f811af1`
- Solstice `706ee08297ef0fb4a963711b6a19ac572b275ebbc65778f1e3b5eb50e00d32a3`

## Two publisher lanes are unchanged

- **Reframe → Bookshelf:** authenticated writer admission of a genuine source/edition/work/containing space; persisted FountainStore identity/state; Press composition. A source candidate, Empty, visual tile or approved reader does **not** create a public host.
- **EstatePublisher → website:** separately approved rights, target host, typed publication manifest/receipt, DNS/TLS and independent public HTTPS readback. The stage checker refuses to promote based on a fabricated or self-declared browser/publisher JSON and leaves public receipt validation to the current authoritative EstatePublisher executor.

## Remaining bounded next step

Run an actual native iPad Safari capture (landscape/portrait, click three editorial icons, return, Info footer and book controls). Address original phone toolbar overflow in its **Fountain Press owner** only after confirming authorial layout intent. Reconcile site owner build/shipping adapter and current authoritative EstatePublisher runtime ownership before adding a real typed public release gate. On a passing, approved exact-source multiowner admission, EstatePublisher—not this HTTP server—must execute and independently verify every HTTPS route with rollback.

**No public website, domain DNS, Caddy deployment, historical audio, Reframe Store membership, book manuscript or original source-owner branch was mutated in this acceptance cut.**
