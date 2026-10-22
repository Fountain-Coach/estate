# EstateShell visual acceptance — native Apple simulators

**22 October 2026 · Author-facing WLAN staging · VISUAL ACCEPTANCE FAILED**

## Tested artifact, not an inferred preview

- Logical environment: `fountain-coach-estate-wlan-staging` (existing Ubuntu Mac mini).
- Current entrance: `http://benedikt-Macmini.local:8200/estate/`; direct-IP fallback `http://192.168.8.50:8200/estate/`.
- Existing service: `fountain-shell-acceptance-preview.service` (active).
- Observed active symlink: `/home/benedikt/estate-shell-acceptance-staging/current -> releases/shared-shell-20261022-v9-local-links`.
- Shared shell version in served HTML: `fountain.estate.shell.v1-candidate-20261022`.
- This is a WLAN-only acceptance preview, **not** a public release and **not** Fountain Press Linotype's book compositor.
- **No staging source, server program, Caddyfile, DNS, symlink, public site or protected media was changed** during visual inspection.

## Native simulator evidence

Native Safari screenshots from **Apple CoreSimulator**, not Chrome. Captures are cropped solely to remove unrelated browser chrome; website pixels are unchanged.

| Device and orientation | Visual evidence | Inspection |
| --- | --- | --- |
| iPad Pro 13-inch (M5), iOS 26.5, portrait | [Masthead and reel](evidence/ipad-portrait-estate.png) | The publisher identity is confined to a narrow utility strip; tiny icon-only navigation competes poorly with the much stronger editorial heading. |
| iPad Pro 13-inch (M5), iOS 26.5, landscape | [Actual footer in Safari](evidence/ipad-landscape-footer.png) | Four legal/provenance regions collapse into a low-contrast strip of small labels and copy despite generous screen width. |
| iPhone 17, iOS 26.5, portrait | [Actual footer in Safari](evidence/iphone17-portrait-footer.png) | Two cramped columns with diminutive copy and closely spaced legal links; the editorial content above is notably clearer. |

## What passed, what did not

**Source:** served HTML contains one shared masthead, the declared editorial reel and one footer with four semantic slots. The served CSS defines a 40px publisher logo, fixed 44px reel cells with visually hidden labels, 10px footer headings, and 12px footer body copy. Many `!important` rules compensate for domain style collisions. Those are facts from the current stage, not proposals to add more overrides.

**Existing structural tests:** the October 22 source records passing shell structural tests and Chromium comparisons. These check technical parity, not editorial composition or full native WebKit acceptance.

**Native simulator visual:** actual iPad and iPhone Safari screenshots were captured at the existing stage address. iPad landscape footer and iPhone portrait footer were reached in Safari. This does not claim full keyboard, touch, accessibility, link destination, media, deep-route, or physical iPad author acceptance.

**Decision: VISUAL FAIL.** The publisher identity, nav and legal imprint have insufficient hierarchy and legibility compared with the editorial page. The four-slot footer is semantically present but not composed as a convincing publisher's imprint.

**Public production:** no change and no production acceptance claim.

## Single-source correction, not a new service

1. Strengthen the actual common masthead's logo/wordmark/edition hierarchy, safe-area and baseline; retain the published mark.
2. Make the nine editorial destinations and Info genuinely legible and touchable across iPad and phone—not default unlabeled miniature icons. Status stays legal/footer only.
3. Recompose the same four *required* footer slots with measured typography, contrast, spacing, legal links and source credit. Do not create a second navigation menu.
4. Consolidate conflicting `!important` CSS into one source-owned, versioned EstateShell implementation. Preserve Teatro Stage, First Reading Linotype reader, site CSP and private Satzfunk media.
5. Re-render with native iPad portrait/landscape and iPhone; accept only after source/geometry/interactions and author review. Public release, if separately authorized, still requires a separate EstatePublisher terminal receipt and public HTTPS evidence.

**FCIS non-invention:** no additional server, service, agent, signing system or framework is justified by this visual failure.

## Rollback and state

The active staging release remains `shared-shell-20261022-v9-local-links`; no new candidate was activated, so no rollback was needed. Any later visual revision must preserve this predecessor and be compared against it at the same viewport.
