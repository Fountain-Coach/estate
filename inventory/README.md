# Fountain Coach estate inventory

Machine-generated from owner Git checkouts and the Estate domain registry.
No publishing, DNS, Caddy or Git mutation. Source ownership is not proof of deployment.

| Host | Owner | Role | Git HTML routes | Public root | Root matches current source |
|---|---|---|---:|---|---|
| benedikt-eickhoff.de | Fountain-Coach/benedikt-eickhoff.de | adjacent-founder-pointer | 7 | 200 | yes |
| book.fountain.coach | Fountain-Coach/book-of-reframe | reframe-historical-reference-not-linotype | 17 | 200 | no |
| fountain.coach | Fountain-Coach/fountain.coach | editorial-identity | 15 | 200 | no |
| governance.fountain.coach | Fountain-Coach/governance.fountain.coach | normative-reference | 165 | 200 | no |
| instruments.fountain.coach | Fountain-Coach/instruments.fountain.coach | technical-catalogue | 4 | 200 | yes |
| midi2.fountain.coach | Fountain-Coach/midi2 | technical-evidence | 0 | 200 | unverified |
| solstice.fountain.coach | Fountain-Coach/solstice.fountain.coach | authored-literary-edition | 32 | 0 | no |
| status.fountain.coach | Fountain-Coach/status.fountain.coach | mandatory-legal-footer-and-transparency | 12 | 200 | no |
| teatro.fountain.coach | Fountain-Coach/teatro.fountain.coach | authoring-and-performance-instrument-not-publication | 5 | 200 | no |
| tennis.fountain.coach | Fountain-Coach/tennis.fountain.coach | retired-technical-experiment | 1 | archived | unverified |
| works.benedikt-eickhoff.de | Fountain-Coach/works-benedikt-eickhoff | literary-works-publication | 60 | 200 | yes |

## Critical boundaries

- Complete tracked HTML routes are in source-routes.json; all 31,918 navigation edges are preserved losslessly in navigation-edges.json.gz and cross-domain relations are summarized in estate-relations.json.
- The public readback is a bounded sample; no false claim of exhaustive public routing.
- The works.benedikt-eickhoff.de parent hostname is owned by works-benedikt-eickhoff; its /solstice/ subtree delegates to the Solstice source repository.
- The MIDI2 code/documentation repository has no tracked deployed site root in this checkout; its live website must be read back independently.
- Archived Tennis must not be counted as a live estate member. The planned Solstice hostname is not assumed to resolve.
- A source revision differing from production is not a reason to replace a public estate homepage with a new bookshelf.

## Public deployment reconciliation

- book.fountain.coach: live HTTPS differs from current checked-out source
- book.fountain.coach: public estate root links absent from current candidate navigation: benedikt-eickhoff.de, midi2.fountain.coach, teatro.fountain.coach, works.benedikt-eickhoff.de
- fountain.coach: live HTTPS differs from current checked-out source; matches historical root Git baseline
- fountain.coach: public estate root links absent from current candidate navigation: benedikt-eickhoff.de, book.fountain.coach, governance.fountain.coach, instruments.fountain.coach, midi2.fountain.coach, status.fountain.coach, teatro.fountain.coach, works.benedikt-eickhoff.de
- governance.fountain.coach: live HTTPS differs from current checked-out source
- solstice.fountain.coach: no successful HTTPS response; do not claim this host is published
- status.fountain.coach: live HTTPS differs from current checked-out source
- teatro.fountain.coach: live HTTPS differs from current checked-out source
- teatro.fountain.coach: public estate root links absent from current candidate navigation: benedikt-eickhoff.de, book.fountain.coach, governance.fountain.coach, instruments.fountain.coach, midi2.fountain.coach, status.fountain.coach

## Repository-side risks

- dirty-owner-checkout: Fountain-Coach/fountain.coach
- revision-differs-from-local-origin-main: Fountain-Coach/midi2
- no-tracked-static-publication-root: Fountain-Coach/midi2
- planned-host-no-publication-assertion: solstice.fountain.coach

## Controls

Build source inventory: npm run inventory:build
Check source inventory without modification: npm run inventory:verify
Read back public HTTPS samples: npm run inventory:probe

Human review and governed publishing remain separate steps.
