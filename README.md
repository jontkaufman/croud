# Croud

A persona-based website review system, driven by Claude Code or OpenAI Codex CLI.

You point Claude at a URL. Claude — embodying one or many richly defined personas — reacts to the site as those people would, then produces a structured report. Every reaction is the persona's; every aggregate stat is computed. The output is designed to be fed to another LLM (your team wiki, a design tool, a content strategist) for site optimization.

> **Worth knowing**: a "review" is many small Claude calls in parallel (one per persona). Costs scale with panel size. Start small.

---

## Table of contents

1. [What you'll need](#1-what-youll-need)
2. [Get the code](#2-get-the-code)
3. [Open the folder in Claude or Codex](#3-open-the-folder-in-claude-or-codex)
4. [Run setup](#4-run-setup)
5. [Run your first review](#5-run-your-first-review)
6. [What's where](#whats-where)
7. [Hard rules](#hard-rules)
8. [License](#license)

---

## 1. What you'll need

If any of these are unfamiliar, the linked install pages walk through every step. **Do these in order.** You only do them once.

### Python (3.9 or newer)

Croud uses small Python scripts to validate persona and review files.

- **macOS / Linux**: open Terminal, type `python3 --version`. If you see `3.9` or higher, you're done. Otherwise install from [python.org/downloads](https://www.python.org/downloads/).
- **Windows**: install from [python.org/downloads](https://www.python.org/downloads/) and **make sure you tick "Add Python to PATH"** during install.

### Claude Code OR OpenAI Codex CLI

Croud is designed to run inside one of these two CLIs. They both speak the same skill format, so either works.

- **Claude Code** (recommended): install instructions at [docs.claude.com/en/docs/claude-code/quickstart](https://docs.claude.com/en/docs/claude-code/quickstart). You'll need an Anthropic account.
- **OpenAI Codex CLI**: install instructions at [github.com/openai/codex](https://github.com/openai/codex). You'll need an OpenAI account.

Pick one. The rest of this README assumes Claude Code, but every command works identically in Codex.

### A terminal

- **macOS**: open the **Terminal** app (in `/Applications/Utilities/`).
- **Windows**: open **PowerShell** or **Windows Terminal**.
- **Linux**: you already know.

---

## 2. Get the code

Two paths. Pick whichever feels easier.

### Path A — Download a ZIP (no Git knowledge required)

1. Go to this repo's GitHub page in your browser.
2. Click the green **Code** button near the top right.
3. Click **Download ZIP**.
4. Find the downloaded file (probably in `Downloads/`). Double-click it to unzip.
5. You'll get a folder called `croud-main` (or similar). Move it wherever you want it to live — Desktop, Documents, anywhere.

### Path B — Clone with Git (if you already use Git)

```bash
git clone https://github.com/<your-fork-or-the-original>/croud.git
cd croud
```

---

## 3. Open the folder in Claude or Codex

In your terminal, change directory into the folder you just downloaded or cloned. For example, if it's on your Desktop:

**macOS / Linux:**
```bash
cd ~/Desktop/croud-main
```

**Windows:**
```powershell
cd $HOME\Desktop\croud-main
```

Then start Claude Code (or Codex):

```bash
claude
```

(For Codex, use the Codex CLI command instead.)

You should see Claude greet you and recognize that you're inside a project (it'll auto-load `CLAUDE.md`).

---

## 4. Run setup

In the Claude Code chat, type:

```
/setup
```

(Or just say: `help me get started`.)

Claude will:

1. Check your Python environment and install dependencies if missing.
2. Ask you ~5 short questions: what you want to review, who your target audience is, how many personas to generate, etc.
3. Generate a starter persona library tailored to your audience.
4. Hand you the exact command for your first review.

The whole thing takes about 2-5 minutes depending on how many personas you generate.

---

## 5. Run your first review

After setup, you can talk to Claude in plain English. Examples:

| What you say | What happens |
|---|---|
| `review example.com as <persona-slug>` | Single persona reviews the site. Cheapest, fastest. |
| `review example.com with 5 personas` | Random sample of 5 personas. |
| `review example.com with everyone` | Full library reviews. (Asks to confirm cost first.) |
| `review example.com with <tag>` | Filter by tag (e.g. `mobile-first` or `over-50`). |
| `generate 10 personas — <description>` | Add more personas to your library later. |
| `list personas tagged <tag>` | Roster query. |
| `show last review of example.com` | Reload the most recent run. |

Claude reads `CLAUDE.md` (the conductor instructions) and translates your phrasing into the right action.

After a review, you'll find:

```
reviews/example.com/<run-id>/
├── reviews/<persona-slug>.md      ← one file per persona
├── screenshots/                    ← captured pages
└── report.md                       ← aggregate analysis
```

The `report.md` is the artifact you feed to other tools — your team wiki, a designer, a content strategist, or another LLM agent for follow-up.

---

## What's where

- `CLAUDE.md` — full conductor instructions (Claude reads this on every session).
- `system/` — schemas, templates, and the browsing protocol.
- `personas/` — your persona library (grows over time; starts empty).
- `skills/` — agent skills (`setup`, `generate-persona`).
- `reviews/` — every review run, timestamped, never overwritten.
- `scripts/` — schema validators (Python).
- `tests/` — validator test coverage.
- `docs/` — design spec and longer-form docs.

---

## Hard rules

These are baked into how Croud works. They're documented in `CLAUDE.md` for the agent and listed here for you:

- **Persona files are never deleted or modified once written.** A persona is a fixed reference point. Re-running a review with the same persona must produce a comparable result. If you want a different persona, generate a new one — don't mutate an existing file.
- **Review run folders are never overwritten.** Every run gets its own timestamped folder. If you want to compare today vs. last week, both runs are still on disk.
- **Reviews and reports never contain Claude's editorial voice.** Only persona reactions (in the persona's voice) and computed stats (mean, median, counts). Recommendations are your job — or the next LLM in your pipeline.
- **The conductor never reviews.** A separate fresh subagent runs each persona's review, so context never leaks between personas.

---

## Costs (roughly)

Each persona-review is one Claude call with web browsing. Rough ranges per panel size, depending on which Claude model your CLI is configured for and the complexity of the site:

| Panel size | Approximate cost |
|---|---|
| 1 persona | $0.05 – $0.30 |
| 5 personas | $0.50 – $2 |
| 10 personas | $1 – $4 |
| 25 personas | $3 – $10 |
| 50 personas | $6 – $20 |

Numbers vary widely based on model choice, screenshot count, and how deep each persona navigates. Claude will warn before any run that exceeds 50 subagents.

---

## Contributing

Contributions welcome. The validators in `scripts/` are TDD-covered — keep them green.

```bash
.venv/bin/pytest tests/
```

---

## License

MIT. See [LICENSE](./LICENSE).
