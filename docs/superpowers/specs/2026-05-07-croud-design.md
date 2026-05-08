---
title: Croud — Persona-Based Website Review System
date: 2026-05-07
status: draft
---

# Croud — Persona-Based Website Review System

## 1. Purpose

Croud is a Claude Code-driven system that simulates a wide range of real human reactions to a website. The user points Claude at a URL, and Claude — embodying one or many richly defined personas — interacts with the site as those personas would, then produces a comprehensive report designed to be consumed by a downstream LLM agent (e.g. the user's business wiki) for design and content optimization.

The system explicitly refuses Claude's own editorial voice. Each review is the persona's reaction. The aggregate report is data and verbatim quotes — no recommendations.

## 2. Goals & non-goals

**Goals**
- Replicate the variance of real human first impressions across age, race, geography, income, tech literacy, device, disposition, and ~30 other dimensions.
- Produce reproducible per-persona reviews and a machine-consumable aggregate report.
- Support iterative growth: build personas in batches of 10–15, accumulate over time, never delete or modify existing personas.
- Run flexibly: single persona, named persona, random sample, tag-filtered subset, full library — with optional N-fresh-runs and sequential return-visit modes.

**Non-goals**
- Replacing real user research. Croud is a fast, broad-stroke proxy.
- Generating Claude's own design opinions. Croud's job is to capture reactions and ship them downstream — interpretation lives elsewhere.
- Rendering or running the website itself. Croud consumes a public URL via headless browsing.

## 3. System overview

```
User (in croud/ with Claude Code)
   │
   ▼
Conductor agent (main Claude session, reads croud/CLAUDE.md)
   │
   ├─ parses plain-English request
   ├─ resolves persona selection (single / random sample / tag filter / full)
   ├─ for each persona × run-multiplier:
   │     dispatches fresh subagent
   │            │
   │            ▼
   │     Persona-review subagent
   │       - loads persona file
   │       - loads system/browsing-protocol.md
   │       - uses /browse skill to capture screenshots + HTML
   │       - navigates the site as the persona naturally would
   │       - writes one structured review (frontmatter + first-person narrative)
   │       - returns to conductor
   │
   ├─ collects all reviews
   ├─ writes per-persona review files
   └─ generates the aggregate report (factual + verbatim only)
```

### Why subagents
- **Fresh memory per run** — Marcus's reaction never bleeds into Priya's. Independent fresh runs of the same persona average correctly because each subagent has zero prior context.
- **Parallelism** — A 50-persona panel completes in roughly the time of one review.
- **Isolation** — System-prompt drift, opinion leakage, and conversation-state contamination are structurally prevented.

### Why plain-English invocation
The user wants frictionless interaction: open Claude Code, talk. CLAUDE.md teaches the conductor a small command vocabulary so common phrasings resolve to deterministic actions.

## 4. Directory layout

```
croud/
├── CLAUDE.md                       # teaches Claude how to operate the system
├── README.md                       # human onboarding
├── docs/
│   └── superpowers/specs/
│       └── 2026-05-07-croud-design.md
├── system/
│   ├── persona-template.md
│   ├── diversity-matrix.md         # axes of variation
│   ├── review-schema.md            # frontmatter + narrative spec
│   ├── report-schema.md            # aggregate report spec
│   └── browsing-protocol.md        # how subagent navigates as persona
├── personas/
│   ├── _index.md                   # machine-readable roster (frontmatter table)
│   ├── marcus-webb.md
│   ├── priya-shah.md
│   └── ...                          # grows over time
├── skills/
│   └── generate-persona.md         # generator skill
└── reviews/
    └── {site-domain}/
        └── {YYYY-MM-DD-HHMM-selector-runtype}/
            ├── report.md
            ├── reviews/
            │   ├── marcus-webb.md
            │   ├── priya-shah.md
            │   └── ...
            └── screenshots/
                └── *.png
```

## 5. Persona schema

Each `personas/<slug>.md` follows a fixed structure. Existing files are immutable once written; the generator only appends new ones.

```yaml
---
slug: marcus-webb
name: Marcus Webb
created: 2026-05-07
age: 47
age_bucket: 40-49
gender: M
race: Black
ethnicity: African American
location: suburban Atlanta, GA
location_type: suburban
income_bracket: middle
education: trade school
profession: HVAC business owner
family_status: married, 2 teens
device_primary: Android phone
device_secondary: shared family laptop
internet_quality: home cable, mobile patchy
tech_literacy: medium
language_primary: English
language_fluency: native
disability: none
patience: low
trust_disposition: skeptical
buying_style: word-of-mouth-first
political_lean: moderate
religious_observance: occasional
typical_mood_online: frustrated, time-poor
reading_style: scanner
attention_span: focused
browsing_context_typical: lunch-break-on-phone
time_of_day_typical: midday
variance_envelope:
  mood_range: [frustrated, time-poor, distracted, briefly-curious, irritated]
  context_range: [lunch-break-on-phone, evening-couch-on-phone, weekend-on-laptop]
  patience_range: [very-low, low, medium]      # within his realistic spectrum
  time_of_day_range: [midday, evening, late-evening]
  device_range: [Android phone, family laptop]
trust_signals_valued: [reviews, founder-face, clear-pricing]
ui_pet_peeves: [autoplay-video, sticky-chat, jargon]
sexual_orientation: straight
gender_identity: cis
immigrant_generation: native
cultural_political_bubble: mainstream
color_vision: standard
reading_literacy: high-school
motor_dexterity: standard
domain_expertise_areas: [HVAC, small-business-ops]
past_online_traumas: [bad-delivery]
brand_sophistication: mid
visual_preference: minimalist
aesthetic_suspicion_threshold: medium
currency_default: USD
measurement_default: imperial
privacy_posture: cautious
risk_tolerance: cautious
tags: [over-40, mobile-first, low-patience, skeptic, blue-collar, business-owner, android, suburban]
---

# Marcus Webb, 47

## Life
[~200 words: career arc, family, daily routine, what frustrates him, what he values, biggest recent purchase, last website that pissed him off, last website he loved and why.]

## Online behavior
[~150 words: typical session length, what catches his eye, what makes him bounce, scroll depth tendency, ad blindness, form fatigue, when he opens new tabs vs commits to one page, mobile vs desktop split.]

## Voice
[~100 words sample of his actual voice — first person — vocabulary, cadence, profanity comfort, whether he hedges or commits.]

## Biases & triggers
[Specific: trusts X, distrusts Y. Bounces on jargon Z. Loves clear pricing. Hates auto-playing video.]

## Browsing protocol
[How this specific persona interacts with a new site — what they look at first, click rules, bounce rules. Drives the subagent's site-navigation behavior.]
```

### Quality rules
- Every section must be filled. No placeholder bios.
- Names must span ethnicity and region authentically.
- Voice samples must be distinct — no two personas should sound the same.
- Bios may contain contradictions (the wealthy tech-illiterate; the careful teen; the power-user retiree). Real people are inconsistent.

## 6. Diversity matrix

`system/diversity-matrix.md` is a reference doc enumerating dimensions to span. The generator consults it to avoid clustering and to fill gaps.

**Demographic / structural**
- Age buckets: 13–17, 18–25, 26–34, 35–49, 50–64, 65–79, 80+
- Race / ethnicity: full spectrum, including mixed
- Geography: urban / suburban / rural × global regions
- Income: poverty, working, middle, upper-middle, wealthy
- Education: none / HS / trade / bachelor / advanced
- Profession: blue-collar, white-collar, creative, retired, student, unemployed, gig, founder, etc.
- Family/household structure: single / partnered / caregiver / kids-ages / multi-gen
- Immigrant/generation status: native / 1st-gen / 2nd-gen / international
- Sexual orientation / gender identity
- Religious observance: none / occasional / devout

**Technical / contextual**
- Tech literacy: novice / casual / power-user / professional
- Device primary: mobile (Android/iOS), desktop, tablet, low-end / high-end
- Internet quality: rural-slow / mobile-only / fiber / satellite
- Browsing context typical: in-bed / lunch-break / at-desk / on-toilet / waiting-room / commuting
- Time of day typical: early-morning / midday / evening / late-night
- Privacy posture: paranoid / cautious / indifferent

**Cognitive / behavioral**
- Reading style: skimmer / scanner / deep-reader / title-only / never-reads
- Reading literacy level: distinct from formal education
- Attention span: ADHD / focused / chronic-multitasker
- Patience: very-low / low / medium / high
- Disposition: trusting / skeptical / anxious / enthusiastic / indifferent
- Typical mood online: bored / rushed / leisurely / pissed-off / curious

**Physical / accessibility**
- Disability: vision / motor / cognitive / none
- Color vision: standard / deuteranopia / protanopia / tritanopia
- Motor/dexterity: standard / tremor / one-handed / accessibility-tools
- Language fluency: native / second-language / ESL-low

**Commercial / experiential**
- Buying style: research-heavy / impulsive / word-of-mouth / never-buys-online
- Risk tolerance: paranoid-CC / freely-buys / BNPL-user
- Brand sophistication: knows-every-brand / mid / brand-naive
- Domain expertise areas: list (drives jargon comprehension at review time)
- Past online traumas: scammed-before / identity-stolen / never-burned / bad-delivery
- Trust signals valued: reviews / press-logos / security-badges / founder-face / known-brand / referrals
- Currency / measurement defaults: USD/EUR/INR/etc; metric/imperial

**Aesthetic**
- Visual preference: minimalist / maximalist / nostalgic / corporate-polished / indie-handmade / brutalist / luxury
- Aesthetic suspicion threshold: when "polished" tips into "fake"
- UI pet peeves: popups / autoplay / sticky-chat / cookie-banners / paywalls / endless-scroll / mandatory-signup

**Cultural / contextual**
- Cultural/political bubble: terminally-online / mainstream / log-off / niche-community

## 7. Review schema

Each per-persona review file lives at `reviews/{site}/{run-id}/reviews/<persona-slug>.md`.

```yaml
---
persona: marcus-webb
site: example.com
run_id: 2026-05-07-1830-random50-fresh
run_type: fresh-1                 # fresh-1, fresh-2... or return-1, return-2...
entry_url: https://example.com/
entry_context: phone, lunch break, frustrated mood
device_used: Android phone
domain_expertise_overlap: low     # low/medium/high vs site topic
session:
  time_on_site_seconds: 14
  pages_visited: ["/"]
  click_path: []
  scroll_depth_max_pct: 35
  bounce_point: hero
  bounce_reason: "AI-generated stock photo + jargon"
scores:
  trust: 2                        # 0-10
  clarity: 4
  intent_to_act: 1
  visual_appeal: 3
  copy_quality: 2
  emotional_response: skeptical   # warm/curious/neutral/skeptical/annoyed/repelled
  would_return: false
  would_recommend: false
elements_noticed:
  - { type: hero_image, sentiment: negative, note: "looks AI-generated, fake smiles" }
  - { type: headline, sentiment: negative, note: "synergistic solutions = jargon" }
elements_ignored:
  - footer
  - testimonials
---

[First-person narrative reaction in the persona's actual voice. ~150-300 words.
What they did, in order. What they noticed. What pissed them off or won them over.
Specific to this visit. No meta-commentary. No third-person summaries.]
```

### Hard rules for the review subagent
- Narrative MUST be first-person, in the persona's voice.
- No external research (no Googling the company, no checking Trustpilot).
- If the persona would not have noticed something, do not list it.
- If the persona is jargon-illiterate, the review must show the confusion.
- Time-on-site must be a realistic estimate based on persona patience and content density.
- Subagent decides when the persona "leaves" — respecting their bounce triggers.

## 8. Report schema

`reviews/{site}/{run-id}/report.md` is the machine-consumable aggregate. It is the artifact the user feeds into a downstream LLM (their business wiki). It contains zero agent opinions or recommendations.

Structure:
1. **Front matter**: site, run_id, timestamp, panel_size, selection criteria, run type, schema_version.
2. **Selection criteria**: how personas were sampled.
3. **Aggregate scores**: mean / median / std / min / max for each numeric metric.
4. **Conversion funnel**: counts at landed / scrolled-past-hero / reached-pricing / reached-CTA / would-return / would-recommend.
5. **Bounce-point distribution**: counts and % per bounce point.
6. **Cuts by dimension**: per-tag breakdowns (age bucket, device, tech literacy, patience, expertise overlap, etc.) with score deltas.
7. **Element-level reactions**: per UI element, counts of positive/negative/neutral plus sample quotes.
8. **Verbatim quote board**: themed, attributed (slug + key demographics).
9. **Pattern flags**: factual observations only ("14/31 mobile-first personas bounced at hero"). No "the hero should be redesigned."
10. **Per-persona index**: links to each `reviews/<slug>.md` with one-line summary.

The report is generated by the conductor after all subagents return. It reads only the per-persona review files and computes everything from them — it does not fabricate stats or quotes.

## 9. Run modes

### Selection modes
| pattern | behavior |
|---------|----------|
| `as <slug>` | single named persona |
| (no selector) | random sample of N (default 50) from current library |
| `with N personas` | random sample of N |
| `with <tag>` | all personas matching tag (intersection if multiple) |
| `with everyone` | full library (cost-gated) |

### Multipliers
| pattern | behavior |
|---------|----------|
| `N fresh runs per persona` | each persona reviewed N times by N independent subagents; outputs averaged in the report |
| `visit again` / `visit N times over <period>` | sequential return runs; subagent receives prior visit log as input so persona "remembers" |

### Cost gate
Before any run that exceeds 50 subagent invocations (e.g. 25 personas × 5 fresh runs), the conductor stops and prompts the user with an estimate. Estimate is computed from a configurable per-subagent average cost stored in CLAUDE.md.

## 10. Run ID convention

`{YYYY-MM-DD-HHMM}-{selector}-{runtype}`

Selector strings:
- `random50`, `random25`, etc.
- `<persona-slug>` for single
- `<tag>-tag` for tag filter
- `everyone` for full library

Runtype strings (folder-level):
- `fresh` (single fresh run per persona)
- `freshN` (N independent fresh runs per persona; e.g. `fresh5`)
- `returnN` for sequenced returns (e.g. `return3`)

The per-review `run_type` field inside each review file disambiguates which-of-N:
- Single fresh run → `fresh-1`
- Three fresh runs → `fresh-1`, `fresh-2`, `fresh-3`
- Three sequential returns → `return-1`, `return-2`, `return-3`

Examples:
- `2026-05-07-1830-random50-fresh`
- `2026-05-07-1830-marcus-webb-fresh5`
- `2026-05-08-0900-marcus-webb-return-2`
- `2026-05-09-1100-mobile-first-tag-fresh`

Run folders are never overwritten. Re-running with the same selector creates a new timestamped folder.

## 11. Browsing protocol

`system/browsing-protocol.md` is loaded by every persona-review subagent. It defines:

- **Moment sampling (first step)**: before opening the URL, the subagent samples one value from each list in the persona's `variance_envelope` (mood, context, patience-on-the-day, time-of-day, device). This becomes the "moment" for this visit and is recorded in the review's `entry_context` and `device_used` fields. Independent fresh runs of the same persona MUST resample independently — that's the source of intra-persona variance.
- **Capture step**: open the URL via the `/browse` skill (gstack), capture hero screenshot, capture full-page or scroll-position screenshots as the persona scrolls, capture rendered HTML/text.
- **Navigation budget**: max 10 clicks per visit, max 5 unique pages, max 3-minute simulated session. Subagent decides when the persona leaves based on their patience and triggers.
- **Click decision rule**: at each step, the subagent asks "would THIS persona click anywhere right now, and where?" The persona's `browsing_protocol` section in their bio drives this.
- **Bounce rule**: respect the persona's bounce triggers — low-patience persona seeing jargon must bounce immediately. The narrative must reflect this honestly.
- **No external research**: the subagent does not Google the company, check Trustpilot, or verify claims off-site.
- **Voice rule**: the narrative is first-person in the persona's voice. No Claude vocabulary.
- **Honesty rule**: if the persona would not have noticed an element, do not score or mention it.
- **Time tracking**: subagent estimates realistic seconds-on-page based on persona patience and content density.

## 12. Generator skill

`croud/skills/generate-persona.md` is invoked by the conductor when the user asks for new personas.

### Modes
- **random** — picks a coherent persona's worth of dimension values from the matrix, biased toward unfilled cells in `_index.md`.
- **tag-spec** — user provides constraints (e.g. "rural, over-60, low-tech, religious"); generator fills the remaining axes.
- **fill-gaps** — generator reads `_index.md`, computes coverage per matrix axis, generates personas to fill underrepresented cells.
- **batch** — generates 10–15 personas in one invocation (the user's preferred working cadence).

### Quality rules baked into the skill
- Each persona must include all sections of the template.
- Names span ethnicity and region authentically — no defaulting to a single demographic pattern.
- Voice section must read distinctly across personas.
- No tropes. Bio details should feel observed, not assumed.
- Bios may contain real-life contradictions.

### Output behavior
- Writes a new `personas/<slug>.md` per generated persona.
- Updates `personas/_index.md` (machine-readable frontmatter table) with slug + key dimensions + tags + creation date.
- Never modifies existing persona files.
- Never deletes anything.

## 13. CLAUDE.md (teaching file at croud root)

Sections:
1. **What this system does** — one paragraph.
2. **How invocation works** — the plain-English patterns mapped to actions.
3. **Hard rules**:
   - Never delete personas.
   - Never modify existing persona bios.
   - Never overwrite review folders.
   - Never inject Claude opinions into reviews or reports.
   - Always dispatch a fresh subagent per persona run.
   - Always capture screenshots before reviewing.
4. **Cost discipline** — when to ask before running.
5. **Index of system files** — pointers to schemas, matrix, protocol.
6. **How to add personas** — point to the generator skill.
7. **How the report is built** — point to `report-schema.md`.

## 14. Persistence, immutability, and reaction variance

The system distinguishes the **persona file** (frozen) from the **persona's reaction on a given visit** (varied).

### Persona file — frozen
- Written once. Never modified. Never deleted.
- The generator is append-only.
- Marcus's bio, voice, biases, expertise, and structural traits next month are byte-identical to today's.
- This guarantees reproducibility: an old run can be re-explained later, and reruns reflect *visit-level* variance, not bio drift.

### Persona reaction — varied within character
A real person doesn't react identically on Tuesday morning and Saturday night. The bio captures the **person**, not the **moment**. Each visit pulls a moment from the persona's `variance_envelope`:

- **Mood on arrival** — sampled from `mood_range` (e.g. Marcus is usually frustrated, occasionally briefly-curious).
- **Browsing context** — sampled from `context_range` (lunch-break vs evening couch vs weekend laptop).
- **Patience on the day** — sampled from `patience_range`. Same persona, fractionally more or less tolerant today.
- **Time of day** — sampled from `time_of_day_range`.
- **Device** — sampled from `device_range` (mobile vs desktop within their habits).
- **LLM sampling stochasticity** — even with identical inputs, two fresh subagents produce different narrations. This is desired, not a bug.

The selected moment is recorded in the review's `entry_context` and `device_used` fields, so any single review is fully traceable.

This is what makes "5 fresh runs of marcus-webb" valuable: 5 different visits by the same person, not 5 photocopies. The aggregate report then captures Marcus's *distribution* of reactions, not a single point estimate.

### Run folders — frozen
- Review run folders are never overwritten. Each run gets a unique timestamped folder.
- A site can accumulate hundreds of run folders over time, enabling diff-style comparisons (out of scope for v1, supported by the schema).

### Library — grows indefinitely
The user expects to build personas in batches of 10–15 over time and accumulate hundreds.

## 15. Open questions / future work

These are intentionally out of scope for the first build but worth flagging:

- **Diff reports across run-ids** — comparing reviews of the same site over time (after a redesign). The schema supports it; the diff generator is a follow-on.
- **Persona aging** — eventually, real people change. We may want a sibling-persona mechanism (e.g. `marcus-webb-2027`) rather than mutating bios.
- **Cross-site personas** — a persona's expertise overlap is computed per-site; should we cache those computations per (persona, site) pair?
- **Cost-per-run telemetry** — tracking actual cost over time to refine the cost-gate estimator.
- **Localization** — reviews in non-English voices for non-English personas. The voice rule already supports this; tooling support (e.g. ensuring the subagent produces non-English narrative) is a future concern.

## 16. Build sequence (high-level, to be expanded by writing-plans)

1. Repository scaffold: directory structure, README.md, CLAUDE.md skeleton.
2. System files: persona-template.md, diversity-matrix.md, review-schema.md, report-schema.md, browsing-protocol.md.
3. Persona generator skill: skills/generate-persona.md.
4. Conductor instructions in CLAUDE.md: invocation patterns, dispatch rules, cost gate.
5. First batch: generate 10–15 seed personas via the skill.
6. First review run: single named persona on a known site, validate end-to-end.
7. Panel run: random-25 on a known site, validate report aggregation.
8. Multi-fresh + return-visit modes.

## 17. Success criteria

- A user can sit down in `croud/`, open Claude Code, and run their first review on a real website with one plain-English sentence.
- The persona library grows in batches of 10–15 without manual file editing.
- Two independent fresh runs of the same persona on the same site produce visibly different but persona-consistent narratives (variance within character).
- The generated report is comprehensive enough that a downstream LLM agent (the user's business wiki) can act on it without needing the per-persona files — though those remain the source of truth.
- No review or report contains Claude's editorial voice. Every reaction is the persona's; every aggregate stat is computed.
