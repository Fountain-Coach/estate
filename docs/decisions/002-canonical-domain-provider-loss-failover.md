# ADR 002 — Canonical-domain failover after complete hosting-provider loss

- **Date:** 2026-10-15
- **Status:** Recovery gate designed and observed; **NOT READY** for canonical-domain cutover
- **Primary owner:** Fountain Coach domain owner; DNS registrar and SecretStore authority separate from content publisher
- **Scope:** Nine publicly observed estate domains, two independent registered DNS zones, private/service continuity
- **Evidence:** [Observed authoritative DNS](../../recovery/failover-dns-witness.json), [failover gate](../../recovery/failover-readiness.md), [browser/runtime boundary](../../recovery/runtime-boundary-witness.md), [Ubuntu static cold restore](../../recovery/ubuntu-cold-restore-witness-20261015.md)

## Decision

Our existing Ubuntu machine is a **verified emergency static origin** for the 600-URL bounded published estate snapshot, but it is **not** yet an approved replacement for all canonical domains.

The system must preserve independent authority over:

1. **Published release:** Immutable Git-backed public bytes, exact content hashes, all admitted routes, authorized release identity.
2. **Serving origin:** Reconstructed static files plus a host-neutral Caddy configuration on Ubuntu; SSH and tunnel service are replaceable transports.
3. **DNS delegation:** Domain owner/registrar retains final authority to direct both registered zones to independently functioning authoritative nameservers.
4. **Secrets and durable state:** Private FountainStore, OAuth, domain keys, mail credentials, media not in Git, device trust and backups cannot be inferred from a public HTML archive.
5. **Production admission:** Explicit owner-approved transition, a complete DNS comparison, public canonical TLS readback and tested failback/rollback.

These boundaries must never silently collapse into an agent's SSH session or a successful Cloudflare quick-tunnel GET.

## The demonstrated primary failure

On 2026-10-15, the public DNS delegation for `fountain.coach` names three **Hetzner** nameservers. All nine observed active hostnames currently resolve to the original `65.109.14.71` IP (some via a CNAME). In the simulation where both Hetzner's origin **and its authoritative DNS** are lost, the known local Ubuntu and GitHub artifact survive, but the canonical Fountain Coach domain does **not** have proven reachable DNS. This is a decisive continuity blocker.

`benedikt-eickhoff.de` is independently delegated to DomainControl authoritative nameservers. However, its website A record still points at the old IP and its iCloud Mail MX/SPF and verification data must survive any move or independent emergency routing. `works.benedikt-eickhoff.de` depends on that second zone, and the published Solstice First Reading remains under `/solstice/` there.

The captured read-only DNS witness covers **only explicitly known names and selected common mail labels**. It is *not* a complete zone export. It cannot prove registrar ownership/session access, discover every DKIM or SRV label, or guarantee email record parity.

## Required stages before real recovery

### 1. Domain-owner custody, no delegation changes

- Establish authorized registrar access for **both** registered zones and a durable owner/key recovery plan, outside the lost hosting provider.
- Obtain a **complete** authoritative zone export including every A/AAAA/CNAME, TXT/DKIM/DMARC/SPF, CAA, MX, SRV, delegated NS and third-party verification name. Compare to the separately captured public DNS witness.
- Record expiry, renewal, domain lock and transfer controls privately. Do **not** store registrar passwords, tokens, recovery keys, or unrestricted zone-manager credentials in a public repository.
- Explicitly distinguish a registrar account from a DNS provider. If original authoritative DNS is down, changing its A record is impossible; the registrar-level nameserver delegation is the survival control.

### 2. Independent authoritative DNS preflight

- Provision a second DNS provider (Cloudflare is the current tunnel candidate) and load a faithful zone snapshot before changing registrar delegation.
- Verify all records by directly querying the **new provider's authoritative nameservers**, including iCloud MX/SPF/DKIM and domain verifications, while public DNS continues using its existing authority. Reconcile name-by-name and type-by-type without dropping unknown records.
- A Cloudflare Quick Tunnel URL is **not** DNS authority for nine original hostnames. Named tunnel routes and custom-domain TLS require separate authorized setup and coverage.
- Capture DNSSEC/DS state at the registrar; mismatched DS after an NS move can blackhole the zone. Confirm CAA constraints and certificate issuance before approving any cutover.
- Cloudflare DNS and Cloudflare Tunnel together are a new concentration risk. For stronger independence, keep registrar custody and downloadable zone snapshots outside Cloudflare; consider a different independent DNS provider if provider diversification is the overriding requirement.

### 3. Named tunnel and host-based routing rehearsal

- Create a restricted named tunnel; recover tunnel credentials independently through the owner trust/SecretStore route.
- Add **explicit mappings** for all nine public hostnames and preserve the `works.benedikt-eickhoff.de/solstice/` delegation. Any host omitted from the ingress map is BLOCKED rather than redirected into a generic bookshelf.
- Run Caddy in a separately enrolled, bounded recovery container. The verified origin `127.0.0.1:18480` is not the public service's hostname; Cloudflare must preserve (or explicitly map) the canonical Host header. No Caddy admin exposure or residential router inbound rule.
- First prove browser and HTTPS readback under separate preview names or an authorized delegated *nonproduction* zone. Only an owner-authorized next step may involve the canonical names.

### 4. Service continuity and owner authority

- Record the independent recovery path for FountainStore durable state, confidential backups, keys, OAuth/service state, BotCast integrations, and any other live service separately. A successful static page must not be marked `AUTH_READY`, `MIDI_READY` or `STORE_READY`.
- Verify iPad reading and browser audio/Csound/MIDI behavior, not only script/file bytes. User gesture permissions and external API dependencies need active client tests.
- Define realistic RTO/RPO by timing a complete cold drill and quantifying data loss, not by extrapolating from a single static restore.
- Avoid changing the publishing taxonomy or replacing currently published content with staging material during disaster recovery.

### 5. Canonical-domain promotion and rollback

- Require a clearly scoped owner approval identifying affected zones, hostname list, frozen release digest, restore host identity and change window.
- Make an authoritative DNS parity report, negative-control tests, email health proof, HTTPS/TLS host-by-host proof and rollback plan mandatory before publishing.
- Keep former DNS authority available for rollback if it exists; in the specified total-Hetzner-loss scenario, rollback **cannot** assume Hetzner DNS becomes accessible again. An alternative functioning DNS authority is required.
- A post-cutover readback must verify the last-public edition identity and file bytes across all admitted routes and separately verify dynamic services. The separate off-WLAN human witness remains required.

## Read-only rehearsal that is complete today

The GitHub Release contains the exact 600-response byte-verified public archive. The Ubuntu machine fetched it **directly from GitHub**, ran Caddy in isolation, and served all nine HTTP Host identities with 600/600 exact byte matches. One single-host external Cloudflare Quick Tunnel demonstrated public HTTPS to the original Fountain Coach homepage. **Production DNS remains unchanged.**

The current [failover readiness ledger](../../recovery/failover-readiness.json) has 14 independently checked gates, including a deliberately negative provider-loss simulation; [runtime evidence](../../recovery/runtime-boundary-witness.json) classifies browser-code indicators without treating a library reference as proof of an active external service.

The gate is intentionally `NOT_READY_FOR_CANONICAL_PROVIDER_LOSS_FAILOVER`, and it does not permit the agent to change DNS or the public estate.

## Implementation placement

This decision, the domain owner graph, and the failover gate belong to `Fountain-Coach/estate`. Caddy runtime packaging can be delegated to the appropriate runtime/press repository once the owner-approved ingress contract is pinned. Secrets and registrar tokens belong to their custodians, not to this public repository. No GitHub Actions/CI workflow is required for this decision.
