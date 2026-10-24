# Lucide is the estate's functional icon family

**24 October 2026 — author direction.** The author observed visual drift in logo and icon treatments and explicitly requested consistent reuse of the already selected icon set. The set is **Lucide Icons**, adopted in the Instruments semantic triptych as **lucide-static v0.468.0 (ISC)**. This is a rule for consistent graphical semantics, not a requirement that independent publications use a single generic brand.

## Functional icon contract

- For actions, functional capabilities, menu controls, instrument categories and their associated catalogue or social previews, **prefer the same canonical Lucide glyph and base SVG path data**, rather than drawing new ad hoc pictograms, using emoji substitutes, inventing SVG interpretations or mixing unrelated icon families.
- In the published Instruments triptych, the accepted mapping is **Sing → microphone; Ear → ear; SatzfunkPlayer → clapperboard**. Source: `Fountain-Coach/instruments.fountain.coach/docs/decisions/2026-10-24-semantic-instruments-staging.md`. Three existing assets in Instruments were already regenerated with the original Lucide static path data. Do not claim new assets or a deployment on the basis of this decision.
- Preserve comparable viewBox/stroke conventions and optical sizes across identical functional contexts, neutral icon treatment and visible keyboard-focus/accessibility semantics. Maintain accessible names as text; a vector alone is not a title or an instrument identity.
- Include applicable upstream licence notices beside distributed SVG source or in the owning static publication artefact. Serve icon assets from each approved domain's source-owned static files, not a network-dependent icon-service/runtime dependency.
- **Do not replace the Fountain Coach canonical brand logo, publisher mark, attributed artwork, book cover or an edition's authored visual motif with Lucide.** Brand identity, cover art and functional wayfinding have different semantic owners. A brand is never established by reusing a catalogue icon.
- Shared publication shells should use the same established design tokens for icons where they express the same action. The owner's page body can remain editorially distinct; no global runtime wrapper or wholesale redraw is justified.

## Drift and admission

For each independently scoped affected route, compare the actual published icon SVG geometry, CSS, accessible label, published artwork identity and currently accepted owner Git revision. Replace proven inconsistent *functional* glyphs at their owning Git source only. Verify that fixed icons and their social or secondary representations actually show the same Lucide sign. Preserve surrounding type, shell, footer and reader mechanics. Follow Git development → canonical WLAN staging → separately authorized public deployment, with independent browser/HTTPS witness and rollback.

**Observed 24 October:** Sing, Ear and SatzfunkPlayer in the author's screenshot already show the three matching adopted Lucide glyphs. Do not manufacture a repair for them. This decision prevents future drift on other surfaces; it is not a blanket authorization to revise every logo or deploy new imagery.
