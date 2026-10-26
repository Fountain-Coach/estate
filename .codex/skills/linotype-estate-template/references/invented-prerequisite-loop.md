# The Invented-Prerequisite Loop — FCIS anti-pattern

**Named shorthand for discussions:** **Invented-Prerequisite Loop**. This is the explicit failure sequence established by the FCIS founding conduct standard, not the name of a new capability, test harness or security system.

> **Goal substitution -> speculative prerequisite -> implementation -> test-based legitimization -> new dependency -> moving Definition of Done.**

The loop begins when an agent reframes a working, bounded task as a reason to build an additional mechanism. It then tests the invented mechanism, mistakes passing tests for evidence of necessity, and uses that self-created dependency to move the finish line. Its hallmark is that **the user's original result remains unfulfilled** while the agent's new mechanism becomes compulsory.

## Binding source and EstatePublisher precedent

- **Normative:** [FCIS Founding Rule — Goal Fidelity and Non-Invention](https://github.com/Fountain-Coach/.github/blob/main/docs/FCIS-Non-Invention-and-Goal-Fidelity.md), adopted 20 October 2026. Governing maxim: *Do not invent the problem to justify the solution.*
- **Accepted amendment:** [Governance Chapter 07 goal fidelity amendment](https://github.com/Fountain-Coach/governance.fountain.coach/blob/main/docs/chapters/07-goal-fidelity-founding-amendment.md).
- **Actual failure/reversal:** [EstatePublisher Chapter 158 non-invention decision](https://github.com/Fountain-Coach/EstatePublisher/blob/main/docs/FCIS-158-non-invention-decision.md), dated 22 October 2026. The first static publisher required a new host helper and signed-grant ceremony; no observed SSH, rsync, atomic symlink or Caddy failure established their necessity. Synthetic tests passed, but validated only that invented design. The revision restored the owner's established SSH delivery path.
- **Publication contract:** [Governance Chapter 158 — Publishing Is Not a Distributed Transaction](https://governance.fountain.coach/chapters/158-publishing-is-not-a-distributed-transaction/). EstatePublisher compiles/verifies an authorized static release; bounded authenticated transport delivers; Caddy serves. Application Store replication, MIDI2 sessions and new remote-agent enrollment are not requirements for ordinary static publication.

## Required response when an agent declares a new blocker

Ask, and answer in the work record, the existing FCIS four-question decision test:

1. What precisely did the writer ask to observe or accomplish?
2. Which operation **actually fails now**, with what reproducible result?
3. Which **already binding** rule and demonstrated deficiency make the currently working mechanism insufficient?
4. What is the **smallest correction** and acceptance check on that same working path?

If an answer is missing, label the proposal **PROPOSED / NON-BLOCKING** and return to the original operation. Do not invent a new Definition of Done by adding security, identity, provenance, store, browser, staging, GitHub CI or host-enrollment ceremonies. Do not force the writer to repeat "proceed accordingly" or operate the agent's test environment.

## The important distinction for production-first staging

The writer **explicitly chose** a production-baseline-plus-declared-Git-delta staging policy. This requirement is real *for that requested canonical transition*: identify the relevant published production baseline, preserve affected routes/assets, apply only pinned Git changes, and verify the existing staging predecessor and actual release. It is **not** evidence that a new SSH account, remote helper, signing infrastructure, Store sync, or whole-estate testing service is required.

The existing EstatePublisher SSH transport (approved owner key/config, rsync, SHA-256 inventory, atomic symlink, retained rollback, independent HTTPS/WLAN readback) is a usable baseline. If its native code cannot enforce the new production-lineage guarantee, state **NOT YET GUARANTEED** and repair the smallest existing client-side gap *when that guarantee is the requested outcome*. Do not use this as a pretext to stop unrelated, already authorized static publishing. Never claim a procedural skill or successful invented mock tests supply the missing runtime guarantee.

**Illustrative refusal language:** "Your requested production-first staging guarantee is not proved by the currently installed EstatePublisher; its predecessor check concerns only staging. A small baseline comparison in the existing client may be necessary. Ordinary authorized SSH static publication remains a separate working capability; no new host identity or daemon is implied."

**Stop rule:** After the original requested capability is independently verified, stop. Record unrelated potential improvements as non-blocking proposals rather than recursively expanding the publication workflow.
