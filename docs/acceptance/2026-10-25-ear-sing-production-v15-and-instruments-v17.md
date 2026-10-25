# Ear / Sing essay — public production and reciprocal Instruments release

**25 October 2026 · Verified public production following explicit author approval after v34 staging proofreading.**

The original essay source owner is `Fountain-Coach/fountain.coach@61f264d39615c66a3c5bd9e8359979c3c5c23575`; its source-addressed listening adapter is owned by `Fountain-Coach/SatzfunkPlayer@b0e3461cc2d73ab7325373be93d5436d5e091f8c`. The reciprocal catalogue source owner is `Fountain-Coach/instruments.fountain.coach@69ec0e5e87db33934463e0e29076cbbe4f5b2cd0`. The author explicitly granted public promotion of *The Ear That Learns* and its original synthetic recordings. No Japanese human singer, PJS audio, or private Satzfunk archives are authorized for this release.

## Fountain Coach exact-host public v15

The live 26-file production v14 predecessor, `estate-20261024-v14-satzfunk-reel-estate`, was inspected via SSH and the affected HTTPS baseline read back (root `f234a80c286c27e2f147096c5421d2a8d54aed2339fc5ad9a3e5a5d2eda5f918`, collection `30bf86c2c53e299cf60fe76410fd2fbd2c3257a08e10769c6fa2ef51ba6bfcbb`, CSS `d8a6e65183510323ebba5c45b28d8663205d55a00111b214a25b59766262e97f`). The prebuilt v15 candidate `estate-20261025-v15-ear-sing-61f264d` preserved 22 baseline files byte-identically, modified four existing files, added seven essay/audio files, and deleted nothing. Original *The Composable Book* and earlier essays remain.

Caddy's verified existing `@fountainNewEssay` matcher lacked the new essay and `/assets/site.css` routing. Exactly one host-specific matcher line was extended, validated and reloaded. Old Caddy SHA-256 `277203a076bda8a3a1ff518d2efeb754c2dfec2554b647919e1c394fa018f110`, new `74489ff88a5782f7871a251b03ba2c2f0857f7f65c07228b4b0fcdf934f3c9f9`, original backed up at `/etc/caddy/Caddyfile.before-ear-sing-20261025`. [Preserved matcher diff](2026-10-25-ear-sing-fountain-caddy-public-route.diff).

The installed typed `EstatePublisherSSHDelivery` passed exact-host preflight and returned **`state=active`, `activated=true`**, preserving v14 rollback. **Ten** independently SHA-verified public HTTPS witnesses cover the new essay, all 3 original synthetic AAC takes, the player, image, stylesheet, homepage, complete Essays collection and earlier *Composable Book*. Real Chrome on public HTTPS confirmed 3 player choices, 4 time-addressed comments each, 2.15-second seek and direct deep link, light/dark and mobile geometry, and no browser errors.

## Instruments exact-host public v17

The previous 30-file Instruments v16 `estate-20261024-v16-instruments-assets-5ac718e` had homepage hash `68f654280e64b15b0c1c04585b47c05c0b1a067bc95112d55c261786ace18d4d`. Production v17 `estate-20261025-v17-ear-sing-links-69ec0e5` changes **only `index.html`** to `43df71cbef77c225ad58c8a27edec390fc2942a15fd0c75bf4b5c07200557460`, adding the two previously authored Sing/Ear links to the canonical essay. All 29 other files are unchanged, zero added/deleted; v16 rollback retained. The installed typed publisher returned active with **six** exact HTTPS byte checks. Real public desktop and mobile Chrome clicked the Ear link, arrived at the live published essay and 3-take player, and found no overflow/JS errors. No Caddy change required.

## Boundaries and receipts

- Active public `fountain.coach` → `releases/estate-20261025-v15-ear-sing-61f264d`.
- Active public `instruments.fountain.coach` → `releases/estate-20261025-v17-ear-sing-links-69ec0e5`.
- Hetzner Caddy remains active. Only those approved exact-host releases and the scoped Caddy matcher were altered.
- Canonical Ubuntu WLAN stage remains **`shared-shell-20261025-v34-ear-sing-dark-9f49cc1`** with existing service active; no stage-state mutation or promotion by shortcut occurred.
- Public essay: `https://fountain.coach/essays/the-ear-that-learns/`. Public catalogue: `https://instruments.fountain.coach/`.
- Human singer recordings, Japanese source-blind phoneme recognition, vocalist qualification, Reframe Bookshelf membership, production of private source files, and native physical iPad Safari testing are **not** claimed.

Complete original typed manifests, release receipts and baseline deltas are preserved in the respective [Fountain Coach](https://github.com/Fountain-Coach/fountain.coach/tree/main/docs/releases) and [Instruments](https://github.com/Fountain-Coach/instruments.fountain.coach/tree/main/docs/releases) owning repositories. This Estate note is an independent operational witness, not a substitute for those original typed receipts.
