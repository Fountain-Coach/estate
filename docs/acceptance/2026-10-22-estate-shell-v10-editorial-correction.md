# EstateShell v10 — editorial correction and WLAN acceptance

**Date:** 22 October 2026  
**Scope:** the existing author-facing Ubuntu staging environment, not public production  
**Source revision:** `feature/estate-shell-editorial-20261022`  
**Shell version:** `fountain.estate.shell.v2-editorial-20261022`  
**Active staged release:** `shared-shell-20261022-v10-editorial`  
**Retained rollback:** `shared-shell-20261022-v9-local-links`

## Fixed, rather than worked around

The [native iPad/iPhone proofreading audit](2026-10-22-estate-shell-simulator.md) rejected the previous thin masthead, nine tiny unlabeled icons and cramped four-column legal footer. The redesign operates **inside the existing source-owned shared EstateShell**, keeping the same publication identities, real publisher mark and four semantic footer slots.

- Publisher masthead and wordmark now have measured proportions and adequate spacing.
- All nine editorial reel destinations plus Info have visible text, appropriate responsive grouping and touch-sized controls.
- The footer has readable text, a stronger imprint, source/provenance, legal/access/Status, and truthful staging status.
- Conflicting legacy selectors `.estate-nav` and `footer[role="contentinfo"]` were removed **from the new shell projection** rather than adding more `!important` overrides. The top-level `footer` retains native contentinfo landmark semantics.
- Original Estate, Teatro and First Reading editorial bodies, artwork, reader controls, private archive boundaries and source rights remain independent and unchanged.

## Evidence from the actual change

- 16 structural and negative-tests in `test_shared_shell_acceptance.py` passed.
- 13 shared-release positive/negative tests in `test_shared_shell_release.py` passed.
- `check_shared_shell_release.py` passed for the 3 generated domain pages, shared CSS/logo, declared LAN bindings, active identity, Info and legal Status.
- `test_shared_shell_browser.py` passed 12 browser cases: three sites × four sizes (desktop, iPad landscape, iPad portrait and phone portrait), with zero new errors. These test actual rendered geometry, visible labels, legible footer font size, touch heights, Info scroll and retained Teatro canvas / First Reading controls.
- Source SHA-256 identities match the original v9 staging receipts:
  - Estate: `deee2ab39eac56511989f624911e3274db1aba657c197ce235f82a3353b13ca9`
  - Teatro: `71308fe02d4df6e0237884aeccccd8b040c0df2d32e2ea05e4243f93a008d996`
  - First Reading: `3faddbff97117fbe4e528ead6b714a093932d6f425806517d9c0ee8c18fb0e09`
- One First Reading source image timed out during source fetch. Its unchanged 133,595-byte public file was restored from the retained v9 staging release and independently matched its SHA-256 `d896e49fab8b9de64fe6d216ec3749127e52909b29a260fae285c6755e0966f7`.
- All 65 new staging files passed **host-side** SHA-256 readback. Their directory is immutable by release convention and remains distinct from v9.
- The first switch initially failed a too-early HTTP check and automatically rolled back to v9. The bounded readiness retry activated v10 and independently read back HTTP 200 + the exact v2 marker at `/estate/`, `/teatro/` and `/solstice/editions/first-reading/`.
- Native iPad Pro 13-inch (M5), iOS 26.5 Simulator Safari rendered the v10 entrance in portrait and landscape. This is not the same as a physical iPad author approval or a complete cross-domain native-device acceptance.

**Known unrelated item:** the existing source-owned First Reading toolbar has an 8-pixel overflow at phone width. This is not an EstateShell change; do not alter the book compositor to hide it.

## Exact viewing URL

[EstateShell author-facing WLAN stage](http://benedikt-Macmini.local:8200/estate/)  
Fallback `http://192.168.8.50:8200/estate/`

The preview is an author-controlled WLAN service, not a public DNS release. Satzfunk remains an authenticated private archive; no private media is copied into the static preview.

## Limits / stop conditions

This evidence proves source preservation, structural/browser regressions, native Safari rendering of the entrance and a staged HTTP release, **not production acceptance**. Full device interactions, legal links, editor proofreading of the revised imprint and a separately authorized EstatePublisher production receipt remain distinct gates. No new staging server, enrollment system, remote helper, GitHub CI or FountainStore dependency was introduced.

**Rollback:** restore the previous `current` symlink target `releases/shared-shell-20261022-v9-local-links` on the existing Ubuntu stage and restart its existing preview service if the author rejects v10. Preserve both immutable release trees and their source locks.
