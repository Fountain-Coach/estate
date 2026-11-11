# WIND-01 auditory correction — private WLAN stage v188

**Date:** 2026-11-11. **Task:** correct the writer's audible rejection of the first two wind gestures. The goal is an actually perceptible musical distinction and a learner slider that affects the currently playing sound.

The writer heard **no difference**, perceived no effect from the control, and instead heard a repeating railway-like `ta-ta-tam tam` rhythm. This **fails** the first lesson's musical/educational acceptance despite v187's successful non-silent Csound signal witness.

## Source of failure and correction

Source inspection found the specific UI bug: `Wind01Lesson.tsx` captured `amount` at Play and never read subsequent slider changes. Separately, the generic Csound stage orchestra had a prominent shared low-frequency texture with its own `rspline/randi` modulations and only a faint turbulence-dependent voice.

The correction uses the existing `BrowserCsoundRuntime(context, WIND01_ORCHESTRA)` injection point. Its lesson-only voice has **no independently timed mechanical modulation**; it uses the same `@csound/browser` AudioWorklet and the already-authored two-gust envelope, with explicit upper-frequency noise balance responding to `turbulence_mix`. `amountRef` is read on every 85ms gesture tick, so the learner can now modify the sound **during** playback. The generic Teatro stage orchestra remains untouched.

**Source owner:** `Fountain-Coach/midi2-gpu-fabric@13a798086a5b75fbded189ae7510d8e76bceb551` (branch `feat/teatro-ear-wind01-browser`). The lesson text remains `Fountain-Coach/teatro-ear@886f12bfc3dc9e651e175eb6cc4966554f300816`.

## Real browser acoustic comparison — not a hearing claim

Chrome on macOS running the local Vite client instantiated the new lesson Csound WASM/AudioWorklet. An actual analyser captured ~95 100ms frames per gesture, using 2048-point FFT power from 1700–5000Hz divided by 120–950Hz:

- **Wind I, 2.8–3.7s:** ratio 0.884; **Wind II:** 3.234. Distinct high-frequency power, not merely channel-value differences.
- **Wind I, 5.9–6.9s:** ratio 0.802; **Wind II:** 3.187.
- **Learner gesture during the same nine-second playback:** changing from 0% to 100% after 3.4s changed the measured high/low energy ratio from 0.750 (2.8–3.7s) to 1.796 (4.2–5.6s) and 3.040 (5.9–6.9s).
- Zero captured browser errors. Unit suite: 29 passed, 1 previously skipped. Vite production build passed. The author has **not** yet heard or approved the revised sound.

The measured frames and method are recorded in source `apps/teatro-stage-web/docs/wind01/audio-contrast-v188.json`. These are **spectral contrast observations**, not a perceptual test, a tinnitus remedy or a claim of naturalistic acoustic quality.

## Proposed staging change

**Existing active stage:** `shared-shell-20261111-v187-teatro-ear-wind01-af0d6f2`, existing owner-WLAN `192.168.8.50` port 8200 HTTP and 8243 HTTPS, with source-lock SHA256 `b195123e9c430b821ea69f61a174d3c52aff533422e6e2d504a117742b049bd6`.

**New immutable release:** `shared-shell-20261111-v188-wind-gestures-13a7980`. It replaces only `teatro/learn/two-winds/index.html` and adds the two new content-hashed JS files. It preserves all v187 old JS/CSS files and every existing Estate/Teatro/Bookshelf route. One source-lock entry `wind01V188AuditoryCorrection` records the author report and exact new assets. The inherited v187 gate and v186... original readers stay authoritative.

**Actual browser link after activation:** `https://192.168.8.50:8243/teatro/learn/two-winds/` (WLAN private certificate required). Never call this corrected until the new active release, full exact-asset SHA readback, existing neighboring route preservation and **real HTTPS browser Csound contrast** are separately verified.

**Publisher procedure:** `staging/teatro_ear_wind01_v188.py` extends the current checked-in v187 staging procedure and rollback; no new server, user authentication, DNS, public Caddy, FountainStore, ChatGPT/MCP, independent synthesizer, or score rendering. The public static EstatePublisher CLI is not the executor for this existing private source-guarded WLAN stage.

**Governance record:** Ch. 07 scoped source-first remediation, Ch. 08 explicitly downgrades the previous output-witness claim in light of failed human hearing, Ch. 151 retains the native Csound/Scenario boundary, Ch. 158 preserves source-bound immutable static staging. **Forbidden:** treating spectral data alone as proof of an audible lesson, wiping the failed v187 release, changing unrelated works, or production promotion. **Conflict:** automated v187 Csound non-silent checks versus user's actual "can't hear difference" report; the latter governs acceptance. **Excluded:** FCIS, MIDI2, engraving, hardware iPad audit until the two sound gestures themselves are worth teaching.

**Terminal result:** pending, to be appended only from release and HTTPS acceptance evidence.

## Staging defect discovered independently — retained CSS HTTP 403

The first v188 terminal receipt proves the new HTML and JS assets, but a separate four-asset HTTPS readback found that the **unchanged v187 CSS was rejected with HTTP 403**. The immutable v188 release contains the exact correct CSS bytes `a014bf1aefa43b550693746fe5ea57c5e38ff589c9bc021af652ed32aae928b0`; the defect is in the generated v188 handler, which checked only new/changed file digests and refused every other `teatro/learn/two-winds/` path before asking the inherited v187 guard.

**Finite repair:** remove this incorrect blanket refusal. Delegate unchanged older CSS and hashed JS to the v187 source guard, which already verifies exact byte identity and refuses unknown paths. Keep the v188 source-lock and immutable release unchanged. The checked-in `teatro_ear_wind01_v188.py repair-css-guard` operation requires the exact active release, admission and previous guard SHA, verifies the candidate without modifying the serving script, writes a backup, swaps only the external service guard, restarts the existing HTTP/HTTPS services and requires independent CSS+HTML+JS byte readback; on error it restores the previous guard. It records its own append-only terminal receipt. **Do not claim this defect corrected until that receipt and a full browser test pass.**

## Terminal verification — correction accepted technically, pending author hearing

**Active private WLAN stage:** `shared-shell-20261111-v188-wind-gestures-13a7980`; immutable release content and original source-lock unchanged. The preceding `v187` remains for rollback. The source-owned corrected guard is in `Fountain-Coach/estate` branch `feat/teatro-ear-wind01-wlan-stage`, with the original rejected-CSS guard retained as a nonserving backup. The corrected guard returns control to the v187 predecessor for old stylesheet/JS assets and still refuses unknown routes.

**Terminal receipts:** `2026-11-11-wind01-v188-terminal-receipt.json` establishes exact stage activation and source hashes; the separate append-only `2026-11-11-wind01-v188-css-repair-terminal-receipt.json` establishes the subsequent guard correction. Both CSS and HTML and the new lesson JS were independently served with HTTP 200 and pinned SHA on **HTTP 8200 and HTTPS 8243**; the retained CSS SHA stayed `a014bf1aefa43b550693746fe5ea57c5e38ff589c9bc021af652ed32aae928b0`. No current release root files were rewritten to repair the serving guard.

**Live stage browser acceptance:** Mac Chrome on the real WLAN HTTPS route, 1150px desktop and 820px tablet-sized emulation, loaded the exact four assets HTTP 200, no request/page errors, `window.isSecureContext=true`. Three actual `@csound/browser` auditions passed their output witness, learner adjustment (79%) and verbal-score writing operated, and Stop returned silence. CSS was verified to load and both layouts had zero horizontal overflow. JSON evidence: `docs/qa/wind01/2026-11-11-v188-live-https-ui.json`.

**Live stage *acoustic contrast* acceptance:** Csound AudioWorklet's output analyser, captured in-browser over this HTTPS URL, measured a spectral high/low power contrast ratio between Wind II and Wind I of **4.42× at the first gust and 4.41× at the second**. Changing the learner control from 0% to 100% **while sounding** changed the spectral ratio by **3.33×** between the sampled sections. The underlying 95 frames per audition, frequency bands and independent validation are recorded in `docs/qa/wind01/2026-11-11-v188-live-https-acoustic.json`. These numeric tests demonstrate real audio behavior rather than merely a moving slider, but they do **not** replace a human perception test.

**Copy link:** `https://192.168.8.50:8243/teatro/learn/two-winds/?rev=188`. Browser address resolves on the owner WLAN and its certificate remains privately trusted. **Still pending:** the author listening on their actual device and judging whether Wind I/II are clearly different, whether the mechanical train-like pattern is absent, and whether the revised gestures deserve to teach. Native iPad Safari audio/VoiceOver and public production are not claimed. FCIS Fountain Host remains deferred.
