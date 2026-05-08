````markdown
# Review Schema

Every per-persona review file at `reviews/{site}/{run-id}/reviews/<persona-slug>.md` MUST conform to this schema.

## Frontmatter (required)

```yaml
---
persona: <persona-slug>                # must match a file in personas/
site: <site-domain>
run_id: <YYYY-MM-DD-HHMM-selector-runtype>
run_type: <fresh-N | return-N>          # N is 1-indexed within the run
entry_url: <URL>
entry_context: <free-form, e.g. "phone, lunch break, frustrated mood">
device_used: <one of persona.variance_envelope.device_range>
domain_expertise_overlap: <low|medium|high>
session:
  time_on_site_seconds: <int>
  pages_visited: [<URL>, ...]
  click_path: [<element/URL>, ...]
  scroll_depth_max_pct: <int 0-100>
  bounce_point: <free-form>
  bounce_reason: <free-form>
scores:
  trust: <int 0-10>
  clarity: <int 0-10>
  intent_to_act: <int 0-10>
  visual_appeal: <int 0-10>
  copy_quality: <int 0-10>
  emotional_response: <warm|curious|neutral|skeptical|annoyed|repelled>
  would_return: <bool>
  would_recommend: <bool>
elements_noticed:
  - { type: <e.g. hero_image>, sentiment: <positive|negative|neutral>, note: <free-form> }
elements_ignored: [list of element types]
---
```

## Body (required)

A first-person narrative reaction in the persona's voice. Length: 150–300 words.

What the persona did, in order. What they noticed. What pissed them off or won them over. Specific to this visit. No meta-commentary. No third-person summaries.

## Hard rules for the review subagent

- Narrative MUST be first-person, in the persona's voice.
- No external research (no Googling the company, no checking Trustpilot).
- If the persona would not have noticed an element, do not list it in `elements_noticed`.
- If the persona is jargon-illiterate, the review must show that confusion.
- `time_on_site_seconds` must be a realistic estimate based on persona patience and content density.
- The subagent decides when the persona "leaves" — respect their bounce triggers.
- All scores must be integers 0–10. `would_return` and `would_recommend` must be booleans.
- The narrative must NEVER contain Claude's editorial voice (no "the site could be improved by…").
````
