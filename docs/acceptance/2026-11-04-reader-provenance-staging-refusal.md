# 4 November 2026 — Reader provenance violation, rollback and staging refusal

**Incident:** A Fountain Press essay edition, *What Makes a Page Modern?*, was manually assembled as a separate `book-app` HTML reader under `/estate/essays/what-makes-a-page-modern/`, copied to an immutable WLAN staging release, and presented as a legitimate Fountain Press edition. This was **not** source-verbatim editorial admission through the existing Reader. Passing page composition and viewport checks were misrepresented as adequate evidence of reader provenance.

**Author's correction:** Do not invent a reader. Inspect the actually published **production** Reader and approved **staging** Reader before admitting any new work to either. Establish the canonical source, the original manuscript text and rights, production→staging reader lineage, actual owner-normal composition, then stage the book as a source addition to the **existing reader**. Do not build a separate route, alternative app shell, alternate compositor, layout wrapper, audio player or pseudo-admitted book.

## Observed state, not inferred from older snapshots

- **Public production observation:** `https://fountain.coach/` provides the existing Bookshelf Reader with `reading-first-press-engine.js`, `reading-first-app.js`, accompanying audio modules, and `reading-first-press-*.css`/`reading-first-shell.css`. The guessed public `/editions/essays-continuing/` route returned **404** on observation. Its absence is *not* an invitation to create an unrelated stage reader.
- **WLAN owner:** Ubuntu Mac mini `MacMiniDocker`, `192.168.8.50:8200`, source-locked `fountain-shell-acceptance-preview.service` with `/home/benedikt/estate-shell-acceptance-staging/current`.
- **Preserved accepted v140:** `shared-shell-20261103-v140-same-folio-return`. Its `source-lock.json` SHA-256 is `d263837865d282f495de905e3c43833be3b118faf0332529f61564b137bfaebc`; main Bookshelf `estate/index.html` SHA-256 is `69e656346b219be35c030e437100e72338f54d3a70abecbe6030971773cb1c01`.
- **Rejected v141:** `shared-shell-20261104-v141-what-makes-page-modern-1ab82bb`, containing a new page and thirteen source-created SVG illustrations. The route used the unrelated legacy `book.js`/SolsticeLinotype shell. The original essay PDF was not independently reconstructed from the actual source in this edition. Therefore **the new route must not be merged or published.**
- **Observed rollback:** `current` restored to v140 with the existing service restarted; `/estate/` and `/estate/editions/essays-continuing/` each returned HTTP 200, while the rejected `/estate/essays/what-makes-a-page-modern/` returned 404. Production was untouched.

## Real production/staging runtime difference

The accepted v140 stage and public root load the same known Reader engine and CSS, but a **stage-only divergence must be preserved and reviewed**, never silently overwritten with production. HTTP bytes and SHA-256 of these files were compared on 4 November:

| Asset in `/estate/assets/linotype/` | Production SHA-256 | Accepted stage SHA-256 | Same? |
| --- | --- | --- | --- |
| `reading-first-press-engine.js` | `0fed47d6d2bb4c61565cbc37d9f6df21da3f650b365dc1856ee72fdb95eaba4d` | same | Yes |
| `reading-first-app.js` | `4243dea9d3d8be1187f0c72cbde994e7748eebaeacc78e91d618b222024cfea4` | `557ba7736110ccf1ae4819549b3bf80fa1d6c411cf3b77b0e977db8aace23253` | No |
| `teatro-vergil-hearing.mjs` | `185744bbc4daa72cc55044720d089b854f1cf2d6ca2eab10d868ac74e72ca720` | `ef22bbe0109dd39d3fc5772f222b6e38d6b388d2ee327467c522f4ea6515dd18` | No |
| `vergil-prologue-hearing.mjs` | `5d60ecfa5ecadce573c40ede51f83c88cd359c8f6e822fe18938c5fef336a9d8` | `25a248b4a12ec189292fe44e297b2c7f2a7b2edd59d9a58db48ce66fcb938b61` | No |
| `reading-first-press-frame.css` | `4cd2f853315d51bdd2c31917782d42759fee0a9a20cf18ae4d261af085bd0e51` | same | Yes |
| `reading-first-press-host.css` | `a0ce4a3ba7c0e549354de8b3aaed608ad178f62bcfbc3451e3443f2989ea84b0` | same | Yes |
| `reading-first-shell.css` | `769fb12fbe7205e90269ecbf3760c8a6d226e78347bd1d62f05035174d671247` | same | Yes |
| `teatro-vergil-hearing.css` | `aff97c7676e9f3cf254beba93f5e17d3d0bf57956b72f86e4c9cff750317314a` | same | Yes |
| `vergil-prologue-hearing.css` | `a77abac2539be9c991e23f064851d12db5a1dfeb2e853de8a1a5c7beb3c553ce` | same | Yes |

The active stage-only `reading-first-app.js` differed in URL/address projection and rehearsal grant, per scoped diff. The two hearing modules also differed; their substantive differences have not been fully accepted as public behavior. An automatic production copy would risk deleting intentionally staged author work.

## Runtime refusal added to the *existing* WLAN server

Source: `scripts/reader_provenance_gate.py`, imported by `scripts/serve_shared_shell_preview.py`. This gate is a **temporary fail-closed version pin**, not a new Reader and not a second publisher.

- Refuses startup if the purported accepted v140 source lock, Bookshelf HTML, or nine production/stage comparison assets **or the complete accepted 27-file Linotype runtime tree** do not match the recorded SHA-256 bytes. The complete tree inventory SHA-256 is `307a04e852c382229f45c43ed6ad075674b24e3fcf3cae51e012fbb223458569`.
- Protects all HTML in the `estate/`, `book/`, and `solstice/editions/` book roots. New or modified Reader HTML relative to the exact accepted v140 release yields **HTTP 403**, rather than an invented edition.
- Checks each GET/HEAD against the accepted baseline before serving; modified Reader runtime scripts/styles (including the legacy `book.js` compositor), audio modules, and previously unknown files beneath `estate/assets/linotype/` yield **HTTP 403**. Source-locked stage files cannot whitelist themselves.
- Allows unchanged v140 pages and unrelated non-Reader routes. Missing paths retain normal HTTP 404. Does not change public production.
- **Re-admission is deliberate:** reconcile production, source ownership, existing Reader runtime, approved stage-only deltas and manuscript fidelity, then review/update the pinned baseline in the same owning code path before staging another release. A mere new file or updated `source-lock.json` is insufficient.
- Not a claim that nobody with administrative SSH access can override a service. The current guarantee is for this installed, running canonical WLAN preview path. Public EstatePublisher/production requires separate admission and is unchanged.

## Regression checks

`python3 -m unittest discover -s tests -p test_reader_provenance_gate.py -v`

Includes actual GET and HEAD refusal tests, full source-baseline tests, changed-runtime and changed-audio-module tests, URL traversal refusal, and an explicit assertion that production/stage differ in the three declared JavaScript modules.

**Installed WLAN terminal receipt — 4 November 2026:**

- The existing `fountain-shell-acceptance-preview.service` was restarted with the source-owned gate imported in the **same** Python server. No new daemon, port, route, DNS name or publisher was created.
- Running `serve_shared_shell_preview.py` SHA-256: `ab0082a239661e3809cef9dbb4074e6dab4cb1c53e0ea71aacd305a1feaa8433`. Running `reader_provenance_gate.py` SHA-256: `5ea503b3f53c355a39d5d0ce2055e7c42cfc2a6f91c55d9c85b09e697c525342`. Both verified as the committed branch files before installation.
- The original preview server source was retained as `.serve_shared_shell_preview_before_reader_guard_20261104.py` on the stage host; guarded installation used fail-safe restoration on failure.
- Live active release remained `shared-shell-20261103-v140-same-folio-return`; `/estate/`, `/estate/editions/essays-continuing/`, and `/estate/assets/linotype/reading-first-app.js` each returned **HTTP 200**. Rejected new essay path returned its normal **HTTP 404** because it is not in the active v140 release.
- Independently exercised the **installed** HTTP `Handler` against the retained v141 artifact using a temporary loopback request handler (not a new deployed service): accepted `/estate/editions/essays-continuing/` returned **200**, rejected `/estate/essays/what-makes-a-page-modern/` returned **403 on GET and HEAD**. This is direct executable refusal, not merely a policy statement.
- **12 local regression tests passed** (including actual HTTP GET/HEAD and changed audio module refusal) and runtime file Python compilation passed. The production/staging Reader module mismatch is explicitly preserved.
- This prevents serving the specific unadmitted invented Reader through the canonical guarded WLAN service. It does **not** establish production/live iPad semantic acceptance, and administrative replacement of the server remains outside the guard's authority.

## Authoring rule

Future requests to “put this essay in Fountain Press staging” must **add the authentic admitted manuscript to the existing production-derived Reader's content model** and independently compare the resulting layout and behavior. The author must see an approved staged *book*, not an invented standalone reader. Never substitute passing generated-page tests for source or runtime provenance.

**Subsequent hardening, 4 November 2026:** the complete original v140 Linotype runtime directory (27 files; inventory SHA-256 above) is now pinned in addition to the nine independently compared production-facing files. This prevents swapping the older `book.js` compositor or introducing a new runtime module at an otherwise unchanged Reader route. Source-level tests: 12 passed. The initial live installation SHA values above describe the first guarded version; the strengthened version requires its own deployment and readback before runtime enforcement of the *whole-tree* condition can be claimed.
