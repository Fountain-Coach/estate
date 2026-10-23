# First Reading WLAN staging repair — 23 October 2026

User goal: repair the broken staging counterpart of the existing public edition.
Public production is outside this operation.

## Reproduced fault

The active v11 artifact omitted all 45 resources declared in its inherited
Solstice asset inventory: 4 CSS/JavaScript files and 41 original images.
It also omitted all 30 linked standalone readings and the proof workbench.
An inherited empty missingAssets array and eleven root-HTML readbacks did
not establish a functioning book.

## Bounded correction

The builder now merges each SHA-256-pinned predecessor reader asset from
/solstice/assets, rejects missing/conflicting inputs and completes the public
edition dependency graph before inventory. First Reading remains an exact
source-owned full-viewport book with its original toolbar; the common estate
masthead remains on the Solstice domain entrance. The edition must not be
wrapped in a second masthead that changes its usable page geometry.

The reading graph contains 92 independently fetched public files, including
33 HTML routes (edition, 30 standalone readings and two proof workbenches).
The full original 45-resource inventory is verified. Local static acceptance
separately checks the 173 common-shell routes and the exact reading graph.

## Verification

15 focused Python tests pass, including deliberate missing/modified resource
refusal. Chromium comparison proves the same source and candidate pagination
at matching geometry: landscape spread, portrait single page, working Next and
Contents, no failed resource requests or JavaScript errors. Hidden lazy images
in the original source are not broken requests; all 41 image byte hashes are
independently verified.

Deployment and live readback are recorded below after the existing typed
UbuntuEstateShellWLANStage delivery. No public publishing is authorized here.
