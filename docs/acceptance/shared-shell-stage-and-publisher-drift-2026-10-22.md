# Shared EstateShell acceptance: local WLAN stage and native publisher ownership drift

**22 October 2026 — bounded implementation evidence, not production publication.**

## Results of the bounded cut

We implemented the **same source-owned chrome** (masthead, one nine-item editorial reel with Info, and one four-slot legal/provenance footer) around **two authentic, already-public source pages** without replacing their work content.

- Staging URL: `http://192.168.8.50:8199/estate/`, linking to `http://192.168.8.50:8199/solstice/`. These are LAN-only, `noindex` and `no-store`.
- Ubuntu user service: `fountain-shared-shell-browser-stage.service`; current immutable stage release `/home/benedikt/estate-shared-shell-staging/releases/20261022-v4`, with earlier `v1`–`v3` retained for comparison and rollback.
- Source snapshot HTTPS body SHA-256: `fountain.coach/` `deee2ab39eac56511989f624911e3274db1aba657c197ce235f82a3353b13ca9`; First Reading `3faddbff97117fbe4e528ead6b714a093932d6f425806517d9c0ee8c18fb0e09`.
- Shared CSS SHA-256 on both Ubuntu hosts: `23b626c94a31433da658b01cf9a4dadb06b859d4c5fb7e50e41657a5d70f72bd`. Original site masthead PNG SHA-256: `8c5fad1c3db56138d5959da75991dc8034a0be537ce46da6ffcc0d9655e7f729`.
- `scripts/estate_shell.py` returns the source body digest unchanged, including First Reading's `book-toc-button`, `book-type-button`, `book-prev`, and `book-next` identities.
- Local tests: 15/15 `scripts/test_shared_shell_acceptance.py`; 13/13 `scripts/test_shared_shell_release.py`. A separate portable demonstration proved 15/15 negative/positive Python tests and eight in-memory Chromium viewport checks, though its CSP had been altered solely for that isolated offline rendering.
- Headless Mac Chrome observed both real LAN pages at 1280 x 900. The first stage had an **incorrect stylesheet URL** and was visibly malformed; the second exposed Solstice's *correct* strict Content Security Policy, which blocked off-origin CSS/JavaScript. These were corrected in `v3` and `v4` by locally mirroring **45 unchanged publicly accessible Solstice CSS/JS/JPEG assets**, approximately 6.69 MB, with per-object SHA-256 provenance in `capture-lock.json`. CSP was **not weakened**.
- One upstream script, `https://works.benedikt-eickhoff.de/assets/estate-shell-state.js`, returned 404 at capture. Do not infer it has working remote behavior. Both sites' content sources and web production remain unchanged.
- The original Fountain Coach mark was taken from the public site and stage-tinted for sufficient visibility, **not invented by an image model**.

## Critical EstatePublisher owner mismatch

An independently checked Mac worktree at `midi2-gpu-fabric` old commit `c0f86086` contained `apps/estate-publisher/`. We wrote `EstatePublisherSharedShellAcceptance.swift` and 11 XCTest positive/negative cases, added a read-only `--shared-shell-observations` option to its `EstatePublisherScenarioRunner`, and expanded preview scenario evidence requirements. `swift test --filter EstatePublisherSharedShellAcceptanceTests` passed **11/11**; the earlier preview declaration test also passed **1/1**. Native scenario CLI accepted a **synthetic nine-site positive fixture** while rejecting a deliberate footer defect (nonzero exit) without granting public release.

**Do not merge or advertise these as the GitHub main's EstatePublisher implementation.** The current authoritative GitHub main of `Fountain-Coach/midi2-gpu-fabric`, `22f2f4a15c38e54066bc54743d106455ab963986` at inspection, no longer contains `apps/estate-publisher/` (the old working copy's `origin` still targeted retired Hetzner Git, whose history diverged sharply from GitHub). A cherry-pick was tested and **aborted on modify/delete conflict** to avoid silently resurrecting a removed subsystem. The native changes therefore remain a porting candidate, **not current production/mergable GitHub-main source**.

The current source owner must be identified **before** promoting the native publisher gate. Preserve the tested patch as reference only until an actual current EstatePublisher owner and executable runtime are determined.

## Remaining acceptance / release blockers

1. Only **2 of the nine domain roots**, no required deep routes, are inside this new full-shell LAN stage. Teatro/Satzfunk and the remaining sites are still unverified for common masthead/footer.
2. No native iPad Safari user acceptance, no full CSP/AX interaction readback of all domains, no real footer Info/reader interaction acceptance.
3. No typed current-owner EstatePublisher terminal admission and independent public HTTPS/DNS/TLS/rollback readback. The `satzfunk.fountain.coach` hostname and historical audio/translation release rights are still unadmitted.
4. Reframe's writer-authorized Bookshelf membership is **not** a website release, and this work neither modifies FountainStore membership nor creates any book.

**Result:** a demonstrably better, reversible local site-template prototype and an independently compiled native gate for a *different historical owner*, not a claim that the public estate is now unified.
