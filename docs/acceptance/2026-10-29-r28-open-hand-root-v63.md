# R28 follow-up — open hand always returns to Reader root

**Observed:** 29 October 2026.  
**State:** Owner-WLAN **v63 staged and independently browser/AX checked**; not public production, not a physical iPad/VoiceOver acceptance, and not a new FountainStore admission.  
**User's rule:** **The open hand is the button to move to the root.** It is not a decorative mark or a parent-relative back button.

## Authority and code

Fountain Press owns the book/Bookshelf composition. The rule is recorded in [Press publication identity and cover navigation](https://github.com/Fountain-Coach/fountain-press/blob/main/docs/publication-identity-and-cover-navigation.md), with the actual Press `runtime/bookshelf.py`, `runtime/bookshelf.css` and `tests/test_bookshelf_collection_identity.py` changes at owner revision `5e04ce2502d537ba06b6e772ab58af86ad773413`. A focused source Press render smoke test passed for root and a nested source collection, confirming exactly one `/estate/` root anchor with the universal named hand, and no redundant collection arrow. The full Press test suite was **not run** as part of this bounded stage correction.

The publication staging projection is [`Fountain-Coach/estate/staging/r28_open_hand_root.py`](https://github.com/Fountain-Coach/estate/blob/main/staging/r28_open_hand_root.py), source commit `29fb917edf2c5ff6e5dd695ea268f9c209d3bdf8`. It reuses the exact existing hand PNG unchanged, adds the same named link to two **byte-identical** Bookshelf entrances and the existing First Readings collection, and substitutes the hand for the previous Back text on the continuing Essays and *Teatro — An Unfinished Composition* book toolbars. The former First Readings collection text arrow is removed as redundant. It does not create new works, cover artwork, record/rights authority, pages or web-shell renderer.

## Staging, content integrity and rollback

| Item | Exact observed identity |
| --- | --- |
| Canonical owner-WLAN URL | `http://192.168.8.50:8200/estate/` |
| Ubuntu active release | `shared-shell-20261029-v63-reframe-hand-29fb917` |
| Retained predecessor | `shared-shell-20261029-v62-reframe-r28-20015e9` |
| Current symlink | `/home/benedikt/estate-shell-acceptance-staging/current` resolves to v63 |
| Serving service | Existing `fountain-shell-acceptance-preview.service`, restarted after symlink activation; observed active |
| Bookshelf HTML SHA-256 | `7cc797797a2aa73dc4176036655efefcfe7a85e585d4abb71868c4b3798c4d95` |
| First Readings HTML SHA-256 | `ea2d626ce7b516d6c3ab7864ad2bafb907b301e166cbe26bd6e2613af130f84b` |
| Continuing Essays HTML SHA-256 | `c24303fbe864f48c88c144c06f085f713208475728f8b39512fb1541221b506b` |
| Teatro nested reader HTML SHA-256 | `b3704d0bf5cfd9da4063abd3d4baa937030752eb18f4e6853aad81ca8cca964c` |

The entire v62 immutable release was copied to nonactive v63, pinned by original root/collection/book and CSS SHA-256, and the existing stage `current` was checked before activation. The complete file-level diff shows **only** the two Bookshelf HTML routes, First Readings collection HTML, two connected book HTML routes, scoped R28 CSS and the updated source lock. The original artwork, Fountain Press runtime, other routes, media, essay manuscript source/identity and unchanged First Readings collection manifest remain byte-preserved. The prior v62 release remains available for rollback.

## Browser and accessible interaction

Live canonical-WLAN HTTP returned 200 for the Bookshelf, First Readings, continuing Essays and the nested *An Unfinished Composition* book. Chrome DevTools Protocol at true **1024 × 850 desktop** and **390 × 844 mobile-emulated** viewports exercised **eight root-hand journeys**:

- Exactly one accessible root-hand link per checked page, `aria-label="Go to Reader root — Bookshelf"`, original image loaded.
- Browser keyboard focus and **Enter** on the hand navigated to `/estate/` from all four pages, including an idempotent root-to-root action.
- Chrome AX reported exactly one named hand link on each page. Settled click/touch targets measured at **227 × 227 desktop / 171 × 171 mobile** on the root, **about 72 × 72 / 66 × 66** on First Readings, and **44 × 44** on both book toolbars.
- In all eight cases, document width matched viewport width, with no horizontal scrolling. The two existing Bookshelf cover identities, one First Readings member, seven original Essays chapters, one nested reader chapter and original artwork remained present.
- Chrome reported **zero runtime exceptions** during the settled test. The initial exploratory measurement ran before root CSS/image settled (18 px high, image incomplete); **that incomplete-load sample was not accepted**. Repeating on fully loaded pages passed all checks with process exit code 0. Desktop/mobile screenshots were inspected.

This is Chrome browser/AX evidence, **not** a physical iPad Safari touch/VoiceOver acceptance or a universal accessibility certification. First Readings still contains the historical nine-domain header above its Bookshelf; R28's v63 correction concerns the **hand navigation**, not that independently open broader shell cleanup.

## Production and remaining boundary

Public `https://fountain.coach/` still returned the old portal (HTTP 200, 18,449 bytes); public `https://benedikt-eickhoff.de/` still returned an HTTP 308 redirect to `https://works.benedikt-eickhoff.de/`. Neither host, DNS, TLS, publishing receipt, mail record nor public source has been modified by this private-WLAN correction. Reframe ADR-008's two-domain same-source publication remains an independent open work item.
