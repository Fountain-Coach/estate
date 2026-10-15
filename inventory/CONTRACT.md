# Estate source-of-truth inventory contract

**Scope:** every registered Fountain Coach estate hostname, owning GitHub repository, tracked HTML route, and navigation dependency. This is an inventory of the entire estate, not a new Bookshelf, product taxonomy, or web home page.

## Authority model

- Domain claims are declared in the Estate registry manifest and must name exactly one GitHub source repository.
- The owner checkout is resolved and verified against its actual GitHub origin, not inferred from directory naming.
- Every Git-tracked HTML file under that owner's declared publication root receives a canonical route and SHA-256 source digest. Untracked build outputs and proofing files cannot silently appear as published works.
- Where a public host delegates a path to another owner, the inventory records both the parent host and delegated source. The essential example is works.benedikt-eickhoff.de, whose parent site is owned by works-benedikt-eickhoff while the /solstice/ subtree is sourced from solstice.fountain.coach.
- Some domains are instruments rather than editions. Teatro is such an instrument and remains part of the estate even when it does not occupy a cover slot.
- MIDI2's primary owning repository contains code and documentation rather than a static publication-root tree. Its independent public site is not fabricated from a local HTML file.
- A proposed publication (the planned solstice.fountain.coach hostname) does not become publicly serving merely by being in Git. Archived Tennis is retained as an owner reference without an active-site assertion.

## Artifacts

| File | Meaning |
|---|---|
| domain-ownership.json | Per-domain Git owner, lifecycle, source checkout and revision, source-root validity, tracked file counts and risks |
| source-routes.json | Every tracked HTML route, owner/source file and exact SHA-256 digest; includes delegated public paths |
| navigation-edges.json.gz | Deterministically Gzip-compressed complete HTML navigation edges including internal, estate and external targets |
| estate-relations.json | Reviewable cross-domain source navigation dependencies |
| public-readback.json | Independent HTTPS response status, bounded route sample, page digest, links and source-versus-live comparison |
| README.md | Human-readable reconciliation, deployment divergences and omissions |

Each owner revision represents a **source-candidate**, not a claim about the public server. The independent HTTPS witnesses are read-only observations; they do not assert deployment or authority to mutate Caddy, DNS, content, secrets, or the user's devices.

## How to run it

From the Fountain-Coach/estate repository (owner checkouts must be accessible under the same Development root; set FOUNTAIN_DEV_ROOT to override that root):

1. Run npm run inventory:build to reassemble the source contract from the Git owner checkouts and Estate manifest.
2. Run npm run inventory:verify or npm run check to fail on a stale inventory, lost route, invalid delegation, broken source inventory or missing owner checkout.
3. Run npm run inventory:probe to capture a fresh independent public HTTPS snapshot, including source comparisons. This is a **sample**, not an exhaustive remote crawler.
4. Review inventory/README.md and the diffs before considering any change to a publication, hostname or Bookshelf.

No GitHub workflows or CI are created. The commands do not publish anything.

## Why this prevents our recent failure

The new v36 Bookshelf selectively displayed Essays and First Readings but omitted several live governance and technical domains. That selection is a design decision about a single surface, not an estate definition. The inventory is compiled from actual owner repositories and recorded hosting delegations, and it explicitly computes which estate domains visible on the public root are missing from the current candidate root navigation.

A visual UI release must not be declared estate-complete while these differences remain unresolved and author approval is absent. This inventory makes that discrepancy machine-readable without forcing the UI to display every route as a book.

## Known limits

The currently captured remote evidence is a bounded HTTPS root + representative route sampling. It does not exhaustively verify every publicly served page or authenticate the exact remote deployed Git revision by a deployment receipt. The source route inventory is complete for locally checked-out **Git-tracked HTML**; dynamic server endpoints, unpublished documents and CDN-hosted generated material require separate authority. Local origin/main comparisons are local tracking refs, not an up-to-the-second GitHub ref fetch.

Source SHA equality to live HTTP body bytes is strong evidence for a matching artifact. A mismatch only proves different bytes—not automatically which revision is deployed. Public release continues to require an independent authorized publishing/readback process.

## Stable verification while owner repositories advance

`inventory:build` deliberately captures the presently committed `HEAD` of each owning Git checkout, storing the full SHA in the inventory. `inventory:verify` instead rereads the **pinned commit objects** recorded in the existing inventory; it does not follow a moving `HEAD`, Git index or working tree. Owner changes cannot invalidate already frozen disaster-recovery evidence merely by advancing a branch. A separate build creates a new owner snapshot when explicitly requested. Both modes confirm the GitHub remote identity and rehash committed files; neither takes uncommitted editorial work as publication authority.
