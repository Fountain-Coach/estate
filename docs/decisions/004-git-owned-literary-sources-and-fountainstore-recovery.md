# ADR 004 — Git-owned literary sources and recoverable FountainStores

**16 October 2026 · Fountain-Coach/estate · Adopted source ownership; full disaster recovery OPEN**

## Decision

**Git owns authored source identity and revision history. FountainStore owns live transactions, editorial state and authorization.** Apply the domain source-ownership model to books, corpora and editions. Every durable authored work needs a canonical owning Git repository, pinned commit and independently verifiable source object. One repository may own a related collection; a physical FountainStore directory does not automatically require its own repo. An edition refers to a work and its approved sources, not to a cover, Score image or runtime corpus ID.

The public Estate registry is a **metadata-only cross-owner index**, not a second manuscript repository or Store. A Git source commit cannot itself publish a book, replay scenarios, authorize a writer/model act, or replace an active Store. Fountain Press owns the composition, Reframe the semantic Bookshelf and editor, and EstatePublisher the explicit release boundary.

## Recovery chain

1. From the committed literary-ownership registry select the stable work ID and its authoritative repository, immutable commit, Git blob, source type and SHA-256.
2. Retrieve the original bytes from an **off-host Git mirror**; verify Git blob ID and SHA-256. Reconstruct source into a new isolated destination. A PDF remains a PDF; it cannot silently become a Fountain screenplay.
3. Independently retrieve a typed **FountainStoreRecoveryKit / FCIS 117** snapshot from approved private, encrypted off-host custody. Include eligible source/attachments, writer/model editorial documents, source references, receipts and omissions. Under FCIS 118, private or ineligible personal context must not be committed to this public registry or exported without owner authorization.
4. Restore into a new governed FountainStore; verify source/edition IDs, digests, Store sequence, omitted references, annotations, selected semantic positions and receipt lineage against the recovered Git objects. The target Store is not publication-ready until separately admitted.
5. Rebuild Reframe's source-backed Bookshelf, reopen real books using Fountain Press, then verify writer/editorial continuity. Publication requires a separate EstatePublisher authorization and independent readback.

**FCIS 117 is the Store snapshot/recovery authority; Git is the durable authored-source authority and the mirror for eligible recovery projections.** This is not competing runtime authority. Owner trust-root/Golden Key recovery remains governed by Estate ADR 003 and FCIS 139; having Git does not grant lost-key replacement.

## Actual evidence, not synthetic books

The first index contains eight distinct candidates: three original authored PDFs from the private `Fountain-Coach/works-benedikt-eickhoff` Git owner; three pinned edition source entry points owned by Solstice, Fountain Coach and Teatro Git repositories; and Ulysses/Metamorphoses as local FountainStore corpora **not yet Git-mirrored or approved as editions**.

Six source objects were independently checked against their owning local immutable Git commits. **One actual remote reconstruction succeeded:** the private GitHub blob for `Ballern Gehen`, object `fc25691ec70ce2f0798da6b98dd3f8cccea7ad3c`, was downloaded independently of the local checkout, written to an isolated destination, and verified byte-for-byte: **34,877 bytes**, SHA-256 `ab610ab150eaeb2d67817529b012dedaeeedc9949abba0faf70ccd42f508202b`.

This proves **one recoverable Git-authored source**, not recovery of an entire edition, FountainStore, or owner security authority. No manuscript bytes have been added to public Estate Git; no publication or production Store was changed.

## Mandatory invariants

- One stable authored work ID must resolve to an owning Git repo and immutable source revision before the corresponding book is considered Git-recoverable.
- A single work may have multiple editions, source revisions, and Store projections; none may multiply its work identity. A corpus is a runtime materialization, not itself proof of an authored book.
- Preserve historical divergence as revisions, not silent Git↔Store two-way synchronization.
- Never import private raw database/WAL snapshots, unrestricted writer materials, keys, tokens, private media or unclassified drafts into public Git. The FCIS 117 typed projection kernel is available, but a real authorized off-host snapshot/restore adapter still needs proof.
- The existing `Fountain-Coach/book-library` is a curated Git-owned source provider; it does not replace the author's own repositories or bypass rights/provenance approval.
- GitHub remote blob recovery is not independent provider-loss recovery. A second owner-approved off-provider bundle/mirror remains necessary to survive GitHub loss.
- The index must keep `completeLibraryInventory=false`, `anyFountainStoreRestored=false` and `independentCompleteStoreBackupVerified=false` until independently proven with receipts.

## Next integration

Reframe's Bookshelf catalogue should resolve **Git-authored work → source edition → Store corpus/projection** through a verified registry, not list every attached Store as a book. The next controlled implementation is a private, classified source mirror for an eligible unmirrored corpus and a typed FountainStore export/clean-room restore, followed by a native reading/annotation readback. No new CI, public deployment or credential recovery is authorized by this document.

Verify with `python3 scripts/verify-literary-git-ownership.py verify`; optional read-only `local-verify` checks the actual immutable local Git objects; the explicit `github-recover` drill reconstructs one approved object into an isolated path.
