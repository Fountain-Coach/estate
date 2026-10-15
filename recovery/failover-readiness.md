# Hetzner-provider-loss recovery readiness

**Result: NOT_READY_FOR_CANONICAL_PROVIDER_LOSS_FAILOVER**

The existing Ubuntu/Caddy origin successfully reconstructs the 600 observed static public bytes. This report evaluates the separate canonical-domain, DNS, identity and dynamic-state boundaries. It is a **read-only** exercise: no registrar session, zone import, named tunnel, live routing, secrets or production Caddy configuration was modified.

## Public DNS authority and dependencies

| DNS zone | Observed delegated nameservers | Operational concern |
|---|---|---|
| fountain.coach | helium.ns.hetzner.de, hydrogen.ns.hetzner.com, oxygen.ns.hetzner.com | Provider-loss single point of failure |
| benedikt-eickhoff.de | ns71.domaincontrol.com, ns72.domaincontrol.com | iCloud Mail records and adjacent literary domain must be preserved |

This is **not a complete DNS zone export**. A small known-host record census cannot enumerate every unlisted DKIM selector, private verification subdomain, SRV or third-party integration. At a later authorized migration, obtain a complete zone export through its owning provider/registrar and compare every record before a nameserver change.

## Observed public hosts

| Host | Known source owner | Current A (sample) | Public responses recovered |
|---|---|---|---:|
| benedikt-eickhoff.de | Fountain-Coach/benedikt-eickhoff.de | 65.109.14.71 | 23 |
| book.fountain.coach | Fountain-Coach/book-of-reframe | 65.109.14.71 | 54 |
| fountain.coach | Fountain-Coach/fountain.coach | 65.109.14.71 | 26 |
| governance.fountain.coach | Fountain-Coach/governance.fountain.coach | 65.109.14.71 | 277 |
| instruments.fountain.coach | Fountain-Coach/instruments.fountain.coach | 65.109.14.71 | 14 |
| midi2.fountain.coach | Fountain-Coach/midi2 | 65.109.14.71 | 37 |
| status.fountain.coach | Fountain-Coach/status.fountain.coach | 65.109.14.71 | 22 |
| teatro.fountain.coach | Fountain-Coach/teatro.fountain.coach | 65.109.14.71 | 5 |
| works.benedikt-eickhoff.de | Fountain-Coach/works-benedikt-eickhoff | 65.109.14.71 | 142 |

## Failover and runtime gates

| Gate | State | Reason |
|---|---|---|
| immutable-public-bundle | PASS_BOUNDED | 600/600 observed HTTP-200 files retrieved from GitHub and hash verified on Ubuntu; SHA-pin protects integrity but GitHub release is not policy-immutable |
| ubuntu-static-origin | PASS_BOUNDED | Isolated local Caddy on loopback 18480 answered 600/600 resource bytes for all nine original Host headers |
| cloudflare-single-host | PASS_BOUNDED | Temporary uncredentialed Cloudflare URL returned exact fountain.coach root over public HTTPS, not the original canonical hostname |
| complete-public-release | BLOCKED | 621 bounded URLs observed; unlinked public resources, complete source release admission and source owner signature unknown |
| fountain-authoritative-dns-independent-of-hetzner | BLOCKED | Current NS delegation entirely to Hetzner; registrar-level NS migration/access not exercised |
| founder-zone-and-icloud-mail-preserved | BLOCKED | Different registrar DNS; existing iCloud mail MX/TXT must survive; public observation does not establish full zone contents |
| zone-inventory-exhaustive | BLOCKED | Known-host and common mail-label DNS readback is not a complete zone enumeration and does not prove registrar credentials |
| canonical-nine-host-ingress-and-tls | BLOCKED | Named tunnel, per-host hostname ingress, canonical-domain TLS, control-token custody and rollback not tested |
| owner-auth-domain-trust-and-secrets | BLOCKED | No independently recoverable owner key or SecretStore custody proof |
| private-fountainstore-state | BLOCKED | Git static publication does not include private Store durable state or a verified off-provider encrypted restore |
| browser-runtime-and-interactive-audio | BLOCKED | Caddy byte equality does not test iPad reader interaction, browser Csound, MIDI2 performance, playback or user consent |
| external-api-and-service-identities | UNDETERMINED | Public static URL census cannot establish active OAuth, BotCast, API, email integrations or other external runtime state |
| off-home-network-witness | BLOCKED | Quick Tunnel tested via internet by Mac, not independently accepted on a separate ISP/device |
| recovery-rto-rpo-and-failback | BLOCKED | No timed authorized full cutover or rollback; private data loss objective undefined |

## Explicit provider-loss simulation

In the assumed disaster (Hetzner server/IP unavailable **and** Hetzner authoritative DNS unavailable), the reconstructed files continue to exist on Ubuntu, but **fountain.coach is not demonstrated to remain publicly reachable**. Until the registrar directs queries to functioning independent nameservers, an HTTP-healthy origin cannot rescue a DNS-dead domain.

Next action: independently prepare and verify alternative DNS ownership, exact complete zones, Cloudflare named tunnel/hostname control and protected token custody. Test with delegated nonproduction zones and only then seek explicit owner authority for canonical-domain migration.

## Limitations

- Per-host HTTP 200 static equality does not attest live service API, FountainStore, OAuth, BotCast, interactive iPad reader or MIDI2 performance continuity.
- The historical static release remains explicitly **unadmitted** as production.
- TXT records are public DNS data but may include third-party verification tokens; no secrets/private backup content was queried.
- Public DNS observation cannot prove registrar login, ability to move delegation, domain expiry/transfer status or complete zone contents.
- The simulation is deliberately fail-closed and must not be described as a performed DNS failover.

Refresh public DNS witness: `npm run recovery:failover:probe`. Verify pinned snapshot without network: `npm run recovery:failover:verify`.
