# HTTPS preview shares the existing Reader provenance guard

Observed 4 November 2026 while staging the figure-balanced essay. Owner-WLAN HTTPS service `fountain-shell-acceptance-preview-https.service` on 192.168.8.50:8243 used the existing `SecureStageHandler` derived from the HTTP `Handler`, but constructed it without the required `reader_gate` keyword. After the November 4 HTTP source guard was installed, HTTPS returned HTTP 403 `Reader provenance guard not installed` for an otherwise valid v142 page. The failed v143 guard installation automatically restored the previous guard; v142 remained active.

Correction: preserve the existing HTTPS entrypoint, SSL context, routing and MP3 byte ranges. Initialize the very same `ReaderProvenanceGate` against the accepted immutable v140 baseline and the current source-locked staging root, pass it to `SecureStageHandler` via `partial`, and check it before all requests including the custom MP3 range branch. No second permission authority, server, renderer, publication transport or new domain is created.

Tests: three local HTTP adapter tests verify 200 for admitted page GET/HEAD, 403 for invented Reader GET/HEAD, 206 correct bytes for the existing recorded media range, and fail-closed 403 when guard is missing. Additionally, 14 source guard tests remain valid. Running TLS service and source digest must be separately read back before claiming this correction is deployed.

Target stage remains the accepted owner-WLAN HTTPS service; active release must first be v142 and existing HTTP must be independently preserved. After guarded HTTPS works, source-bound v143 may be activated through the existing atomic symlink and rollback path. Public production is not part of this operation.


## Live service readback — 4 November 2026

Source of `serve_shared_shell_preview_https.py` merged through estate PR #13 as commit `fe512bcde4c5f9795b5660b9c6479be9850e8dcc`. The **existing** `fountain-shell-acceptance-preview-https.service` script was safely backed up and replaced with SHA-256 `9a82515373dcac72283ea3f88ae520fac8400516b42b862f4e4d90d426560e92`. It now initializes and passes the same `ReaderProvenanceGate` as the HTTP preview and checks the media range path before serving.

Both existing services were restarted and independently read back against the unchanged accepted v142 Reader: HTTPS `:8243` and HTTP `:8200` each returned 200 with the exact original root HTML and app SHA, and both retained the 404 for the abandoned standalone Reader path. After the bounded v143 release switch, the same two services returned the **matching exact v143 Reader HTML** and SVG bytes, and remained active. macOS WebKit with its normal certificate validation (`ignoreHTTPSErrors=false`) successfully opened the HTTPS v143 essay. Its portrait layout returned 13 measured leaves. This is an actual browser witness, not a promise of a physical iPad acceptance.

The owner-WLAN TLS preview is not a public release; public HTTPS bytes were independently checked to remain unchanged. The original server source was retained for rollback.
