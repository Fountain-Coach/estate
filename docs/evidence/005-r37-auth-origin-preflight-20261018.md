# R37 auth origin — read-only preflight evidence

**Observed 2026-10-18, authenticated Mac environment** via `scripts/preflight-auth-origin.sh` on branch `feature/r37-auth-origin-custody`.

```
R37_AUTH_ORIGIN_PREFLIGHT v1
proposed_origin=https://auth.fountain.coach
delegation_dns=helium.ns.hetzner.de.,hydrogen.ns.hetzner.com.,oxygen.ns.hetzner.com.,
auth_dns=NOT_ESTABLISHED
cloud_zone=NOT_VISIBLE_TO_ACTIVE_CONTEXT
https=NOT_ESTABLISHED
passkey_enrollment=BLOCKED_UNTIL_INDEPENDENT_OWNER_DNS_TLS_AND_RECOVERY_EVIDENCE
```

**Interpretation:** Fountain Coach's public domain is delegated to Hetzner nameservers. The exact proposed WebAuthn relying-party name has no publicly resolvable A/AAAA record. The available `hcloud` CLI context can see a running cloud server, but `hcloud zone list` does not show the DNS zone. **This does not prove who can update the authoritative zone** and is not authorization to add DNS records, route Caddy, manage certificates, or change registrar delegation.

**Action needed:** identify the actual DNS zone custodian and obtain narrowly authorized management access, then stage an exact named `auth.fountain.coach` HTTPS origin with proof of certificate validation, issuer-service identity and rollback. The Estate ADR 005 and owner-continuity recovery gates remain binding. DNS must not be silently migrated or confused with Hetzner Cloud server access.

No DNS/TLS/SSH configuration or secret material was modified by this preflight. No WebAuthn passkeys were enrolled.
