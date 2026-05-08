````markdown
# Improvement Plan Schema

Every improvement plan at `reviews/{site}/{run-id}/improvement-plan.md` MUST conform to this schema. An improvement plan is the actionable translation of a review run's report into prioritized, evidence-backed website changes.

The plan is the ONE Croud artifact where Claude's editorial voice IS appropriate. Reviews and reports stay strictly in persona / computed-stat territory; the plan layer translates those signals into concrete recommendations a team can act on. Every recommendation must still cite the persona evidence it traces back to — verbatim quotes, persona slugs, counts.

## Frontmatter (required)

```yaml
---
site: <domain>                                  # required
source_run_id: <YYYY-MM-DD-HHMM-...>           # required, the run this plan is derived from
panel: <free-form description>                  # required, e.g. "10 construction-domain personas"
plan_type: website improvement plan             # required, fixed
generated: <YYYY-MM-DD>                         # required
schema_version: 1
---
```

## Body sections (required, in this order)

### 1. Executive summary

3-5 bullets stating the most consequential findings of the run. Anchor every bullet in computed numbers from `report.md` (panel size, mean trust, percentage of personas affected by a recurring issue, conversion-funnel deltas). State the cheapest highest-impact fix opportunity in one bullet.

### 2. P0 — Critical conversion blockers

The smallest set of issues that, if fixed, would close the largest share of bounces. Inclusion criteria: each P0 issue must affect ≥ 50% of the panel OR cause an above-the-fold bounce in ≥ 30% of the panel.

For each P0 issue:

- **Issue title** — short imperative phrase ("Restore contact information across the site").
- **Evidence.** Count of personas affected, with their slugs. Then 2-3 verbatim quotes attributed by slug.
- **Actions.** Numbered, concrete, implementable. No vague verbs ("improve UX"); use specific verbs ("add", "remove", "rename", "expose at", "link from").
- **Effort.** One of: XS (hours), S (days), M (weeks), L (weeks–quarters).
- **Expected lift.** What metric this is expected to move and approximately by how much.

### 3. P1 — Trust and target-market mismatch

Issues that don't usually cause an immediate bounce but cap how high the trust ceiling can go. Same per-issue structure as P0.

### 4. P2 — Copy, framing, and message clarity

Items that consistently soften trust without hard-bouncing visitors. Same per-issue structure.

### 5. P3 — Mobile, accessibility, and performance polish

Lower-frequency issues, often visible only on a particular device or assistive-tech profile. Same per-issue structure.

### 6. Sequencing recommendation

Bucket every action across P0–P3 into four time buckets:

- **Week 1 (XS / hours)**
- **Weeks 2–3 (S / days)**
- **Weeks 4–6 (M / weeks)**
- **Quarter+ (L)**

Each bucket is a bulleted list of actions referenced by their P-id (e.g. `P0.1`, `P2.3`).

### 7. Validation plan

A markdown table comparing baseline (this run) against post-fix targets. Include at minimum: trust mean, intent_to_act mean, would_return count, would_recommend count, hero-bounce percentage, plus any per-finding metric named in expected lifts.

State the recommendation explicitly: "After implementing the P0 set, re-run the same panel via a fresh Croud run on the production site."

### 8. Out-of-scope

A short bulleted list naming things this plan deliberately does not cover (product capability, sales strategy, SEO, etc.). Reduces scope creep when the plan is consumed downstream.

## Hard rules

- Every recommendation MUST cite persona evidence. No "best practices" or generic UX truisms.
- Every quote MUST be verbatim from a per-persona review file in the same run folder. No paraphrasing.
- Every priority assignment (P0/P1/P2/P3) MUST be derivable from the count + severity of evidence in the report. Don't put a finding in P0 because it "feels important" if only 1/10 personas mentioned it.
- Effort estimates are heuristic. Use a one-line note in the action section if the estimate hides a non-obvious dependency.
- The plan does NOT predict outcomes the system can't justify. "Expected lift" is a directional estimate grounded in panel response, not a precise forecast.
- Out-of-scope must be honest about what the plan can't address (e.g. underlying product capability, market positioning beyond website copy).
````
