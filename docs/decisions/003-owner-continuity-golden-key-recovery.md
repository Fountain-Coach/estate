# ADR 003 — Owner continuity and Golden Key recovery programme

- **Date:** 2026-10-15
- **Owner:** Fountain Coach domain owner; individual state and trust authorities retain their own jurisdiction
- **Decision status:** Programme and acceptance contract adopted for the Estate registry; implementation and private recovery **not yet complete**
- **Previous milestones:** [ADR 001 — off-provider static restore](001-local-ubuntu-off-provider-tunnel-recovery.md), [ADR 002 — canonical-domain failover](002-canonical-domain-provider-loss-failover.md)
- **Implementation home:** [Fountain-Coach/estate](https://github.com/Fountain-Coach/estate), coordinating with [Fountain-Store](https://github.com/Fountain-Coach/Fountain-Store), [swift-secretstore](https://github.com/Fountain-Coach/swift-secretstore), [FountainAuthKit](https://github.com/Fountain-Coach/FountainAuthKit), and EstatePublisher
- **Relevant authority:** [FCIS 118 — classification and continuity](https://governance.fountain.coach/chapters/118-european-cybersecurity-profile/), [FCIS 139 — owner trust recovery](https://governance.fountain.coach/chapters/139-owner-trust-root-secretstore-custody-and-recovery/), [FCIS 143 — one bootstrap/session](https://governance.fountain.coach/chapters/143-simplicity-is-key-one-bootstrap-one-trusted-session/), [FCIS 148 — production artifact only](https://governance.fountain.coach/chapters/148-production-runtime-artifact-only/)

## Decision and immediate priority

Our **bounded static HTTP estate** has a reproducible GitHub release and a 600/600 byte-exact cold Caddy restore on the independently reachable Ubuntu machine. This succeeds without the former Hetzner origin. It does not restore durable private FountainStore state or authority to govern that state.

**Next priority: map the company's irreplaceable state, prove its independently recoverable backups, and prove a legitimate owner-controlled continuity path.** Registrar/Cloudflare named-tunnel administration is deferred to the final availability phase. No credential harvesting, production trust mutation or dynamic Store restoration is authorized by this ADR.

A domain's availability, content identity, state identity, and authority identity are distinct acceptance boundaries. Host root/SSH access cannot substitute for owner-signed trust. A Git archive of publicly seen pages cannot substitute for private Store records or an authorized publication receipt.

## Programme stages, in order

### Stage 1 — Recovery State Manifest (this initial implementation)

Create a deterministic **metadata-only** typed ledger in the Estate owner repository, mapping each state class to:

- unambiguous stable class identity and owning Git/component or operational authority;
- FCIS 118 classification: `institutional-knowledge`, `personal-context`, or `authority-capability`;
- whether content is reproducible from public Git, must be backed up privately, or must remain in protected native custody;
- acceptable export/restore interface and independent proof required;
- known repository/contract evidence, source revision and current verification status;
- irrecoverable/unknown gaps, omission rules and authority for any future action.

**No private state contents**, private filesystem paths, personal details, public key fingerprints tied to a specific person, or credential/key material belong in this manifest. A class entry does **not** prove a deployment instance, backup or restore exists. Unknown scope must remain `UNVERIFIED`.

### Stage 2 — Private state discovery and backup evidence

Use **read-only** inventories through legitimate Store/host authority (only when enrolled and authorized) to identify actual durable instance identities, WAL/SSTable state, attachment stores, media, published state/receipts, unpublished projects, and operational configuration. Merely finding development fixture directories on the Mac does not prove they are production data.

For each required nonreconstructible class, get an owner-authorized, typed export with schema/version, source authority identity, snapshot watermark/sequence, object and omission counts, digest, key-custody reference (not key), retention, and encrypted *off-host* destination. Independently verify backup retrieval and full integrity. Never put private snapshots or credentials in the public Estate repository.

FountainStore's typed `FountainStoreRecoveryProjector` is a **projection kernel**, not a demonstrated live production snapshot. An open recovery projection must exclude authority capabilities and unknown/ineligible personal context. Chapter 117 is retained architectural reference, **not** an operational backup receipt.

### Stage 3 — Golden Key continuity and succession authority

FCIS 139 states that the deployed owner trust model uses an owner Curve25519 signing root in SecretStore, that local and production roots differ, and **no accepted break-glass recovery operation currently exists**. The Estate registry must preserve this as a blocker rather than claim lost-root recovery is solved.

Owner trust-root rotation requires existing active owner authorization. Lost-root recovery, successor admission/inheritance, and first bootstrap are distinct trust transitions and require a separately reviewed, explicit authority protocol. No new signing key or host root credential is sufficient by itself. No key bytes, vault recovery token or bearer credential appear in git, logs or receipts.

FCIS 143 asks for **one deliberate bootstrap and one bounded trusted session**. Tests must prove denial on wrong target, expiry, replay, revoked or absent custody; no silent fallback or additional repetitive approval path. Succession requires accountable owner-controlled legal/technical authority, not a free-standing agent permission.

### Stage 4 — Clean-room proof

Construct an isolated new Store on a fresh independent host using **only** pinned Git artifacts, an authorized encrypted off-host backup and narrowly delegated owner authority. Preserve the production service untouched. Replay/corruption/missing/expired-key controls must fail closed; exact Store/record, attachment, sequence and publication receipt identities must be checked against signed source/export manifests.

The recovery executor must not independently grant itself owner trust or treat an LLM-generated reconstructed record as authentic. Production nodes admit previously built signed artifacts; they never build from source on the target (FCIS 148).

### Stage 5 — Operational acceptance and optional DNS failover

Repeat the clean-room drill independently, measure recovery time (RTO) and recoverable data-loss interval (RPO), verify a permitted new publication through typed FountainStore/EstatePublisher authority and exact readback, and produce a durable, redacted terminal receipt. Only an owner-reviewed, admitted restore moves a class from `UNVERIFIED` to `ACCEPTED`.

A separate later owner-authorized phase prepares complete DNS zone export, registrar-level independence, nine-host ingress and canonical TLS, using ADR 002. It is **not** a prerequisite for the private-state clean-room proof and does not become part of the current work automatically.

## Programme Definition of Done

All six mandatory predicates must be proven through independent evidence:

1. **Inventory complete:** each operationally indispensable state class and *actual production instance* has a named authority, classification, retention/omission policy, loss impact, and individually identified source-of-truth; none remains anonymous or guessed.
2. **Backup independent:** each essential nonreconstructible record/asset has versioned encrypted off-failure-domain backup plus retrieval and digest evidence; no secret crosses the open recovery boundary.
3. **Owner authority recoverable:** active-root or genuinely lost-root transitions are validated by an explicitly reviewed owner procedure with target binding, replay protection, bounded trusted session, compromise/expiry handling and a redacted terminal receipt. If no accepted lost-root path is available, DoD is BLOCKED.
4. **Clean-room restore:** no original Hetzner server, old Mac workspace, or privileged hidden source is used; recovered Store/asset/receipt identities and sequence watermarks match the approved evidence, not manufactured substitute state.
5. **Continuity proven:** a newly admitted environment performs one authorized publication and independent readback. Wrong-target, missing-backup, corrupt, replayed, unauthorized and stale inputs all fail closed.
6. **Reproducible, timed, accepted:** at least two independent drills, measured RTO/RPO, explicit owner acceptance, backup rotation and rollback/failback instructions, immutable redacted receipts.

A proof of static Caddy bytes alone is **not** a pass for any private-state predicate. Where personal data is not eligible for backup, the **documented omission/erasure** must survive and recovery must not silently restore it.

## First implementation slice

Pin `recovery/state/state-manifest.json`, a deterministic verifier, an explicitly blocked machine-readable readiness report, and a synthetic negative/positive test harness. Test only *declarative metadata* and fictitious non-sensitive records; do not probe live SecretStore, open Store directories, retrieve owner keys, or claim a private backup is made. Add the tests to `npm run check`, commit and push this documented boundary. Subsequent authorized work can enrich the manifest with private-source evidence receipts without publishing sensitive details.

## Anti-goals and prohibitions

- No Cloudflare account/configuration, domain/registrar change, public DNS cutover or new standing paid VPS in this phase.
- No real signing-key rotation, loss-of-root bypass, owner/successor enrollment, SecretStore access or credential export by this programme definition.
- No copying private user context, raw Store WALs, signing material, OAuth grants, tokens or private backups into public Git.
- No treating the open-source SecretStore library as a verified host-side secret recovery system; no treating the FountainAuthKit unit tests as an operationally enrolled OAuth service.
- No pretending GitHub's byte-verified 600-resource snapshot is a complete dynamic business recovery.
- No GitHub Actions/CI workflows; use local or explicitly enrolled execution and committed receipts.
