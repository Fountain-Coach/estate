# ADR 001 — Local Ubuntu emergency origin through an outbound tunnel

- **Date:** 2026-10-15
- **Authority:** Fountain Coach domain owner; Estate registry owns topology, individual Git repositories own content
- **Decision status:** Design direction pinned. **No implementation, authorized DNS migration, public failover, or disaster-recovery acceptance is claimed.**
- **Scope:** The full published estate, including technical and institutional domains, not only the Bookshelf
- **Grounding:** [Machine-readable estate inventory](../../inventory/CONTRACT.md), [source-route ledger](../../inventory/source-routes.json), [live HTTPS witness](../../inventory/public-readback.json)
- **Governance:** [FCIS 117](https://governance.fountain.coach/chapters/117-fountainstore-snapshot-export-and-git-recovery-projection/), [FCIS 139](https://governance.fountain.coach/chapters/139-owner-trust-root-secretstore-custody-and-recovery/), [FCIS 146](https://governance.fountain.coach/chapters/146-local-fountainstore-remote-caddy-production-estate/), [FCIS 157](https://governance.fountain.coach/chapters/157-the-writer-owns-the-public-domain/)

## Context and decision

Assume the existing Hetzner data centre and its server IP permanently disappear, perhaps including access to Hetzner DNS. We nevertheless know an **existing local Ubuntu machine connected to our WLAN** survives, outside that provider.

**Use this Ubuntu machine as the first recovery origin.** An agent with bounded SSH access can reconstruct the exact last-published public estate from its GitHub owner revisions and approved release artifacts, serve an isolated immutable static release through local Caddy, and expose that origin to the public internet over an **outbound tunnel**, initially a disposable Cloudflare Quick Tunnel. No second Hetzner VPS, publicly routable residential IP, or router port forwarding is necessary for the first proof. A named Cloudflare Tunnel with deliberate DNS authority is a later **separately authorized** emergency-routing option.

The proof is not that Caddy can serve a newly generated homepage: the objective is restoration of the **already published estate**, including editorial content, governance, technical documentation, original images, published editions, domain relationships and delegated routes.

The Ubuntu machine is a **recovery execution host**, not a publishing authority, not the origin of GitHub content, and not an independent backup of private Store/credentials. Cloudflare provides transport/public HTTPS, **not** canonical publication identity or source authority. This strategy introduces Cloudflare, the household ISP, and local power as additional dependencies. It tests survival of the Hetzner server/provider, not survival of every possible outage.

## Candidate recovery topology

```text
Owning GitHub repositories at exact LAST-PUBLISHED commits
             + Fountain-Coach/estate inventory
             + approved, hashed public-release lock
                         |
          governed agent: read/verify/assemble
             (missing materials BLOCK, never invent)
                         |
             immutable recovery release
                  on local Ubuntu
                         |
                isolated local Caddy
                  (static sites/files)
                         |
               loopback origin listener
                         |
                outbound cloudflared
                         |
       disposable Quick Tunnel HTTPS test URL
           [later: named tunnel + DNS approval]
                         |
                outside-WLAN visitor
```

A current Git `main` branch is NOT a proxy for the last live release. On 2026-10-15, public `fountain.coach` was byte-identical to its earlier homepage revision `420be0c`, not its current Bookshelf root. Historical homepage versions are also evidenced for Governance, Status and Teatro. **One homepage match alone does not prove all routes or assets match**. Book of Reframe and MIDI2 still lack complete exact-live-homepage restoration proof. The published Solstice First Reading is hosted under `works.benedikt-eickhoff.de/solstice/`, sourced from `Fountain-Coach/solstice.fountain.coach`; the future `solstice.fountain.coach` DNS hostname must not be presented as live.

The previous Caddy candidates sometimes reverse-proxied many hostnames to a legacy Store upstream. A fresh disaster-recovery Caddy must not rely on that dead endpoint. Static material can be recovered independently, but any truly dynamic Store/API/media/authentication capability requires an explicit separate recoverable data and secrets plan. We cannot certify those capabilities merely by serving their landing pages.

## Phase A — Isolated external rehearsal (no production effects)

1. Select approved **last-public** Git commits and content digests for every active domain and delegated route. Use `Fountain-Coach/estate/inventory/` for ownership, required routes and public drift diagnostics. Produce an explicit `recovery-release-lock` for exact Git revisions, source paths, assets, route mapping, expected hashes and known gaps. A missing required artifact is `BLOCKED`, not substituted by LLM prose or a convenient `main` build.
2. On the existing Ubuntu machine, assemble release bytes in a **new isolated directory**; do not overwrite the existing WLAN staging, Store or other services. Configure a **separate** Caddy listener/instance and validate config and asset paths. Avoid production ports, vhosts and the Caddy admin API.
3. Test all required routes and asset digests locally with the intended Host routing. Then expose the isolated origin through a **disposable Cloudflare Quick Tunnel**, and independently test from a non-WLAN connection. The temporary `trycloudflare.com` hostname is **not a domain failover**, not guaranteed persistent, and might need a host-mapping test adapter for multi-domain validation.
4. Preserve the evidence: exact source/release lock, Caddy config hash, origin health, external HTTPS readback, asset and navigation audit, explicit blocked routes, browser/reading screenshots, clean shutdown.
5. **No change** to live DNS, Caddy serving, permanent tunnels, Git sources, or the public estate. The agent may not assume a tunnel is published merely because the local server started.

**Milestone:** `LOCAL_COLD_RESTORE_EXTERNALLY_OBSERVABLE` — only when the isolated reconstructed release is externally reachable and its required content/routes are verified with independent witnesses. Currently **not achieved**.

## Phase B — Emergency canonical domains (independent authorization)

1. Prepare a **named, restricted Cloudflare Tunnel** with per-host Caddy ingress, recoverable credentials, minimal access and no exposed origin admin API. Never commit credentials or private Store snapshots to Git.
2. Resolve DNS authority **before** the loss of Hetzner. On 2026-10-15, `fountain.coach` uses Hetzner authoritative nameservers; updating its Hetzner A records after Hetzner DNS is lost cannot be the plan. Establish registrar access plus alternative authoritative DNS for the `fountain.coach` zone with all existing records preserved (A/AAAA, CNAME, MX, TXT including SPF/DKIM/DMARC, CAA and verification). The `benedikt-eickhoff.de` zone (including `works.benedikt-eickhoff.de`) has **different** authoritative nameservers; it needs its own approved routing/delegation plan.
3. A named-tunnel route, correct public TLS, hostname verification and domain-owner authorization are separate requirements. Tunnel availability or Git pushes do not authorize switching DNS. Reissue HTTPS certificates as needed rather than trying to recover the old server's private certificate keys.
4. Only an explicitly authorized, receipt-bearing failover can redirect canonical names. Independently read back public HTTPS and every admitted domain's release identity, then prove a safe rollback/failback path.

**Milestone:** `EMERGENCY_DOMAIN_FAILOVER_READY` — requires an actually rehearsed DNS/tunnel/host-identity cutover and rollback. Currently **not achieved**. A home ISP or power outage may still make the emergency origin unavailable.

## Phase C — Optional independent remote host

Once Phase A works, run the **same host-independent restore scenario** on a new VPS at a provider **other than Hetzner** to test loss of both original server and household connectivity. Renting a second Hetzner server tests a narrower single-host failure, not disappearance of the provider. A standing paid VPS is **not** a prerequisite to the first meaningful proof on our existing Ubuntu machine.

## Explicit constraints and stop conditions

- No reclassification of Teatro as a book or omission of public normative/technical domains because they have no publication cover.
- No reconstruction from the two-cover v36 staging homepage in place of the actual public estate.
- No unverified assets, invented text, synthetic narration or implied complete MIDI2/Book-of-Reframe release.
- No unapproved DNS, Caddy, registrar, public tunnel or Git mutation; no secrets embedded in the estate repository.
- Private FountainStore state, user data, media stores, authorization and dynamic functions need independent backups and owner-trust recovery, not simply Git.
- No single-host/IP/address hardcoding in the recovery scenario; keep Caddy host-neutral and ports/config isolated.
- RTO/RPO (time to restore/acceptable loss) are unknown until measured in a full cold drill.
- An HTTP 200 or valid TLS certificate is **insufficient**; require correct release digests, routes and content.
- The owner controls the public domain at all times; the agent is an executor within that authority, never its replacement.

## Next step — not part of this documentation change

**Implement a read-only release-reconciliation planner in Fountain-Coach/estate.** It must discover the exact last-published artifact for every domain, identify gaps (especially Book of Reframe and MIDI2), and produce a complete fail-closed recovery lock. After review, run a clean isolated Caddy restore on Ubuntu, and only then open a temporary public tunnel for a genuine external test.

This ADR records the choice and rationale. It does **not** claim the tunnel exists, an emergency DNS provider has been selected, a release lock is complete, or disaster recovery is operational.
