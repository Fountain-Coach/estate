# Stage 2 — Operational state discovery boundary

**Status: BLOCKED — no established native owner authorization or actual production Store inventory.**

This is a safe, read-only inspection of *pinned source APIs*, not a privileged scan of current processes or the Store filesystem. A protected machine-level service inventory was not admitted. No service configuration, credential, private record, backup or signing key was read.

## Verified source contracts

| Source contract | Owning repository | Pinned source path | Finding |
|---|---|---|---|
| store-backup-api | Fountain-Coach/Fountain-Store | Sources/FountainStore/Store.swift | Backup directory is nested under the store's own options.path; local backup is not off-host custody |
| recovery-projection-kernel | Fountain-Coach/Fountain-Store | Sources/FountainStoreRecoveryKit/FountainStoreRecoveryKit.swift | Pure projection kernel receives authority-supplied records; does not discover Store, transmit backups, or authorize restore |

**Important:** The Store's createBackup method writes into a 'backups' child of its own Store directory. This is a local backup mechanism, not evidence of independent encrypted off-host custody. The RecoveryKit's projector is pure and requires an authority-supplied document set; it does not discover an operational Store.

## Still-unverified operational target classes

| Candidate | Component authority | Actual live instance |
|---|---|---|
| authoritative-fountainstore-instance | Fountain-Coach/Fountain-Store | NOT_OBSERVED |
| store-receipts-and-publication-state | Fountain-Coach/Fountain-Store | NOT_OBSERVED |
| private-media-and-attachment-custody | Fountain-Coach/Fountain-Store | NOT_OBSERVED |
| reframe-private-project-and-personal-state | Fountain-Coach/Fountain-Store | NOT_OBSERVED |
| owner-native-secret-custody | Fountain-Coach/swift-secretstore | NOT_OBSERVED |
| writing-domain-authorization-runtime | Fountain-Coach/FountainAuthKit | NOT_OBSERVED |
| independent-backup-destination | Fountain-Coach/estate | NOT_OBSERVED |

## Mandatory next acceptance boundary

1. Identify one exact operational FountainStore source through a previously enrolled native host/service adapter with bounded owner authorization.
2. Record metadata only: source authority class, schema/version, declared classification scope, source sequence, count of eligible and omitted categories, typed read-only result, opaque evidence digest and independent verification. The signed/protected full receipt stays with its legitimate authority; the Estate accepts only a redacted, authenticated summary.
3. Fail closed if the authority is stale, target is unknown, records are unclassified, inventory is partial, or the signed receipt cannot be independently verified.
4. The off-host encrypted backup, clean-room restoration, Golden Key lost-root recovery and actual authorized publication require **separate** evidence and approvals. None follows from this source API audit.

## Verification

Run npm run recovery:operational:verify for offline evidence reconciliation; npm run recovery:operational:test for synthetic fail-closed tests. Source implementation checking is restricted to pinned local Git code during npm run recovery:operational:build. No live machine interaction, private Store scan or network request is part of either test.
