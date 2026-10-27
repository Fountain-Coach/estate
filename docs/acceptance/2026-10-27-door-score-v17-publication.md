# The Door Is a Score — production publication and FCIS 158 recovery

27 October 2026. Exact public release: `estate-20261027-v17-door-score-semantic-9947db4`.

## Authored scope

- Source owner: `Fountain-Coach/fountain.coach`, source commit `9947db4598362cd63eb4a598a19a2b7288c2b393`.
- Estate semantic update: home/essays collection and publication manifest; Teatro opening/social score and audio preserved.
- Previous production release: `estate-20261025-v16-ear-sing-social-124c9fa`, retained for rollback.

## Actual execution

Published using the existing owner SSH/Caddy static deployment capability `Fountain-Coach/EstatePublisher` from branch-local source. The selected public host was `fountain.coach` only. The explicit Caddy route allowlist gained three entries for `/essays/the-door-is-a-score`, its slash form and descendant assets; other host rules were unchanged.

The local standalone publisher prepared a 65-file manifest, passed preflight and 11 Swift tests, transferred the immutable release, verified its complete staged SHA-256 inventory, atomically changed the existing `current` symlink, validated and reloaded Caddy, and checked HTTPS bytes independently.

Native terminal receipt: `/Volumes/DockerDisk/codex-estate-runs/door-score-20261027/standalone-static-v17-receipt.json`, `state=active`, `activated=true`, predecessor retained.

Verified public files:

- `/essays/the-door-is-a-score/index.html`: `5c0e63d041f573688d514a2e7bf5109ba3bd9d0892a00e1f05c3b854bd4a901b`.
- `/essays/the-door-is-a-score/assets/teatro-door-score.png`: `47791d9ac527641ae7b2cfe7ffe7111a99b9e39afaf89b28e53d4fa3d44cd4bb`.
- `/essays/index.html`: `5e4599d6f4830b3ea8f3c1dae00cb2cb179fb76f27858da58295eef809bf3526`.

Independent follow-up returned HTTP 200 on the article, image, OGG and MP3 audio, Csound JavaScript, essays collection, Ear essay and home. Live HTML announces the proper canonical Open Graph image, dimensions and JSON-LD semantics. Remote witness confirmed `current` points to v17, Caddy is active and v16 still exists.

## FCIS lesson

This publication had previously been obstructed by unnecessary Store replication and signing/credential dependencies. FCIS Goal Fidelity and Non-Invention and current Governance Chapter 158 required reversal to the accepted bounded SSH release path. The effective change was minimal, limited to Caddy route admission inside the existing publishing transport, with rollback and public readback. No additional Store, agent, identity or approval ceremony was needed.

The branch-local publisher's route-admission source patch needs a separate genericity/code review before promotion to the canonical publisher main branch. That follow-up is **not a condition of this already verified publication**. No Facebook post was made.
