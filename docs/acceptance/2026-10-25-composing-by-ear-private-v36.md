# Composing by Ear — private sound-and-MIDI 2.0 composition, EstateShell v36

**25 October 2026 · Owner-WLAN immutable stage, actual audio execution separately witnessed. No public promotion.**

## Author intention and source ownership

The author asked to create **composing by ear**, not a teaching/pronunciation assessment: original Sing material listens into a second sound through Ear → source-owned MIDI 2.0 → actual Csound Teatro, with an independent output listening witness and an audible comparison.

- Original source owner: `Fountain-Coach/teatro.fountain.coach@42fe7fc8d7864c6c9f5fbf14ddfc44f41c953729` implements the exact private browser loop; `Fountain-Coach/teatro.fountain.coach@0efbd7005ba620f66b0620c8a22b509db7f66f43` repairs only source-owned mobile audition wrapping/rebuild safety.
- Original Sing source WAV, never copied into staging: SHA-256 `1d285c6b0a9dd2f7b7be58aac1509b5f55bcac5e3636c530cbec25f20db8f505`; 48kHz/5.2s mono, 249600 frames. The original Teatro Ear worklet digest `4f1d800fd5518975c0bc98a5fb0ace93eaa726d8731bf330a8eff59a9d115427` was exact-extracted from existing `site/assets/book-csound-host.js`. Neither original entered this stage or a public repository.
- Existing `book-midi2.mjs` 64-bit Channel Voice Universal MIDI Packets, group0/channel0/controller74 with 32-bit controller values. Original Csound browser WebAssembly worklet `BookCsoundHost`, existing `wind_mix` port. There is no new MIDI bus, DAW, third-party voice renderer or fallback synthesizer.

## Independent Mac original execution witness

The run was executed in genuine local Chrome against the exact original Sing WAV and Csound/Ear source worklets, with fresh isolated browser documents for control and composed audition. The source check and browser acceptance passed without browser script failures.

- **Source Ear:** 488 real acoustic windows.
- **MIDI 2.0:** 61 validated, accepted controller UMP events from source Ear; 61 actually applied to Csound's `wind_mix` on the composed run; zero changes on the control run.
- **Csound output Ear:** approximately 563 measured windows. Separate real Csound output PCM captured in both runs, 48kHz stereo, ~5.957s each, both audio contexts closed.
- **Acoustic result:** raw measured output RMS control 0.0001824954; composed 0.0005228742; **2.865136×**. MIDI 2.0 backpressure drops and refused packets zero.
- Csound is deliberately quiet: an equal 120× linear multiplication was applied to both *after* measuring the raw output to make the audio listenable without clipping. Two true AAC/M4A derivatives were made by macOS `afconvert`. The WAV evidence and acceptance JSON remain private in the Mac /tmp experiment fixture and are not hosted on the estate.
- The physical-link boundary is explicit: **this is the existing in-browser MIDI 2.0 UMP event plane**, not witnessed external or native hardware MIDI delivery. Ear measured RMS, not detected pitch/phonemes; shipped note48 is a placeholder. The Csound output was only independently *observed*, not fed back into the controller.
- The global Teatro `npm run check` did **not** pass because its existing Fountain Press shared-identity check refers to a missing `/Users/benedikteickhoff/fountain-press/runtime/identity-circle.css` path. No workaround or hidden success claim; the new scoped Python/JS syntax checks and the independent real-browser end-to-end proof passed.

## Canonical registered private WLAN stage: v34 → v35 → v36

The authoritative WLAN preview remains the **same** existing `MacMiniDocker` EstateShell service on `192.168.8.50:8200`, not a new server. The existing `serve_shared_shell_preview.py` refuses source WAVs and serves AAC byte-ranges. Production DNS, Caddy, and all other services remain unchanged.

1. Observed predecessor **v34** `shared-shell-20261025-v34-ear-sing-dark-9f49cc1` with active service and pinned source lock. Cloned immutable v35 `shared-shell-20261025-v35-composing-by-ear-42fe7fc`. Native verifier compared the full staged tree: **994 pre-existing files unchanged**, 3 new experiment files (one HTML, two AAC), **only source-lock.json modified**, no deletions; existing original essay/Teatro front-door routes retained. Native `inspect()` accepted and all HTTP SHA readbacks matched. v34 remains retained.
2. Fresh actual Mac Chrome public-view simulation on the new WLAN page at desktop and iPad portrait successfully decoded both AACs; the 390px profile exposed a 142px horizontal overflow from the long visible Sing SHA. This was a **real visual defect**, not author-approved.
3. Owner fixed only `code{overflow-wrap:anywhere;word-break:break-word}` in its source template and committed `0efbd70`. The rebuilt v36 candidate `shared-shell-20261025-v36-composing-by-ear-mobile-0efbd70` was cloned **from actual v35**, changing only the static HTML and `source-lock.json`. An independent host-side comparison witnessed **996 byte-identical files**; both AAC files retained their original v35 SHA-256. The new HTML matched the source template exactly, retaining every other textual/media byte.
4. Host native `inspect()`, four-file/then two-file stage inventories, atomic `current` activation and existing `fountain-shell-acceptance-preview.service` restart passed. Verified current symlink v36, active service, previous immutable v35 retained for rollback.
5. Actual HTTP GET from the Mac verified v36 HTML SHA-256 `41b7469740f45ec7e6ca38bf36cca7126c311e50d52d284a0b9f0c3a0412a6cf`, `csound-control.m4a` SHA-256 `d8a02db7222b25a0dd886c355b23d75b4ba9a38190cf6da622cc80961cee8b27`, `csound-by-ear.m4a` SHA-256 `48afe2ca50be06da1a5276413a9b368ca58ff23a826310400462907585bc28e0`. The actual byte-range response returned **HTTP 206** with `Content-Range: bytes 0-31/85074`, `Content-Type: audio/mp4`, and noindex header. `source-lock.json` remained private (HTTP 404). The public HTTPS route remained 404.
6. A second independent **actual HTTP browser run with no injected CSS** passed desktop dark (1280px), iPad portrait-sized dark (820px), narrow mobile dark (390px) and desktop OS-light. **Zero horizontal overflow**; both AACs loaded with metadata duration ~6.016s (container/priming), remained paused by default, and both were played using the browser audio decoder at the iPad-size view. No JavaScript or HTTP media failures. This is **Chrome browser emulation of an iPad viewport**, not a claim of physically tested iPad Safari.

## Current private listening address

`http://192.168.8.50:8200/teatro/experiments/composing-by-ear/`

At this URL, the reader gets original unmodulated Csound and Ear-modulated real Csound audio, their measured ratio, source/time identity, no autoplay and explicit limitations. It is a **private static audio audition** on the owner WLAN, not a live browser-Csound performer on iPad, a new public Teatro edition or a launched SatzfunkPlayer edition. The existing SatzfunkPlayer source-bound listening adapter was not copied/reimplemented; composing source can become a later admitted editorial source.

Status: **PRIVATE STAGING ACCEPTED, NOT PUBLIC, NO PHYSICAL MIDI 2.0 HARDWARE CLAIM**.
