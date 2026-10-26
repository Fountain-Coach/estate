# Reframe Bookshelf admission and public website release are different operations

**Fountain Coach architectural correction · 22 October 2026**

## Terms

| State | Authority | Observable result | Not implied |
| --- | --- | --- | --- |
| Source candidate | Source owner, Git provenance | Verified possible manuscript/source identity and SHA | Admitted book, rights, opened reader |
| Bookshelf-admitted work or edition | Writer/Reframe, FountainStore membership and editorial provenance | A truthful recognized book, admitted cover and containing shelf relation | Public distribution, DNS, top-reel icon |
| Readable composed edition | Fountain Press Linotype, with Reframe source address and consent | Authentic pages, reading, selection, return/reopen at semantic source position | Public release or right to redistribute the manuscript |
| Optional public edition/site publication | Publisher + source owner + EstatePublisher | Authorized public host/path, release receipt, independently verified HTTPS and rollback | New authorial membership or inferred SourceStore admission |

**Critical:** a Reframe Bookshelf publication normally changes the *Bookshelf's content*, not the estate site's domain topology. A reader can be the first writer of an Empty space; the Empty is a selectable state and cannot be represented as an already authored work or published edition.

## Required behavior

1. From a Git/Store candidate, resolve an exact authored source identity, digest, edition, cover rights and containing-space relationship. Refuse ambiguous or stale joins. Missing Store is unknown/unavailable, not permission.
2. On writer admission, persist explicit Reframe/FountainStore membership and original work/edition evidence. Render the book through Fountain Press's original Bookshelf and reader. Neither Press nor EstatePublisher owns the editorial decision.
3. Selecting a cover opens the *same source-bound edition*, with measured Press pages, semantic original passage position, and return to its containing shelf; editorial Composer/E01 acts remain separate from manuscript revisions unless the writer explicitly authorizes them.
4. If writer chooses Empty, only create new authored source after an attributed, consented, versioned writing act. Empty must not count toward admitted book totals.
5. For a public website release, require a separate rights/publisher grant, destination host and route, custody manifest and exact approved EstatePublisher deployment/rollback. No automatic new domain or reel icon.

## Negative tests

- Git-owned PDF is not automatically a Bookshelf book.
- Browser view or fabricated attractive cover is not source/edition admission.
- Opening a text or selecting a folio is not a durable reading position or a manuscript edit.
- Store-unavailable/unverified E01 is not zero activity or proof of rights.
- Private Bookshelf membership or a local preview cannot yield an EstatePublisher public-release success.
- A new work's edition/cover does not change the nine editorial entries in the estate reel.

## Source authority

- [Reframe R17 — Bookshelf state of Linotype](https://github.com/Fountain-Coach/Reframe/blob/main/scenarios/017-linotype-bookshelf-landing.md)
- [Reframe R22 — Git-authored literary estate](https://github.com/Fountain-Coach/Reframe/blob/main/scenarios/022-git-authored-literary-estate-bookshelf.md)
- [Reframe R24 — source-verified editorial evidence](https://github.com/Fountain-Coach/Reframe/blob/main/scenarios/024-source-verified-bookshelf-editorial-state.md)
- [Reframe R26 — Empty and first writing act](https://github.com/Fountain-Coach/Reframe/blob/main/scenarios/026-empty-bookshelf-first-writing-act.md)
- [Reframe ADR-006 — ownership and Press host](https://github.com/Fountain-Coach/Reframe/blob/main/docs/architecture/ADR-006-fountain-press-composition-owner-and-reframe-reading.md)
- [Fountain Press composition boundary](https://github.com/Fountain-Coach/fountain-press/blob/main/docs/reframe-composition-owner-boundary.md)
- [Fountain Press publication identity and cover navigation](https://github.com/Fountain-Coach/fountain-press/blob/main/docs/publication-identity-and-cover-navigation.md)

The cited integration scenarios contain incomplete iPad/native public acceptance; never upgrade their status in documentation.
