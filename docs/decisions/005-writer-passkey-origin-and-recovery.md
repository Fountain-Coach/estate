# ADR 005 — Named passkey origin and independent owner continuity for R37

**Date:** 2026-10-18  
**Status:** PROPOSED / BLOCKED — no DNS, certificate or owner credential may be provisioned by this ADR  
**Owner:** Fountain Coach Estate domain owner; FountainAuthKit authenticates and authorizes independently of publication and model providers.  
**Relates to:** Estate ADR 002 (canonical DNS independence), ADR 003 (Golden Key recovery), FCIS 131/139/142/143, [FountainAuthHostKit R37](https://github.com/Fountain-Coach/FountainAuthHostKit/tree/feature/r37-writer-trust-ceremony).

## Decision

The canonical native Reframe writer-passkey relying-party identity is **`auth.fountain.coach`**, with exactly **`https://auth.fountain.coach`** as the accepted origin and issuer, pending independent governance and operational acceptance. This name was proposed by FCIS 142, not newly invented by a login-screen implementation.

On 2026-10-18 `auth.fountain.coach` had **no resolvable DNS record** from the authenticated Mac; the existing Ubuntu `192.168.8.11:8445` HTTPS OAuth pilot is a *different* endpoint and cannot be silently promoted to WebAuthn relying-party authority. A successful `curl` to an IP, an SSH session, a Linux process UID or a trusted local TLS certificate is not proof of passkey enrollment authority.

The RP/domain owner graph and recovery plan belong to `Fountain-Coach/estate`. The issuer implementation belongs to `Fountain-Coach/FountainAuthHostKit` and `FountainAuthKit`. No private keys, backup contents, registrar tokens, user identifiers, passkey credential IDs, certificates or enrollment secrets belong in Estate Git.

## Required identity and recovery continuity

- DNS control must be established through the domain-owner/registrar custodian rather than inferred from SSH or a Caddy config. Discover existing zone contents, CAA/DS and renewal delegation; do not modify unknown records or iCloud mail records.
- Choose a clearly named deployment target, immutable Git-owned artifact, independent restore capability and correctly authorized certificate issuance. Host/service process identity must be separately authenticated. The new auth endpoint is dynamic private authority, **not** a static book or a disaster-recovery landing page.
- First writer-passkey enrollment needs a separately authorized owner claim anchored in an admitted owner root. ADR 003 and FCIS 139 say *lost-root Golden Key recovery is not accepted yet*. Do not treat creation of a first passkey as a way to bypass that block; enrollment must fail closed until a legitimate root/enrollment proof is available.
- A second authenticator and independently recoverable owner plan should be tested before depending on a single iPad. Revocation, re-enrollment, root rotation, off-host encrypted state restore and rollback are distinct bounded transitions with their own redacted receipts.
- A passkey assertion authenticates a principal. Only FountainAuthKit grants bounded client/resource/scope; Composer checks the grant *again* against the selected book, and connecting OpenAI gives no writing permission.
- iPad Safari/WebAuthn and native AuthenticationServices require the actual relying-party origin and an admitted `webcredentials` associated-domain relationship for native use. No forced Safari opaque-origin fallback, `localhost` or IP-based passkey operation.

## Promotion gates

1. Complete domain-owner, DNS, TLS, certificate renewal and public/private routing evidence for exactly `auth.fountain.coach`, with no broad wildcard.
2. Independently prove owner-approved initial enrollment and recovery without exposing credentials or broadening ADR 003 privileges.
3. Pin a reviewed Swift WebAuthn verifier and run valid/invalid registration, assertion, user-verification, challenge replay, credential revocation and compromised-device tests on an isolated environment.
4. Prove the actual named-origin ceremony in iPad portrait and landscape Reframe Composer without changing the bookshelf or writing manuscript.
5. Separately prove real resource-server authorization and one explicitly invited Chapter 149 MIDI2 OpenAI turn.
6. Demonstrate full credential, Store, DNS and TLS disaster recovery without assuming the original Hetzner server or DNS survives.

**Until all gates pass:** R37 is design/code groundwork only, `AUTH_READY=false`, `COMPOSER_WRITER_READY=false`, and `MODEL_TURN_AUTHORIZED=false`. The running R36 services and the original read-only `:8444` preview stay unchanged. No production DNS, NS delegation, TLS or owner key mutation is authorized by this proposed ADR.
