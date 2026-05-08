````markdown
---
name: generate-persona
description: Generates one or more new persona files for Croud. Modes: random, tag-spec, fill-gaps, batch. Always appends — never modifies existing personas.
---

# generate-persona

Generates new persona files in `personas/`. Updates `personas/_index.md`. Appends only — never modifies or deletes existing files.

## Modes

### random
User asks for N personas with no constraints (e.g. "generate 10 personas").

Behavior:
1. Read `personas/_index.md` and `system/diversity-matrix.md`.
2. Compute current coverage per matrix axis.
3. For each new persona:
   - Bias picks toward underrepresented axis cells.
   - Sample one value per matrix axis.
   - Generate a coherent bio using the picks (life, online behavior, voice, biases, browsing protocol).
   - Compose tags from the picks.
   - Generate a `variance_envelope` with 2–4 values per range.
4. Validate each new file with `python scripts/validate_persona.py personas/<slug>.md`.
5. Update `personas/_index.md`.

### tag-spec
User specifies constraints (e.g. "generate 10 personas — rural, low-tech, over-60").

Behavior:
1. Lock the user-specified axes.
2. Randomize remaining axes (still biased toward gaps).
3. Otherwise as random mode.

### fill-gaps
User asks to fill gaps (e.g. "fill gaps in the persona library").

Behavior:
1. Read `_index.md` and `diversity-matrix.md`.
2. For each axis with under-coverage (< 1 representative per cell, or < 5% of total roster), prioritize generating personas covering those cells.
3. Default to 10 personas unless user specifies otherwise.

### batch
User asks for a multi-persona batch (e.g. "generate 15 personas"). This is the default working cadence.

## Hard rules

- ALL frontmatter keys from `system/persona-template.md` are required. Do not omit any.
- Every body section must contain real content. No placeholders.
- Names must span ethnicity and region authentically. Do not default to one demographic pattern.
- Each persona's `## Voice` section must be distinct in vocabulary and cadence from neighboring personas.
- Bios may contain real-life contradictions (the wealthy tech-illiterate; the careful teen).
- Each `variance_envelope` list must contain at least 2 values, drawn from the persona's realistic range — not the full enum.
- Slugs must be kebab-case and unique.
- Generated files MUST validate clean against `scripts/validate_persona.py` before commit.

## Forbidden

- Do not modify existing persona files.
- Do not delete persona files.
- Do not skip the validator.
- Do not write generic "John Smith, 35, accountant" filler.
- Do not write reviews here. This skill only writes personas.

## Output

For each generated persona:
- A new file `personas/<slug>.md` conforming to `system/persona-template.md`.
- An updated entry in `personas/_index.md`.

After generation, report to the user:
- Count generated.
- Slugs created.
- Validator pass/fail for each.
- A coverage delta (which matrix cells went from 0→1, etc.).
````
