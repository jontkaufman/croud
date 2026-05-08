````markdown
# Report Schema

Every aggregate report at `reviews/{site}/{run-id}/report.md` MUST contain these sections in this order. Reports are designed to be consumed by a downstream LLM agent (the user's business wiki) for design and content optimization.

The report contains zero Claude opinions or recommendations. Everything is computed from the per-persona review files or quoted verbatim.

## 1. Frontmatter

```yaml
---
site: <domain>
run_id: <YYYY-MM-DD-HHMM-selector-runtype>
timestamp: <ISO8601>
panel_size: <int>
selection: <free-form description, e.g. "random sample of 50 from 127-persona library">
run_type: <fresh|freshN|return-N|mixed>
schema_version: 1
---
```

## 2. Selection criteria

A short paragraph documenting how personas were selected for this run (sample size, filters applied, library size at run time).

## 3. Aggregate scores

Markdown table with mean, median, std, min, max for each numeric metric: trust, clarity, intent_to_act, visual_appeal, copy_quality.

## 4. Conversion funnel

Counts and percentages: reached site, scrolled past hero, reached pricing (if present), reached primary CTA, would_return, would_recommend.

## 5. Bounce-point distribution

Markdown table: bounce_point, count, percentage. Includes "finished page" as a category.

## 6. Cuts by dimension

Per-tag breakdowns with score deltas. At minimum: age_bucket, device_primary, tech_literacy, patience, trust_disposition, location_type, expertise_overlap. Each cut is its own table.

## 7. Element-level reactions

For each UI element type that appears in `elements_noticed` across the run: positive count, negative count, neutral count, plus 2–4 representative verbatim quotes attributed to persona slug.

## 8. Verbatim quote board

Themed (Hero / Trust / Copy / Visuals / Pricing / CTA / Mobile / Accessibility / etc.). Each quote attributed: `"quote" — slug (age, gender, device)`. Quotes pulled verbatim from the per-persona review narratives.

## 9. Pattern flags

Factual observations only — never recommendations. Examples:
- "14/31 mobile-first personas bounced at hero (vs 4/19 desktop)"
- "0/50 personas clicked any footer link"
- "Personas with low domain_expertise_overlap (n=22) scored clarity 3.2 avg vs 6.4 for high (n=14)"

## 10. Per-persona index

Bullet list of links to each `reviews/<slug>.md` file with one-line summary (e.g. "bounced at hero (14s)", "reached pricing, did not convert (1m 47s)").

## Hard rules

- The report is generated ONLY from the per-persona review files in the same run folder. Stats must be computable from those files.
- Quotes must be verbatim from the narratives. No paraphrasing.
- No section may contain Claude's editorial voice. Pattern flags state observations; they do NOT prescribe action.
- If a section has no data (e.g. no personas reached pricing), say so: "0/50 personas reached pricing." Do not omit the section.
````
