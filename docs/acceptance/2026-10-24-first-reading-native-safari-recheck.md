# First Reading — native Safari report and bounded recheck, not a repair claim

**24 October 2026.** The author supplied a macOS Safari screenshot of `https://works.benedikt-eickhoff.de/solstice/editions/first-reading/` showing the raw linear source cover running into the next editorial section and cut behind bottom pagination controls, rather than a proper composed sheet. The observed screenshot is a genuine unacceptable display state.

## Observed present state

- Current public HTTPS first-reading index SHA-256: `3faddbff97117fbe4e528ead6b714a093932d6f425806517d9c0ee8c18fb0e09`.
- Current public `solstice/assets/book.css`: `a2b335a3b2b3ecf3a34dc84bf7c309409b9acf073b142970c15ad2c4fcff661d`.
- Current public `solstice/assets/book.js`: `205d8c1fb36a81df21c0ff4895a5c545f8ce9ba623b9f56528d22f0d9a1c7b39`.
- Current public `solstice/assets/linotype-engine.js`: `09cb3a9d94668abbf26d4cf4639be15999e153b364f2a8fa39337f28e8c34d6f`.
- Current authoring `Fountain-Coach/solstice.fountain.coach` Git HEAD `ce30b16376345730cc16509919af6ced6b46a217` contains different `book.css`, `book.js`, `linotype-engine.js` and edition HTML bytes from public production. `Fountain-Coach/fountain-press` Git HEAD `c3550849b16b610690ac6506e45722de599ad2eb` also owns a newer version of the runtime. **Do not silently substitute unverified latest source for the user's published edition.**
- A fresh **native macOS Safari** tab on the authorized Mac was opened and queried through Safari's own AppleScript JavaScript execution. After initial load, `document.body.dataset.bookReady` was `true`, `document.body.className` was `book-app reader-ready`, `#book-flow` had computed `display:none`, and the single `.linotype-stage` had `data-mode=spread`. A second stepwise fresh navigation observed initial DOM unready at 0 s and successful `reader-ready` at ~0.678 s/1 s. The first query showed a saved reading position around `80–81 / 169`; individual font measurement and saved position can change totals.
- Independent Chromium on the same public URL returned HTTP 200 with `bookReady=true`, `sourceDisplay=none`, a measured stage, and `1 / 186` leaves in a clean temporary profile. This is not Safari parity proof.
- The user's original reported failure was **not reproduced** as a persistent native Safari failure during this short check. Its cause is not yet proved. Browser cache state, a transient startup interval, a typesetter catch/fallback and display geometry remain hypotheses, not findings. No browser preferences were altered, no source code was changed, and public production was not redeployed.

## Bounded outstanding acceptance

Before announcing that this visual defect is repaired, reproduce the user's exact native macOS Safari view, capture the actual reader state and JS error/measurement (if fallback), and verify whole A-series cover bound, underlying folios, next/previous and print/appearance behavior. Make the smallest correction in the owning Fountain Press/Solstice static source and stage it on the existing canonical WLAN server, using the verified public asset baseline. Verify exact rendered sheets in Safari and independently read back the stage; separate public release approval remains needed.

This evidence records a known screenshot discrepancy and a different result from a fresh native run, **not** a claim that the user's reported defect was imaginary or fixed.
