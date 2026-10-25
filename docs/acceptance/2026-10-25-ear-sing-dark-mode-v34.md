# Ear / Sing listening panel — dark-mode repair, WLAN staging v34

**Observed / independently checked 25 October 2026.** This is a bounded correction to the existing privately staged essay, not a public release or a general estate theme overhaul.

## Reported failure and root cause

The writer's iPad Safari dark-mode screenshot showed an almost-white player panel with nearly white headings, timestamps, buttons, commentary and input text. In the actual staging browser, **automatic** `prefers-color-scheme: dark` resolved `--ink` to `#ece7dc` and `--paper` to `#1d1b18` but left the legacy `--surface` as **light** `#f6f8fa` in the absence of an explicit `data-theme`. The original panel used `background:var(--surface)` and the selected take used `var(--surface-secondary,var(--surface))`. Explicit `data-theme="dark"` happened to work, explaining why prior light/desktop checks missed the defect.

There is no observed deficiency in the audio model, player, staging server, MIDI transport or publishing contract. The smallest sufficient correction is a **component-local dark surface token** that follows the existing estate's correctly resolved `--paper` value in automatic and explicitly selected dark mode, with a corresponding selected-tab background. The light mode retains its previous `--surface`. Reader-note placeholder text now explicitly uses the existing `--muted` token with full opacity.

## Git authority and scoped delta

- Authoring owner: `Fountain-Coach/fountain.coach@9f49cc1a9adc7a3df0597a455485f8f417286ee3` (full source code, stylesheet and regression checks).
- Changed source: `site/assets/site.css`, with matching static assertion in `scripts/verify_ear_sing_essay.py`; source inventory and edition metadata updated. The full essay, illustrations and player code remain unchanged.
- Predecessor staged release: `shared-shell-20261025-v33-ear-sing-seek-d6736cd`.
- New immutable staged release: `shared-shell-20261025-v34-ear-sing-dark-9f49cc1`.
- Live candidate delta: **only** `estate/assets/essay-site.css` and private `source-lock.json`. Full-file comparison of v33 and v34 on the Ubuntu host showed no added/deleted files and exactly those two modified paths.
- Stage stylesheet predecessor SHA-256: `ed2e6bbebe9f31c1b023b2cb9b3eda9e5477320c4cb554bfebdd0e66650c0e36`.
- New stage stylesheet SHA-256: `6aba1927f4b60e6942ee4f2f19e14ad039d0af93fa4aa1809c9b38300842c9fd`.
- Affected-scope production `https://fountain.coach/assets/site.css` baseline SHA-256: `d8a6e65183510323ebba5c45b28d8663205d55a00111b214a25b59766262e97f`; its contents were byte-preserved as the complete prefix of the staged CSS candidate. The new public essay route remained **404**, and no public promotion was performed.

## Actual stage transition and negative controls

The current registered owner-WLAN service on `MacMiniDocker`, `fountain-shell-acceptance-preview.service`, was observed active with `current` pointing to v33 before staging. The candidate was prepared by copying the prior immutable release and delivering the exact two-file CSS+lock overlay over the existing authenticated SSH/rsync transport. The overlay's SHA-256 inventory passed on the host; the existing preview server's source-lock `inspect()` accepted it. A full host-side comparison witnessed that all audio, illustration, player, other estate routes and other files stayed identical.

Activation was one atomic `current` symlink replacement followed by restarting the **existing** preview service. A bounded readiness check succeeded; an independent live HTTP readback returned the new CSS at its exact expected SHA-256 and the intact Ear–Sing article and complete Essays collection. The predecessor v33 remains available for rollback. No new hostname, helper, service, signing process, CI or source-owned audio publication was introduced.

## Independent browser visual and contrast witness

A local Mac's real Chrome browser loaded the actual WLAN route `http://192.168.8.50:8200/estate/essays/the-ear-that-learns/`. Before changing the stage, a direct computed-style witness reproduced the reported OS-dark mismatch: panel `rgb(246,248,250)`, text `rgb(236,231,220)`. The source patch was tested in the browser first, and **the same five cases were run again after the v34 activation without injecting any local CSS**:

| Mode | Actual panel surface | Text | Lowest sampled text contrast | Result |
| --- | --- | --- | --- | --- |
| System light | `rgb(246,248,250)` | `rgb(39,35,31)` | 5.03:1 | Pass; original light background retained |
| Automatic system dark, 1024 px | `rgb(29,27,24)` | `rgb(236,231,220)` | 7.75:1 | Pass |
| Explicit `data-theme="dark"` | `rgb(29,27,24)` | `rgb(236,231,220)` | 7.75:1 | Pass |
| Explicit light with dark OS | `rgb(246,248,250)` | `rgb(39,35,31)` | 5.03:1 | Pass; user theme wins |
| Automatic system dark, 390 px | `rgb(29,27,24)` | `rgb(236,231,220)` | 7.75:1 | Pass; zero horizontal overflow |

Sampled targets included the study title, take headings and controls, selected take, muted instructions, timed observations, source-data status, textarea, placeholder and copy button. The lowest dark contrast was the gold selected-tab accent, still 7.75:1; typical dark body/annotation contrast was 7.82:1. The screenshot showed a coherent near-charcoal listening panel with legible ivory text and restrained gold emphasis, matching the surrounding dark estate.

Existing source checks passed: `npm run check`, including the independent three-essay Linotype integrity and reading continuity PDF, plus the Ear/Sing source assertions. No player or audio code was modified; the previously established three-take playback, source-bound comments and byte-range seek remain the same file bytes as v33.

**Boundary:** this is a real staged browser contrast and layout witness, **not a claim of native iPad Safari execution on the writer's device**. The CSS now explicitly handles the automatic dark preference witnessed in the writer's screenshot. Public production remains unchanged.

## Current author-facing address

`http://192.168.8.50:8200/estate/essays/the-ear-that-learns/`

The writer is not required to install, publish, or run tests.
