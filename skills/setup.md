---
name: setup
description: First-run onboarding for Croud. Walks a new user through environment checks, asks 3-5 questions about what they want to review and who their audience is, generates a starter persona library tailored to their answers, and lands them on a concrete first command. Trigger phrases: "/setup", "set me up", "help me get started", "onboard me", "I just cloned this".
---

# Croud Setup

You are running this skill because the user just cloned the repo and wants to get oriented. Walk them through the steps below in order. Be warm but concise. Do not skip steps.

## Step 1 — Confirm environment

Run these checks silently and only surface failures to the user:

1. `python3 --version` — needs 3.9+. If missing, tell the user to install Python from python.org and stop.
2. Check whether the project's Python deps are installed:
   ```
   .venv/bin/python -c "import frontmatter, yaml" 2>&1
   ```
   If this fails:
   - If `.venv/` exists but is missing deps, run: `.venv/bin/pip install -r requirements-dev.txt`
   - If `.venv/` doesn't exist, run: `python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt`
3. Verify `system/`, `personas/`, `scripts/`, `skills/` directories exist. If any are missing, the clone is incomplete — tell the user to re-clone.

If everything passes, just say: "Environment looks good." Then move on.

## Step 2 — Welcome and orient

Tell the user, briefly:
- What Croud does (point Claude at a website; Claude — embodying personas — reacts as those personas would; outputs a structured report).
- What they'll do in the next 2 minutes: answer a few questions, generate a starter persona library, run a sample review.
- They can quit at any time and come back later — none of the questions create irreversible state.

## Step 3 — Ask the questions

Use a single `AskUserQuestion` call with these questions (or ask them inline if `AskUserQuestion` isn't available in the host environment).

**Q1 — What do you want to use Croud for?**
- Reviewing a website I'm building or operating
- Reviewing a competitor or reference site
- Auditing a product launch / landing page
- Just exploring the tool — no specific site yet

**Q2 — Who is your target audience? (Free-form)**
Examples to nudge them: "small business owners thinking about adopting accounting software," "gen-z buyers of skincare," "B2B procurement managers at mid-market manufacturers," "rural homeowners looking for solar quotes," or "general public — broad demographic spread."

If they answer "general public" or similar, default to broad demographic generation (the existing `generate-persona` skill's `random` mode with diversity-matrix coverage).

If they give a specific audience, you will translate it into tag-spec constraints for the generator (e.g., "B2B procurement at mid-market manufacturers" → tags like `b2b-buyer`, `procurement`, `decider`, `mid-market`, mostly desktop, mostly power-user / professional tech literacy).

**Q3 — How many personas do you want to start with?**
- 5 (smoke test — fast, low cost)
- 10 (recommended starter — broad coverage, ~$1-3 cost depending on model)
- 25 (deeper coverage; ~$3-8)
- 50 (full panel; ~$5-15)
- I'll generate them later

**Q4 (optional, only ask if they answered "Reviewing a website I'm building" or "competitor" in Q1) — What's the URL?**
Free-form. They can also say "I'll provide it later."

**Q5 (optional) — Do you want screenshots saved to git?**
- Yes — track them in version control (default in `.gitignore`, but you can override)
- No — keep them local only (smaller repo)

## Step 4 — Generate the starter persona library

Based on Q2 and Q3:

- If the user picked "I'll generate them later," skip generation. Show them how to do it themselves later (`generate N personas — <tag-spec>`).
- Otherwise, dispatch the persona generator using the existing `skills/generate-persona.md` skill.
  - For broad audiences: `generate N personas` (random mode, biased toward diversity-matrix gaps)
  - For specific audiences: `generate N personas — <derived tag-spec>` (tag-spec mode)
- For 10 or fewer, dispatch in parallel (one subagent per persona). For more, batch in groups of ~10 to manage rate limits.
- After generation, validate every file: `.venv/bin/python scripts/validate_persona.py personas/*.md`
- Update `personas/_index.md` with the new entries.

## Step 5 — Hand off to a first command

Show the user a short cheat sheet of the most useful commands. Adapt the URL example to whatever they answered in Q4 (or use `example.com` as a placeholder).

```
review <URL> as <persona-slug>          # single-persona review (cheapest, fastest)
review <URL> with 5 personas            # random sample of 5
review <URL> with <tag>                 # everyone matching a tag
generate 10 personas — <tag-spec>       # add more personas later
list personas tagged <tag>              # query the library
show last review of <URL>               # reload the most recent run
```

Suggest one specific next command based on their answers:
- If they have a URL and a starter library: `review <URL> as <one-of-the-generated-slugs>`
- If they have a library but no URL: `review example.com as <slug>` to see how it works
- If they have no library: `generate 10 personas` first

## Step 6 — Where to read more

Point them at:
- `README.md` — the quick reference
- `CLAUDE.md` — the conductor's full operating manual (what every command does, what the hard rules are, where files live)
- `system/persona-template.md` — the schema every persona file follows
- `system/review-schema.md` — what a review file contains
- `system/report-schema.md` — what an aggregate report contains

End with: "You're set. When you want to actually run a review, just type the command above (or describe it in plain English — I'll figure it out)."

## Hard rules for this skill

- DO NOT skip the environment check — broken Python deps will fail every subsequent run silently.
- DO NOT generate more than 10 personas in parallel. Use batched dispatch for larger counts.
- DO NOT modify existing persona files if any happen to be present — only generate new ones.
- DO NOT promise costs that you can't verify. Use the rough ranges above; tell the user "actual cost depends on which Claude model your CLI is configured for."
- If the user says "I just want to see it work, don't ask me anything" — fall back to: generate 5 personas (random mode), point them at `review example.com with everyone`.
