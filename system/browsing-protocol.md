````markdown
# Browsing Protocol

Every persona-review subagent loads this file at the start of its run. It defines, exactly, how a persona "uses" a website.

## Step 1 — Sample the moment

Before opening the URL, the subagent reads the persona's `variance_envelope` and samples ONE value from each list:
- `mood_range` → mood for this visit
- `context_range` → browsing context for this visit
- `patience_range` → patience-on-the-day
- `time_of_day_range` → time of day
- `device_range` → device

Record the sampled values in the review's `entry_context` and `device_used` fields. Independent fresh runs of the same persona MUST resample independently — this is the source of intra-persona variance.

## Step 2 — Capture the page

Use the gstack `/browse` skill (or its current equivalent):
1. Open the entry URL.
2. Capture a hero screenshot (top of page).
3. Capture rendered HTML/text.
4. As the persona scrolls (Step 4), capture additional screenshots at scroll positions where the persona's eye actually settles.

Save screenshots to `reviews/{site}/{run-id}/screenshots/<persona-slug>-<sequence>.png`.

## Step 3 — Form the first impression

Based on the sampled moment + the persona's bio + the hero screenshot, write the persona's first reaction internally. This drives all subsequent decisions:
- If the hero violates one of the persona's `ui_pet_peeves` or fails their `aesthetic_suspicion_threshold`, the persona may bounce immediately.
- If a hero element matches their `trust_signals_valued`, they engage.

## Step 4 — Navigate as the persona would

Budget:
- Max 10 clicks per visit.
- Max 5 unique pages.
- Max 3 minutes simulated session time (subagent estimates wall-clock from patience + content density).

At each step, the subagent asks: **"Would THIS persona, in THIS sampled moment, click anywhere right now? Where?"** The persona's body section "Browsing protocol" drives this. If the answer is "no, they'd leave," they leave.

## Step 5 — Honesty rules

- If the persona would not have noticed an element, do not include it in `elements_noticed`.
- If the persona is jargon-illiterate, the narrative must show confusion, not gloss over it.
- If the persona bounces in 8 seconds, write a short narrative reflecting that. Do not pad.
- Do not Google the company. Do not check Trustpilot. Pure on-page reaction only.

## Step 6 — Voice rule

The narrative MUST be first-person in the persona's voice. Use the persona's `## Voice` section as the style anchor. No Claude vocabulary. No "the user might find that…" — only "I…" or the persona's natural phrasing.

## Step 7 — Score and emit

After the visit, fill in all required fields per `system/review-schema.md`. Scores must be integers 0–10 grounded in this specific visit (not the persona's general disposition). Write the file at `reviews/{site}/{run-id}/reviews/<persona-slug>.md`.

## What the subagent NEVER does

- Modify the persona file.
- Modify any other persona's review.
- Inject Claude's editorial recommendations.
- Re-run a previous review on top of an existing file.
- Skip the moment-sampling step.
- Write a third-person narrative.
````
