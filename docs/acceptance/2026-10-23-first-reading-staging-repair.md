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

## Active stage and independent readback

EstatePublisher activated shared-shell-20261023-v12-first-reading-ad04d80-r2
using source revision ad04d80e750115fd292d0f5501965456e4532dd2.
The prior immutable v11 release remains retained. All 443 candidate files
were independently SHA-256 verified on Ubuntu before activation; nine typed
HTTP witnesses passed. The current symlink and existing user service were
independently observed active after delivery.

[Terminal receipt](2026-10-23-first-reading-stage-terminal-receipt.json).
[All 92 live HTTP/hash witnesses](evidence/2026-10-23-first-reading/live-http-witness.json).
[Native macOS WebKit witness](evidence/2026-10-23-first-reading/native-webkit-live-witness.json)
and [live screenshot](evidence/2026-10-23-first-reading/native-webkit-live-landscape.png).
Native WebKit proves a working spread, Next and Contents with no visibly broken
images. This is macOS WKWebView evidence, not a physical-iPad Safari claim.

The public edition root remains exactly
3faddbff97117fbe4e528ead6b714a093932d6f425806517d9c0ee8c18fb0e09.
The staged edition and all 92 dependencies are exact public source bytes.
No public release occurred.

### Transport refusal and correction

The first typed attempt refused activation because macOS generated an extra
AppleDouble /._source-lock.json when copying from the external volume.
Its refusal receipt is retained. The existing v11 stayed active.
The second attempt used the same 443 approved byte hashes copied into plain
local files without external-volume metadata and COPYFILE_DISABLE=1.
The same native publisher then verified and activated the new immutable
-r2 candidate; no remote helper or verification bypass was introduced.

This repair establishes First Reading's staging integrity. It does not
constitute whole-estate public release acceptance.
