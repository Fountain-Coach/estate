# The Door Is a Score — v18 corrected reel and Facebook social card

Date: 2026-10-27. Repaired route: https://fountain.coach/essays/the-door-is-a-score/

Source owner: Fountain-Coach/fountain.coach, branch essay/the-door-is-a-score-20261027, exact authored commit 387682c010d6e1b9c3e817466d6e473241341d9a.

Previous release: estate-20261027-v17-door-score-semantic-9947db4.
New active release: estate-20261027-v18-door-score-social-reel-387682c.
Native publisher receipt: /Volumes/DockerDisk/codex-estate-runs/door-score-20261027/standalone-static-v18-social-receipt.json, state=active, activated=true, HTTPS byte witnesses passed.

Bounded delta from 65-file predecessor to 66-file immutable release:
1. estate-core.css shows navigable, labeled nine-item reel on <=62rem instead of clipping to three unlabeled icons in a horizontal overflow rail.
2. authored article HTML corrects publication status and declares a new JPEG for og:image and twitter:image (1200x600).
3. New file /essays/the-door-is-a-score/assets/teatro-door-score-social-v2.jpg, 113395 bytes, derived from the preexisting Teatro hero illustration; original full-resolution hero and audio assets preserved.

Verified terminal published byte witnesses:
- /essays/the-door-is-a-score/index.html SHA256 1cdbca31c1685d4146aa05c35cad79558c83aaacb56dde1674178f9efcd7251a
- /essays/the-door-is-a-score/assets/teatro-door-score-social-v2.jpg SHA256 b9bc81910e2fb270dbf1c281b1ca59a1d874291617d9bc19ae32322ccd088fef
- /essays/index.html SHA256 5e4599d6f4830b3ea8f3c1dae00cb2cb179fb76f27858da58295eef809bf3526

Independent post-release readback: new JPEG HTTP 200, image/jpeg, 113395 bytes; Caddy active and current points to v18, predecessor retained; HTTP 200 on essays index, Ear essay, and homepage.

Facebook acceptance: Safari logged-in Sharing Debugger at https://developers.facebook.com/tools/debug/?q=https%3A%2F%2Ffountain.coach%2Fessays%2Fthe-door-is-a-score%2F . Submitted its existing "Erneut scrapen" form. After reload, scraper last-read advanced from approximately four hours to 24 seconds earlier; CDN preview points at teatro-door-score-social-v2.jpg and image loaded complete with naturalWidth=540, naturalHeight=282. Facebook reports HTTP 206 for a ranged scrape and warns missing optional fb:app_id, but its generated link preview includes the new image. No Facebook post was authored or changed.

FCIS lesson: use source-owned contract and exact production predecessor, publish bounded immutable deltas through established SSH/Caddy transport, and inspect *Facebook's actual cached card*, not solely og:image markup.
