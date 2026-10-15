# Browser and server-runtime continuity evidence

**This is a static-source inspection, not an interactive browser or service test.**

The recovered public artifact has 600 byte-verifiable HTTP-200 responses and is served by Caddy on Ubuntu. That proves only the bytes. This inspection records browser API/library indicators and external HTML reference hosts; the presence of a token does not prove a working API, and absence does not prove no runtime dependency.

| Public host | Resources | Browser code indicators | Runtime accepted? |
|---|---:|---|---|
| benedikt-eickhoff.de | 23 | none detected | Not tested |
| book.fountain.coach | 54 | csound_browser | Not tested |
| fountain.coach | 26 | browser_audio, camera_or_microphone, csound_browser, fetch_api, midi_browser_api, wasm, websocket_or_sse | Not tested |
| governance.fountain.coach | 277 | csound_browser, fetch_api, midi_browser_api, oauth_or_external_identity, wasm | Not tested |
| instruments.fountain.coach | 14 | csound_browser | Not tested |
| midi2.fountain.coach | 37 | browser_audio | Not tested |
| status.fountain.coach | 22 | none detected | Not tested |
| teatro.fountain.coach | 5 | browser_audio, camera_or_microphone, csound_browser, fetch_api, midi_browser_api, wasm, websocket_or_sse | Not tested |
| works.benedikt-eickhoff.de | 142 | fetch_api, persistent_browser_storage | Not tested |

## Why dynamic recovery is not admitted

Browser MIDI, Csound, AudioContext, service workers and network APIs may require device activation, hardware permissions, audio assets, cross-domain origin policies or external services. The static archive cannot reproduce private FountainStore operations, OAuth state, authenticated services or past user data. The app/service owners must furnish independently backed runtime/service state and endpoint health contracts.

For each actual interactive service, a later acceptance test needs an independent client (including iPad for the reading/performance UX), correct canonical Host/TLS identity, permission grants and an observed end-to-end result—not only a GET 200.

Detailed per-host evidence and limited path examples are in [runtime-boundary-witness.json](runtime-boundary-witness.json). Run npm run recovery:runtime:build to refresh from the frozen public bundle, and npm run recovery:runtime:verify to detect drift without network requests.
