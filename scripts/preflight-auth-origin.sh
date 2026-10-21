#!/usr/bin/env bash
# R37: READ-ONLY preflight for the exact WebAuthn origin.
# Does not create/edit DNS records, TLS certificates, Caddy configuration or keys.
set -eu
domain="auth.fountain.coach"
base="fountain.coach"

printf 'R37_AUTH_ORIGIN_PREFLIGHT v1\n'
printf 'proposed_origin=https://%s\n' "$domain"
printf 'delegation_dns='
delegation="$(dig +short NS "$base" | LC_ALL=C sort | tr '\n' ',' || true)"
printf '%s\n' "${delegation:-UNKNOWN}"
ip="$(dig +short A "$domain" | grep -E '^[0-9]+(\.[0-9]+){3}$' | head -1 || true)"
v6="$(dig +short AAAA "$domain" | head -1 || true)"
if [ -z "$ip" ] && [ -z "$v6" ]; then
  printf 'auth_dns=NOT_ESTABLISHED\n'
else
  printf 'auth_dns=RECORD_OBSERVED_REQUIRES_OWNER_VALIDATION\n'
fi
# Do not assume this context is the registrar or actual authoritative DNS.
if command -v hcloud >/dev/null 2>&1; then
  zones="$(hcloud zone list -o columns=name 2>/dev/null || true)"
  if printf '%s\n' "$zones" | grep -q 'fountain.coach'; then
    printf 'cloud_zone=VISIBLE_NEEDS_OWNER_VERIFICATION\n'
  else
    printf 'cloud_zone=NOT_VISIBLE_TO_ACTIVE_CONTEXT\n'
  fi
else
  printf 'cloud_zone=CLI_UNAVAILABLE\n'
fi
if [ -n "$ip" ] || [ -n "$v6" ]; then
  if curl -fsS --max-time 6 --head "https://$domain/" >/dev/null 2>&1; then
    printf 'https=RESPONDING_NEEDS_CERTIFICATE_AND_SERVICE_IDENTITY_AUDIT\n'
  else
    printf 'https=NOT_ESTABLISHED\n'
  fi
else
  printf 'https=NOT_ESTABLISHED\n'
fi
printf 'passkey_enrollment=BLOCKED_UNTIL_INDEPENDENT_OWNER_DNS_TLS_AND_RECOVERY_EVIDENCE\n'
