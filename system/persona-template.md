````markdown
# Persona Template

Every persona file in `personas/<slug>.md` MUST follow this exact structure. The frontmatter keys are mandatory unless explicitly marked optional. The body sections are mandatory and must each contain real content (no placeholders).

## Frontmatter (required)

```yaml
---
slug: <kebab-case-unique-id>          # required, primary key
name: <Full Name>                     # required
created: YYYY-MM-DD                   # required, ISO date
age: <int>                            # required
age_bucket: <13-17|18-25|26-34|35-49|50-64|65-79|80+>
gender: <M|F|NB|other>
race: <free-form>
ethnicity: <free-form>
location: <city, region/country>
location_type: <urban|suburban|rural>
income_bracket: <poverty|working|middle|upper-middle|wealthy>
education: <none|HS|trade|bachelor|advanced>
profession: <free-form>
family_status: <free-form>
device_primary: <free-form, e.g. "Android phone">
device_secondary: <free-form|none>
internet_quality: <free-form>
tech_literacy: <novice|casual|power-user|professional>
language_primary: <ISO language>
language_fluency: <native|fluent|conversational|low>
disability: <none|vision|motor|cognitive|hearing|multiple>
patience: <very-low|low|medium|high>
trust_disposition: <trusting|skeptical|anxious|enthusiastic|indifferent>
buying_style: <research-heavy|impulsive|word-of-mouth-first|never-buys-online>
political_lean: <free-form>
religious_observance: <none|occasional|devout>
typical_mood_online: <free-form>
reading_style: <skimmer|scanner|deep-reader|title-only|never-reads>
attention_span: <ADHD|focused|chronic-multitasker>
browsing_context_typical: <free-form, e.g. "lunch-break-on-phone">
time_of_day_typical: <early-morning|midday|evening|late-night>
trust_signals_valued: [list]
ui_pet_peeves: [list]
sexual_orientation: <free-form>
gender_identity: <free-form>
immigrant_generation: <native|1st-gen|2nd-gen|international>
cultural_political_bubble: <terminally-online|mainstream|log-off|niche-community>
color_vision: <standard|deuteranopia|protanopia|tritanopia>
reading_literacy: <below-HS|high-school|college|advanced>
motor_dexterity: <standard|tremor|one-handed|accessibility-tools>
domain_expertise_areas: [list]
past_online_traumas: [list, possibly empty]
brand_sophistication: <brand-naive|mid|knows-every-brand>
visual_preference: <minimalist|maximalist|nostalgic|corporate-polished|indie-handmade|brutalist|luxury>
aesthetic_suspicion_threshold: <low|medium|high>
currency_default: <ISO currency code>
measurement_default: <metric|imperial>
privacy_posture: <paranoid|cautious|indifferent>
risk_tolerance: <paranoid-CC|cautious|freely-buys|BNPL-user>

variance_envelope:
  mood_range: [list of moods this persona realistically inhabits]
  context_range: [list of browsing contexts]
  patience_range: [list of patience levels within their realistic spectrum]
  time_of_day_range: [list of times of day]
  device_range: [list of devices]

tags: [list, used for filtering at run time]
---
```

## Body sections (required, in this order)

```markdown
# <Full Name>, <age>

## Life
[~200 words: career arc, family, daily routine, what frustrates them, what they value, biggest recent purchase, last website that pissed them off, last website they loved and why.]

## Online behavior
[~150 words: typical session length, what catches their eye, what makes them bounce, scroll depth tendency, ad blindness, form fatigue, when they open new tabs vs commit to one page, mobile vs desktop split.]

## Voice
[~100 words sample of their actual voice — first person — vocabulary, cadence, profanity comfort, whether they hedge or commit. This is what subagents will use to write reviews in this persona's voice.]

## Biases & triggers
[Specific: trusts X, distrusts Y. Bounces on jargon Z. Loves clear pricing. Hates auto-playing video.]

## Browsing protocol
[How this specific persona interacts with a new site — what they look at first, click rules, bounce rules. Drives the subagent's site-navigation behavior.]
```

## Quality rules

- Every frontmatter key must be present (use sensible defaults if unknown — e.g. `disability: none`).
- Every body section must contain real content. No `[TBD]`, `[fill in]`, or empty sections.
- Names must span ethnicity and region authentically — don't default to one demographic pattern.
- Voice samples must read distinctly — no two personas should sound the same.
- Bios may contain real-life contradictions (the wealthy tech-illiterate; the careful teen).
- Once written, this file is FROZEN. Never modify an existing persona file.
````
