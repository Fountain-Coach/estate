# Read-only WLAN stage baseline — 28 October 2026

**Status: OBSERVED read-only baseline, NOT the author-led release.** No production, source-owned article or stage symlink was changed during this inspection. The canonical service is the registered `fountain-shell-acceptance-preview.service` at [owner-WLAN entrance](http://benedikt-Macmini.local:8200/estate/) with direct-IP fallback `http://192.168.8.50:8200/estate/`.

The actual `current` symlink returned `/home/benedikt/estate-shell-acceptance-staging/releases/shared-shell-20261028-v56-modell-wirklichkeit-e3753d7` on 28 October 2026. The prior registry `observedRelease=v50` was therefore **historical**. The currently retained rollback identity was **not independently inspected**.

## Actual private HTTP readback

Nineteen explicitly named URLs were inspected using the connected authorized Mac's read-only remote URL mechanism, without substituting public production for the private stage. The rows below describe what was returned; **HTTP status is not independently recorded** by this read API, so they are HTML-body observations rather than typed EstatePublisher delivery receipts.

| Route (under `http://192.168.8.50:8200`) | Readback | Shared header + footer | Complete nine-entry reel incl. Satzfunk and Works | Result |
| --- | --- | --- | --- | --- |
| `/estate/` | portal HTML | Yes | Yes | Baseline shell consistent; **old future-facing homepage, not approved editorial change** |
| `/estate/essays/` | Essays catalogue HTML | Yes | Yes | Shared shell present |
| `/estate/essays/the-door-is-a-score/` | complete authored essay HTML | Yes | Yes | Preserve in new candidate |
| `/estate/essays/the-composable-book/` | complete authored essay HTML | Yes | Yes | Preserve in new candidate |
| `/book/` | Book public projection | Yes | Yes | Shared shell present |
| `/book/commands/` | URL read returned an error | Unknown | Unknown | Exact route not confirmed, **not 200 proof** |
| `/governance/` | current Governance root | Yes | **No, only eight: missing Satzfunk** | Defect |
| `/governance/chapters/92-fountain-coach-publication-estate/` | full chapter | Yes | Yes | Deep route proof |
| `/instruments/` | instrument catalogue | Yes | Yes | Shared shell present |
| `/midi2/` | MIDI2 documentation | Yes | Yes | Shared shell present |
| `/status/` | public status root | Yes | **No, only eight: missing Satzfunk** | Defect |
| `/status/for-agents/` | agent documentation | Yes | **No, only eight: missing Satzfunk** | Defect |
| `/teatro/` | existing Fountain Press Bookshelf | **No** | **No** | Defect; preserve distinct Bookshelf/engine |
| `/teatro/editions/` | existing Bookshelf | **No** | **No** | Defect |
| `/teatro/editions/first-hearing/` | real Linotype sound/reading UI | **No shared header/footer** | **No** | Defect; preserve source-bound reading and mixed media |
| `/works/` | author Works, complete | Yes | Yes | Shared shell present |
| `/works/bewerbung/` | Modell und Wirklichkeit | Yes | Yes | Shared shell present; German legal routes retain local authority |
| `/solstice/editions/first-reading/` | real paginated First Reading | **No shared shell** | **No** | Defect; preserve source-owned reading experience |
| `/pointer/` | Works pointer projection | Yes | Yes | Legacy alias observed, not a separate front door |

The nine identities in the currently working shared reel are `Estate, Book, Governance, MIDI2, Instruments, Teatro, Satzfunk, Works, Solstice`. `Info` is a separate local action. The formerly checked-in `Pointer` reel entry is stale; the editorial branch reconciles it to Works, while the personal pointer domain remains separately meaningful. Company Status remains footer-only.

## Editorial candidate, source and stage remain distinct

The user-approved new homepage and complete Essays collection are committed in `Fountain-Coach/fountain.coach` on `editorial/2026-10-28-author-led-estate`. The estate branch with the same name records the current reel, routes, full static-source inventory and route-audit code. This new candidate has **not** replaced the old portal at the active WLAN entrance. The two newer published essays exist in both public HTTPS and active private WLAN, but their full HTML/media are absent from the older Git-tracked Fountain Coach source snapshot and must not be deleted during source-to-stage composition.

The existing `scripts/audit-editorial-shell.py` supports a machine-readable JSON verdict **and** complete human-readable per-route table in source mode and active WLAN mode. The full 325-route run and visual iPad/Safari/AX proof have **not** been executed. A handful of header comparisons are not represented as universal estate acceptance.

## Operations attempted and not completed

The connected Mac was observed online, and an initial read-only SSH action resolved the live `current` symlink. Subsequent remote terminal/process actions were rejected by OpenAI safety checks, including commands with no side effects. Consequently no authorized EstatePublisher artifact delivery, typed terminal stage receipt, independent full browser acceptance or atomic `current` switch was obtained. The attempt stopped without replacing the active release, installing an alternative publisher, or copying data across source-authority boundaries.

**Stage promotion requirements still outstanding:** independently capture/pin current affected public production routes and complete media, pin source commits, reconcile accepted v56 stage-only changes, run local owner-scope checks, run all-route structural/visual/AX acceptance, then use the existing authorized EstatePublisher SSH transport with predecessor/rollback and readback. Do not claim this already occurred.

## Source and authority

- [Editorial source branch](https://github.com/Fountain-Coach/fountain.coach/tree/editorial/2026-10-28-author-led-estate)
- [Estate candidate branch](https://github.com/Fountain-Coach/estate/tree/editorial/2026-10-28-author-led-estate)
- [Every registered source route](2026-10-28-editorial-route-register.md)
- [Stage registry](../../staging/environment.json)
- [Canonical nine-entry reel](../../navigation/canonical-reel.v1.json)
- [Current estate and founder source governance](../../AGENTS.md)

