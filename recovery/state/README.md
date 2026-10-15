# Recovery State Manifest — Fountain Coach

**Private owner continuity: NOT READY.** The existing 600/600 public static recovery proof remains valid but does not attest any private recovery.

This manifest catalogs 16 types of state, NOT an authenticated inventory of installed production instances. It contains no private Store record, password, key, user information, or secret. The evidence references point to owner components and governance, not live backup receipts.

| State class | FCIS 118 classification | Authority / owner component | Recovery assessment |
|---|---|---|---|
| public-estate-static-artifacts | institutional-knowledge | Fountain-Coach/estate | STATIC_600_BYTES_VERIFIED |
| estate-owned-source-and-manifests | institutional-knowledge | Fountain-Coach/estate | UNVERIFIED |
| fountainstore-durable-institutional-records | institutional-knowledge | Fountain-Coach/Fountain-Store | UNVERIFIED |
| store-publication-and-scenario-receipts | institutional-knowledge | Fountain-Coach/Fountain-Store | UNVERIFIED |
| store-unpublished-personal-context | personal-context | Fountain-Coach/Fountain-Store | UNVERIFIED |
| unpublished-manuscripts-and-editorial-drafts | personal-context | Fountain-Coach/estate | UNVERIFIED |
| media-attachment-payloads-and-digests | institutional-knowledge | Fountain-Coach/estate | UNVERIFIED |
| owner-signing-root-and-golden-key | authority-capability | Fountain-Coach/swift-secretstore | BLOCKED_NO_ACCEPTED_LOST_ROOT_PROTOCOL |
| host-and-device-enrollment-authority | authority-capability | Fountain-Coach/Fountain-Store | UNVERIFIED |
| secretstore-backend-protected-values | authority-capability | Fountain-Coach/swift-secretstore | UNVERIFIED |
| fountainauthkit-domain-grants-and-state | personal-context | Fountain-Coach/FountainAuthKit | UNVERIFIED |
| oauth-signing-keys-and-external-tokens | authority-capability | Fountain-Coach/FountainAuthKit | UNVERIFIED |
| registrar-dns-and-provider-account-control | authority-capability | Fountain-Coach/estate | UNVERIFIED |
| github-organization-owner-and-release-custody | authority-capability | Fountain-Coach/estate | UNVERIFIED |
| successor-transfer-and-legal-owner-intent | institutional-knowledge | Fountain-Coach/estate | UNVERIFIED |
| operational-client-runtime-and-integrations | institutional-knowledge | Fountain-Coach/estate | UNVERIFIED |

## Programme Definition of Done gates

| Acceptance gate | State | Required evidence |
|---|---|---|
| complete-operational-state-inventory | BLOCKED | No independent inventory of all actual production instances |
| independent-private-backup-custody | BLOCKED | No verified encrypted off-host backup, retrieval and integrity receipt |
| golden-key-and-successor-authority | BLOCKED | FCIS 139 lacks accepted lost-root recovery; successor authority unproved |
| clean-room-private-store-restoration | BLOCKED | No authenticated restore of actual protected Store state and media |
| authorized-publication-continuity | BLOCKED | No authorized new publication from restored private authority with independent readback |
| repeatable-timed-owner-accepted-proof | BLOCKED | No two accepted cold drills, measured RTO/RPO, rollback and owner receipt |

## Next governed action

Obtain an authorized **read-only**, redacted inventory of actual live Store instance identities, sources of truth, protected attachment classes, and eligibility/omission policy. Do not read credentials, export raw Store files, or infer production state from development fixtures. Each operational dependency must be traced to its own custody authority.

A later governed adapter may write a private typed backup receipt outside this public repository. This Stage 1 verifier intentionally refuses even plausible-looking receipts in its open manifest.

Chapter 139 has no accepted lost-root owner-recovery operation. Replacing a key or using host root is NOT a valid Golden Key restore. Chapter 143 requires one bounded owner bootstrap/session rather than repeated credential prompts.

## Checks

Run npm run recovery:state:verify to prove the snapshot and derived readiness are unchanged; npm run recovery:state:test to run synthetic denial tests. Neither command contacts a live host or reads secret material.
