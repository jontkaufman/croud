---
name: improve
description: Generates an actionable improvement plan from a Croud review run. Reads the report + per-persona reviews, clusters findings by impact, produces prioritized recommendations with verbatim evidence, and optionally creates GitHub issues + schedules a re-review. Closes the loop from "we ran a review" to "here's what to ship and when to re-test." Trigger phrases: "/improve", "improve <site>", "what should I fix on <site>", "make a plan from the latest review", "turn this report into action", "close the loop on <site>".
---

# Improve

You are running this skill because the user has a Croud review run for a site and wants the actionable next step: a prioritized improvement plan, optionally with tickets and a scheduled re-test.

## When to use

- User has just finished a review run and asks "what should I fix?" or similar.
- User says `/improve <site>` or `improve <site>` (with or without an explicit run-id).
- User asks to "close the loop" on a review.

DO NOT use this skill to generate the original review or report — those are produced by the conductor's main review workflow.

## Step 1 — Resolve the source run

Required inputs:
- `<site>` — the domain that was reviewed
- `<run-id>` — optional; if missing, default to the most recent run for that site

If the user said `improve <site>` with no run-id, glob `reviews/<site>/` and pick the highest-sorted (alphabetically — run-ids are timestamp-prefixed) folder. Confirm with the user: "Using run `<run-id>` (most recent for `<site>`). OK?" — proceed unless they correct you.

If the user said `improve` with no site at all, list the sites under `reviews/` and ask which one. Don't guess.

If the report file at `reviews/<site>/<run-id>/report.md` doesn't exist, stop. Tell the user the run is incomplete.

## Step 2 — Load the source data

Read in order:
1. `reviews/<site>/<run-id>/report.md` — the aggregate, including pattern flags, conversion funnel, element-level reactions, verbatim quote board.
2. `reviews/<site>/<run-id>/reviews/*.md` — every per-persona review, for direct verbatim quoting and trust/clarity/intent scores.
3. `reviews/<site>/<run-id>/improvement-plan.md` — if it already exists, STOP and ask the user: "Plan already exists. Overwrite, append a new revision, or quit?" Default to quit.

## Step 3 — Compute the priority assignments

Walk the report's pattern flags + element-level reactions + bounce-point distribution. Assign each finding a priority using these rules:

**P0 — Critical conversion blocker** if the finding meets EITHER:
- ≥ 50% of the panel cited it as a top trust failure or bounce contributor, OR
- It caused above-the-fold bounces in ≥ 30% of the panel.

**P1 — Trust / target-market mismatch** if the finding:
- Meaningfully suppressed trust scores in a coherent persona segment (e.g. all 3 commercial-GC personas) without necessarily bouncing them, OR
- Surfaces a positioning ambiguity (audience targeting, competitive market, pricing tier).

**P2 — Copy, framing, message clarity** if the finding:
- Drew negative or confused responses from 3+ personas without driving a bounce.

**P3 — Mobile, accessibility, performance polish** if the finding:
- Was raised by 1-2 personas with specific device, accessibility, or context constraints.

If a finding fits two priorities, place it in the higher one. Don't double-list.

## Step 4 — Estimate effort per action

Heuristic, not precise. Use:
- **XS (hours)** — copy edit, single setting toggle, footer link, robots.txt change.
- **S (days)** — new public page (pricing, contact, security, integrations), removing a UI element, swapping a stat for a sourced version, jargon-replacement audit.
- **M (weeks)** — product screenshots, customer logos + first case study, video walkthrough, /security page with real SOC2 work, integrations page with named tools.
- **L (weeks–quarters)** — actual API integration, SOC 2 certification, marketplace listing, public sandbox, multi-page redesign.

If an estimate hides a real dependency (e.g. "depends on getting customer permission to use logo"), say so in one line.

## Step 5 — Write the plan

Write the plan to `reviews/<site>/<run-id>/improvement-plan.md`, conforming to `system/improvement-plan-schema.md`. The full schema is documented there; the skeleton is:

1. Frontmatter (site, source_run_id, panel, plan_type, generated, schema_version: 1).
2. Executive summary — 3-5 bullets, anchored in computed numbers.
3. P0 critical conversion blockers — each issue with title, evidence (count + verbatim quotes + persona slugs), actions (numbered + concrete), effort, expected lift.
4. P1 trust / target-market mismatch — same structure.
5. P2 copy, framing, clarity — same structure.
6. P3 mobile, accessibility, polish — same structure.
7. Sequencing recommendation — Week 1 / Weeks 2-3 / Weeks 4-6 / Quarter+, each a bulleted list referencing P-ids.
8. Validation plan — markdown table of baseline vs post-fix targets for trust, intent_to_act, would_return, would_recommend, hero-bounce %, plus per-finding metrics.
9. Out-of-scope — short bulleted list of what this plan deliberately does not cover.

After writing, run nothing — there is no `validate_improvement_plan.py`, but you should self-check that:
- Every P-section item has both an evidence subsection AND an actions subsection.
- Every quoted line traces back to a real per-persona review file.
- No P0 issue lacks a citation.

## Step 6 — Offer the optional next steps

After the plan file is written, surface a short menu to the user. Ask via `AskUserQuestion` (or inline if unavailable):

1. **Create GitHub issues from P0 items.** If the repo has `gh` CLI auth and a remote, run `gh issue create` per P0 with the issue title = the P0 issue title, body = the evidence + actions + effort + expected-lift sections, and labels `croud-recommendation` + the priority tag (`p0`).
2. **Schedule a re-review.** Use `CronCreate` to schedule a Croud review of the same site with the same panel-selection parameters, default 30 days out. Tell the user the cron expression you'll use; let them adjust.
3. **Both.**
4. **Neither — just the plan file is enough.**

If they pick option 1 or 3, before creating the issues, list the issue titles you'll create and ask "OK to create N GitHub issues?" with a confirm. NEVER create tickets without explicit confirmation — these are visible-to-others actions.

If they pick option 2 or 3, before creating the cron, summarize what will run and when. Confirm before scheduling.

## Step 7 — One-line summary on completion

Print:
```
✓ Improvement plan: reviews/<site>/<run-id>/improvement-plan.md
✓ N P0 / N P1 / N P2 / N P3 issues identified
[✓ Created N GitHub issues]    (only if user opted in)
[✓ Scheduled re-review for <date>]    (only if user opted in)
```

## Hard rules

- Recommendations are Claude's voice — that is appropriate at the plan layer (and only at the plan layer). The reviews + report stay strictly in persona-and-stat territory.
- Every recommendation MUST cite specific persona evidence by slug + verbatim quote. No "best practices" with no panel grounding.
- Every priority assignment MUST be derivable from the report's data. Don't promote findings to P0 because they "feel important."
- DO NOT generate generic UX advice not grounded in this specific run's evidence (e.g. "consider improving your hero image" with no persona who said so).
- DO NOT modify or overwrite an existing plan without explicit user confirmation.
- DO NOT create GitHub issues, post to Linear, schedule cron jobs, or take any other side-effect-bearing action without explicit user confirmation immediately before the action.
- DO NOT modify the source report or any per-persona review file. The plan is downstream of those; it never edits them.
- If the source run had < 5 personas, note this caveat in the executive summary: "Plan derived from a small panel (n=<N>); priorities should be re-validated with a wider sample."
