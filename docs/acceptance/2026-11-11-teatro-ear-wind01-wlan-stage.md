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
