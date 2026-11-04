# HTTPS preview shares the existing Reader provenance guard

Observed 4 November 2026 while staging the figure-balanced essay. Owner-WLAN HTTPS service `fountain-shell-acceptance-preview-https.service` on 192.168.8.50:8243 used the existing `SecureStageHandler` derived from the HTTP `Handler`, but constructed it without the required `reader_gate` keyword. After the November 4 HTTP source guard was installed, HTTPS returned HTTP 403 `Reader provenance guard not installed` for an otherwise valid v142 page. The failed v143 guard installation automatically restored the previous guard; v142 remained active.

Correction: preserve the existing HTTPS entrypoint, SSL context, routing and MP3 byte ranges. Initialize the very same `ReaderProvenanceGate` against the accepted immutable v140 baseline and the current source-locked staging root, pass it to `SecureStageHandler` via `partial`, and check it before all requests including the custom MP3 range branch. No second permission authority, server, renderer, publication transport or new domain is created.

Tests: three local HTTP adapter tests verify 200 for admitted page GET/HEAD, 403 for invented Reader GET/HEAD, 206 correct bytes for the existing recorded media range, and fail-closed 403 when guard is missing. Additionally, 14 source guard tests remain valid. Running TLS service and source digest must be separately read back before claiming this correction is deployed.

Target stage remains the accepted owner-WLAN HTTPS service; active release must first be v142 and existing HTTP must be independently preserved. After guarded HTTPS works, source-bound v143 may be activated through the existing atomic symlink and rollback path. Public production is not part of this operation.
