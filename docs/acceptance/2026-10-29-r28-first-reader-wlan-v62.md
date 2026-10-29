# R28 — First Reframe Reader Bookshelf on canonical WLAN staging

**Date:** 29 October 2026  
**Evidence class:** independently observed owner-WLAN staging and browser readback. **Not** an iPad Safari, FountainStore-admitted public library, paid Writer, production release, HTTPS two-host alias or general accessibility certificate.  
**Owning product scenario:** [Reframe R28](https://github.com/Fountain-Coach/Reframe/blob/main/scenarios/028-one-reader-wlan-first-bookshelf.md); ADR-007 Reader/Writer and ADR-008 one-source/two-domains.  
**Staging implementation owner:** `Fountain-Coach/estate/staging/r28_first_reader.py` at commit `20015e94f2ebcf30c631a2d6ec2f3ca5571340eb`; verified script SHA-256 `e6256e15108df3a4ee8ae1dc823e5c4a768ad3f6754bf8308d6a3ec663cc2308` (earlier first draft failed safely, revised committed script passed). This is a **direct-static staged projection of existing Fountain Press material**, not a second compositor or a new Reframe command.

## One canonical WLAN stage and retained predecessor

| Identity | Observed fact |
| --- | --- |
| Stage host | Existing owner-WLAN Ubuntu Mac mini, `MacMiniDocker`, `192.168.8.50` |
| Canonical Reader entrance | `http://192.168.8.50:8200/estate/` |
| Current active release | `shared-shell-20261029-v62-reframe-r28-20015e9` |
| Immutable predecessor / rollback | `shared-shell-20261029-v61-sing-folio-e613dd4` |
| Active selection | `/home/benedikt/estate-shell-acceptance-staging/current` resolves to v62 |
| Serving process | Existing `fountain-shell-acceptance-preview.service` restarted after symlink change; fresh `MainPID=984303`, service `active` |
| Public host effects | **None**; `fountain.coach/` still returns its prior public portal (HTTP 200, 18,449 bytes), and `benedikt-eickhoff.de/` still returns HTTP 308 to `works.benedikt-eickhoff.de/` |
| Publication rights / native iPad | Not inferred, not changed, not accepted |

The previous service process had cached the real v61 directory. Immediately after changing the `current` symlink, HTTP still served the old Essays root and the new route returned 404. Restarting the *existing* service made it resolve the v62 selection; independently observed HTTP root then became the new Bookshelf. **Service status, live symlink and HTTP bytes were each checked separately.** No new WLAN server or production publisher was provisioned.

## Source and route custody

The v61 source lock records the seven-essay original staged plan: source owner `Fountain-Coach/fountain.coach`, source commit `5ec8c5490c8a1fe2b4a941185ecb3f415a7bdfdd`, seven chapters, author-controlled private stage. The R28 composition reused **the exact already-present Fountain Press Bookshelf markup** from `/estate/editions/`, not new faux book tiles, and retained its two existing source-authored cover images and First Readings identity. The old root's authored full Essays reader was preserved in a new explicit edition route, without rewriting the essay prose, media or measured engine.

| File / route | Input SHA-256 | Result SHA-256 | Change |
| --- | --- | --- | --- |
| `estate/index.html` | `acc8e540360bb1798e18aa58a2896d608a51e2b1ed93fd9875c9f43eaae5e6bb` | `d63e00a2117a3760b3137cb6a8e5b89ac2dd842fbcac2aeb363e556c022119a0` | Existing Press two-cover Bookshelf becomes the principal Reader |
| `estate/editions/index.html` | `4acb31dbca48c84e129b7677a9d05e3b36f4212aafb6ca633ff016c92a505468` | `d63e00a2117a3760b3137cb6a8e5b89ac2dd842fbcac2aeb363e556c022119a0` | **Byte-identical** secondary entrance to the same Bookshelf |
| `estate/editions/essays-continuing/index.html` | New path, authoring from original v61 source-bound root above | `dca55623d8e558b14286567b1998536bddf8d9e5585c6e2181e53e602cf2fbf5` | Seven original Press essay sections, semantic paths and stage media retained; old injected nine-domain shell removed, in-book return to Bookshelf |
| `estate/assets/linotype/reframe-reader-r28.css` | New scoped CSS | `16cfe681fdf1fe4e154568022663635175547c2bcb6323df197a97a769c00aff` | Styling of **existing** Press Bookshelf and footer |
| `estate/collections/first-readings/collection.json` | `8cbaa8cf73400602d0d61520f18d3b8f2e7885e2570981e941a6184b29d91314` | Unchanged | Exact original collection identity |
| `source-lock.json` | Original stage source lock | Appended `reframeFirstReaderR28` record | Original source/reader hashes, paths, predecessor and new candidate evidence |

A full `diff -qr` between v61 and v62 found **only** the two changed HTML entrances, the newly added `essays-continuing` directory and CSS file, and `source-lock.json`. Other 1,158 original files/media and source owners remained preserved. Former routes continue to exist; source-owned Bookshelf membership is **not** asserted to have been newly written to FountainStore.

## HTTP and browser readback

| Route / asset | HTTP |
| --- | --- |
| `/estate/` and `/estate/editions/` | 200, 5,260 bytes, root title **Bookshelf · Reframe Reader · Fountain Coach** |
| `/estate/editions/essays-continuing/` | 200, 105,835 bytes, title **Essays — A Book Continually Written** |
| `/estate/collections/first-readings/` | 200, 10,369 bytes |
| Reader CSS, Press book CSS, original Essays cover artwork | 200 |
| `/solstice/editions/first-reading/` and `/teatro/` | 200 |

Actual Google Chrome headless **Chrome DevTools Protocol** (not screenshot guesses) exercised desktop **1024 × 850** and mobile-emulated **390 × 844** viewports. In both profiles: `innerWidth === documentElement.scrollWidth`; two source-owned Press cover images loaded; the Bookshelf heading, author and legal links were present; the historical nine-domain shell was absent from the principal Bookshelf and the continuing book; clicking Essays opened exactly the seven-section source-bound `essays-continuing-20261029` with intact semantic sequence options; returning from its in-book toolbar reached the identical Bookshelf. No 4xx network responses were recorded.

A separate keyboard and accessibility-tree test at mobile width found named skip link, Bookshelf heading, both cover links and legal/reference links in Chrome AX. Keyboard **Enter** on the focused Essays link entered the seven-essay book; keyboard **Enter** on its focused back link returned to the Bookshelf. Original First Readings route opened with its existing one-book cover. The two real-viewpoint screenshots were visually inspected (desktop and genuine CDP 390-pixel mobile, which corrected the misleading minimum-window-width effect of plain Chrome screenshot-only mobile arguments).

**Known limits, not silently accepted:** the unmodified First Readings child route still displays its historical nine-domain header, to be reframed in the next bounded Reader scenario; live native iPad Safari and VoiceOver acceptance are still pending. Original source meta-CSP contains an unsupported `frame-ancestors` directive: Chrome logs that the directive is ignored when delivered in a `<meta>` element (four console messages across the desktop/mobile root/book readbacks). This is **not** a JavaScript exception or broken network resource, but it is not proof of an effective header-level frame embedding policy; repair/verify at the appropriate publication security owner, not by claiming R28 implements it. No real audio performance or external provider spending was performed.

## Release and next acceptance boundary

**R28 first WLAN projection: observed and independently read back.** The current staged address is available for editorial review, and the v61 symlink target remains retained for exact rollback. Public `fountain.coach` and `benedikt-eickhoff.de` have not been redirected or independently re-hosted, so ADR-008's two-domain alias/redirect acceptance remains **OPEN**. A future Reader pass should bring First Readings and subsequent legitimately admitted works into the same book-first shell, while preserving their source/copyright authority, and then test real iPad Safari/VoiceOver. Production requires an independent EstatePublisher rights/publication authorization and public readback; no such receipt is asserted.
