# Governance — source-anchored illustrations in Fountain Press v163

6 November 2026. **Private owner-WLAN staging accepted; public production unchanged.**

## Exact writer outcome and reproduced defect

Writer observes missing illustrations in the complete Governance book and expects principal images to appear in authentic Linotype prose flow, with a separate source-owned social-image rule. The predecessor v162 actually retained all 70 original source image URLs and returned HTTP 200, but the shared Reader's optional source-anchor input was absent. The existing `reading-first-press-engine.js::text()` therefore repositioned every `figure.frame-reading-figure` by an even-distribution formula. In Chapter 159 the original figure appeared on **folio 4/8**, not in the chapter's first pages. Previous v162 corpus tests examined `#source-flow`, not the composed `.linotype-stage` leaves. This was an incomplete test, not a missing asset or need for a second Reader.

## Minimal source-owned correction

- `Fountain-Coach/governance.fountain.coach@03f15306a018eddd85fab491e592d2fdffd61528` — untouched canonical source, rights, route statuses and original images.
- `Fountain-Coach/fountain-press@cfc2745772c8d3ea306f86e1cae8ac53f8805a9c` — existing Governance source projector now adds `data-inline-after-paragraph` computed from the original source's preceding paragraph count, `data-source-paragraph-anchor`, stable source-image IDs and a `hero`/secondary role. A source image before its first paragraph is placed at the earliest supported in-prose anchor 1, retaining original paragraph text. No source images generated/removed; original chapter strings and all 1,132 authored links are unchanged.
- `Fountain-Coach/fountain.coach@748ba55c38e167e9de90d6ec0572191dbcafa41e` — a browser regression verifies **actual composed leaves**, not only source templates, for every chapter, with figure identity, order, role, anchor, original image URL and 159/133 first-folio cases. No modification to the existing press engine or reading controls.

## Immutable stage lineage and live acceptance

Canonical owner-WLAN staging: `https://192.168.8.50:8243/estate/#/read/governance`.

Active: `shared-shell-20261106-v163-governance-inline-hero-cfc2745`.

Previous accepted rollback release: `shared-shell-20261106-v162-governance-link-fidelity-4d6046b`, retained unchanged, with v161/v160 behind it. Fail-closed original EstatePublisher preview source-locked guard admission passed against **all 23 inherited approved deltas**, with exact change-scope analysis. The only v162→v163 modified file is `estate/index.html`, plus a new `estate/evidence/press-governance-v163.json` and new `source-lock.json`. Removing the four new source-anchor attributes on exactly 70 original `<figure>` nodes reproduces the **exact** v162 HTML, SHA-256 `35ade43f8c38ba56773e1130505d0262e11aec87b716f7d07614eebb13d7156c`. All private audio and other owner assets remain byte-identical.

v163 source-lock SHA-256: `75198bfc5ae03f75d53a5fbc9c1a69b73bde0e5d0f563863d5fe8f73b7989091`.
Independent actual HTTPS SHA readbacks:
- `/estate/`: `4c9298785fa505f8971429be9cf42b10682acc950b534194415193c87472e757`
- `/estate/assets/linotype/reading-first-app.js` (unchanged): `9fc914956045523522a1a4557721bb22a20fe995cb82f2f8c85c053f1f929f09`
- `/estate/evidence/press-governance-v163.json`: `8f0125958684dac0a9c2bf1c006f5e39b92e66b95ac43012da62c213745d871e`

**Actual live no-interception browser acceptance:** 160/160 chapter compositions, 10 complete Reader journeys, and 159/159 additional source-position scans (excluding only the initial fixture volume), with **70/70 source-authentic figures** on measured leaves (67 first-in-chapter heroes and three additional inline figures). The visible 159 image moved from folio 4 to folio 1; Chapter 133 is also on folio 1. 70 HTTP image responses were witnessed and no JS pagination errors observed.

## Separate social-publication gap

This release repairs **illustration placement only**. Source Governance OG metadata already exists on all 160 chapter routes, but **89 currently select the generic Governance estate image**, not the requested *landscape rendering of that publication's first page*. Additionally some chapters use SVG directly as `og:image` rather than a raster derivative; crawlers may not reliably accept SVG. The accepted authorial policy is: **hero = first source-admitted in-prose original image (its social derivative must preserve its identity); without an authored hero = deterministic landscape first-folio rendering**. A social release needs its own source-bundled raster, absolute HTTPS OpenGraph/Twitter card URLs on a **crawler-readable per-work static route**, alt/rights/digest metadata and independent stage crawler readback. A Reader URL with `#/read/<id>` alone cannot carry per-volume OpenGraph metadata for non-JavaScript scrapers. Do not claim this social fallback is deployed in v163 or backwrite the owner Governance site from estate staging.

**Remaining proof boundary:** no physical native iPad Safari/VoiceOver or production public release. No new original artwork was generated; this correction keeps canonical source illustrations intact.
