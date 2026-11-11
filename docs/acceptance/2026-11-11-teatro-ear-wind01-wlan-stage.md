# WIND-01: owner-WLAN HTTPS staging, source-bound v187

**Date:** 2026-11-11. **Lane:** existing canonical `estate-shell-acceptance` staging on Ubuntu Mac mini, *not* production. **Status:** candidate prepared; terminal outcomes recorded only after independent read-back.

## Writer's requested outcome

Provide a **copyable staging server URL**, not a local Mac link, for a genuinely interactive `The Ear That Learns · Two Winds` Csound browser lesson.

Proposed exact URL: `https://192.168.8.50:8243/teatro/learn/two-winds/` (owner-controlled WLAN; existing private certificate trust may be required). The sibling HTTP route, `http://192.168.8.50:8200/teatro/learn/two-winds/`, is for source readback **only**: insecure HTTP cannot run AudioWorklet on another device. Do not claim these are accessible before a terminal readback.

## Source and release boundary

- Existing active staging release independently observed: `shared-shell-20261111-v186-works-books-b8434c5`; current `source-lock.json` SHA256 `4410cd5c364d39d255bdb4447c1b8f6186fa7571c1e0b85bd1d7eff09683a135`. Prior and current services run via `fountain-shell-acceptance-preview.service` and `fountain-shell-acceptance-preview-https.service`; no new server.
- Source-owner browser implementation (private) `Fountain-Coach/midi2-gpu-fabric@af0d6f2bc4ab336306f047fa159203c2265147bf`, branch `feat/teatro-ear-wind01-browser`; Vite `apps/teatro-stage-web/dist` with four files. The pre-existing Csound WASM/AudioWorklet is reused.
- Lesson editorial owner (private) `Fountain-Coach/teatro-ear@886f12bfc3dc9e651e175eb6cc4966554f300816`, content `curriculum/WIND-01-two-winds.md`.
- One immutable staging-only candidate `shared-shell-20261111-v187-teatro-ear-wind01-af0d6f2` inherits all ~1900 files of v186, adds exactly four source-hashed files under `teatro/learn/two-winds/`, and adds one explicitly admitted `wind01V187Admission` entry to `source-lock.json`; **no existing reader/other route bytes may change**.
- Stage source and mechanism: `staging/teatro_ear_wind01_v187.py` in `Fountain-Coach/estate`, following the current v186 source-locked same-service guard chain, no Caddy/DNS/public publication. The existing Stage EstatePublisher CLI advertises direct-static *public* Caddy operation but **not** this WLAN reader's immutable source-guard activation. This task uses the already documented owner-WLAN authenticated SSH/rsync, immutable release and rollback procedure; do not mislabel its receipt as native production EstatePublisher.

## Governance reading record

- **Chapters read:** 07 bounded planning and preserving source owners; 08 source/route/acoustic/AX acceptance separation; 151 the Csound Teatro semantic authority is not a new lesson DSL; 158 decouples static serving from remote Store, and calls for source-bound immutable release with independent readback.
- **Forbidden:** replacing the production-derived Fountain Press reader, altering other staged works, a new audio engine/MIDI2/FCIS server, using plain HTTP as proof of browser Csound, or claiming public production from a private WLAN switch.
- **Conflict and resolution:** Stage current v186 has strict source SHA and host-specific guard extensions; a raw rsync directly into `current` would bypass those rules. Instead prepare v187 immutable predecessor-preserving bytes plus a finite route-specific inherited guard; switch only after candidate proof. Do not use the public Caddy publisher operation for this private WLAN target.
- **Excluded:** new DNS, production Caddy/HTTPS, FountainStore writes, instrument admission, new book reader, physical iPad/Safari and claims of human musical perception.

## Acceptance / rollback gate

Prepare validates the input bundle digest, exact Git SHAs, four allowed asset paths, unchanged v186 source-lock and full unchanged predecessor inventory. Inherited guard must accept existing Bookshelf/Teatro routes, new WIND-01 HTML and JS/CSS, and deny an unadmitted WIND-01 path. Activate only through the existing two stage services with atomic `current` symlink and prior release retained. The terminal receipt must include read-back of HTML SHA through **both existing HTTP and HTTPS**, exact source lock, preserved predecessor and source branch revision.

Then verify in Mac Chrome on the **real WLAN HTTPS route**: read-only page, play Wind I and II and learner wind with actual Csound output witness, Stop, nine-second completion, mobile/tablet layout and no failed assets. This is not a physical iPad Safari or subjective auditory proof. The user may then proofread/listen on their iPad after accepting the local certificate trust.

**Status:** no link should be described as staged until the active release, returned HTTP/HTTPS bytes, browser Csound and terminal receipt are verified.

## Verified terminal result — 11 November 2026

**State: ACTIVE PRIVATE WLAN STAGING.** Existing `current` resolves to `shared-shell-20261111-v187-teatro-ear-wind01-af0d6f2`, with v186 retained. Both existing services are active. Exact v187 gate accepts original v176–v186 source chain and new four-file route, and refuses an unknown WIND-01 asset. Terminal receipt: `wind01-v187-terminal-receipt.json` on the staging host, copied into this source branch as `docs/acceptance/2026-11-11-teatro-ear-wind01-terminal-receipt.json`.

**Copy link — HTTPS (Csound):** `https://192.168.8.50:8243/teatro/learn/two-winds/`. The local HTTPS certificate uses the existing owner-WLAN trust boundary. **HTTP source readback only:** `http://192.168.8.50:8200/teatro/learn/two-winds/`.

**Source:** `Fountain-Coach/midi2-gpu-fabric@af0d6f2bc4ab336306f047fa159203c2265147bf`; lesson `Fountain-Coach/teatro-ear@886f12bfc3dc9e651e175eb6cc4966554f300816`; stage procedure source in `Fountain-Coach/estate` branch `feat/teatro-ear-wind01-wlan-stage`.

**Exact independent HTTPS SHA-256 read-back:** HTML `80790cda48522d34979e9d3b657f4cd892e9bd0adf954120ecea5debe86b9638`; main JS `6092e11cbd53f5cb97b8fb5bd8e4b3c6efe48be695e16de70f20c139dc913957`; lesson JS `faf59be5daa0b79adf0abd8308879c04dd8a8b141c6d20b6860071f2f7f9db99`; CSS `a014bf1aefa43b550693746fe5ea57c5e38ff589c9bc021af652ed32aae928b0`. All match the package admission. HTTP and HTTPS both served the same original index SHA.

**Neighbor continuity:** `/estate/`, `/teatro/`, and `/teatro/experiments/classic-techno-deck/` all returned HTTPS 200 after v187 activation. The source-guard checked the inherited v186 full file inventory byte-for-byte.

**Independent browser acceptance:** actual Chrome on macOS arm64 accessed the **real WLAN HTTPS route** (not localhost); the secure-context flag was true. All four app HTTP requests returned 200, no page errors or failed assets. Wind I, Wind II, and the learner-scaled wind were each started through page buttons, and the existing Csound analyser returned a non-silent/non-clipping signal witness. Learner control at 79%, editable verbal score, stop/silence, 1150px desktop and 820px touch/tablet-emulated layouts verified; neither overflowed horizontally.

**Do not overclaim:** Human musical evaluation of whether the winds are distinct, native physical iPad Safari/VoiceOver, certificate trust on that iPad, FCIS/MIDI2 peer transport and public production remain unverified. No production deployment, new server, FountainStore write or native EstatePublisher production receipt occurred. This was the already documented owner-WLAN staging lane with immutable rollback, not the public Caddy publishing operation.

**Next action:** author auditions Wind I / Wind II on an actual iPad in the registered WLAN and provides musical/gesture feedback. Do not spend this phase on Fountain Host.
