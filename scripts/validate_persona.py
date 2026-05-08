"""Validator for persona files. Run as a script or import validate_persona()."""
from __future__ import annotations

import sys
from pathlib import Path
import frontmatter


class ValidationError(Exception):
    pass


REQUIRED_KEYS = [
    "slug", "name", "created", "age", "age_bucket", "gender", "race",
    "ethnicity", "location", "location_type", "income_bracket", "education",
    "profession", "family_status", "device_primary", "device_secondary",
    "internet_quality", "tech_literacy", "language_primary", "language_fluency",
    "disability", "patience", "trust_disposition", "buying_style",
    "political_lean", "religious_observance", "typical_mood_online",
    "reading_style", "attention_span", "browsing_context_typical",
    "time_of_day_typical", "trust_signals_valued", "ui_pet_peeves",
    "sexual_orientation", "gender_identity", "immigrant_generation",
    "cultural_political_bubble", "color_vision", "reading_literacy",
    "motor_dexterity", "domain_expertise_areas", "past_online_traumas",
    "brand_sophistication", "visual_preference", "aesthetic_suspicion_threshold",
    "currency_default", "measurement_default", "privacy_posture", "risk_tolerance",
    "variance_envelope", "tags",
]

ENUMS = {
    "age_bucket": {"13-17", "18-25", "26-34", "35-49", "50-64", "65-79", "80+"},
    "location_type": {"urban", "suburban", "rural"},
    "income_bracket": {"poverty", "working", "middle", "upper-middle", "wealthy"},
    "education": {"none", "HS", "trade", "bachelor", "advanced"},
    "tech_literacy": {"novice", "casual", "power-user", "professional"},
    "patience": {"very-low", "low", "medium", "high"},
    "trust_disposition": {"trusting", "skeptical", "anxious", "enthusiastic", "indifferent"},
    "buying_style": {"research-heavy", "impulsive", "word-of-mouth-first", "never-buys-online"},
    "religious_observance": {"none", "occasional", "devout"},
    "reading_style": {"skimmer", "scanner", "deep-reader", "title-only", "never-reads"},
    "attention_span": {"ADHD", "focused", "chronic-multitasker"},
    "time_of_day_typical": {"early-morning", "midday", "evening", "late-night"},
    "immigrant_generation": {"native", "1st-gen", "2nd-gen", "international"},
    "cultural_political_bubble": {"terminally-online", "mainstream", "log-off", "niche-community"},
    "color_vision": {"standard", "deuteranopia", "protanopia", "tritanopia"},
    "reading_literacy": {"below-HS", "high-school", "college", "advanced"},
    "motor_dexterity": {"standard", "tremor", "one-handed", "accessibility-tools"},
    "brand_sophistication": {"brand-naive", "mid", "knows-every-brand"},
    "visual_preference": {"minimalist", "maximalist", "nostalgic", "corporate-polished",
                          "indie-handmade", "brutalist", "luxury"},
    "aesthetic_suspicion_threshold": {"low", "medium", "high"},
    "measurement_default": {"metric", "imperial"},
    "privacy_posture": {"paranoid", "cautious", "indifferent"},
    "risk_tolerance": {"paranoid-CC", "cautious", "freely-buys", "BNPL-user"},
}

VARIANCE_ENVELOPE_KEYS = [
    "mood_range", "context_range", "patience_range",
    "time_of_day_range", "device_range",
]

REQUIRED_BODY_SECTIONS = [
    "## Life",
    "## Online behavior",
    "## Voice",
    "## Biases & triggers",
    "## Browsing protocol",
]

PLACEHOLDER_PATTERNS = ["[TBD]", "[fill in]", "[placeholder]", "TODO:", "...]"]


def validate_persona(path: Path) -> None:
    """Raise ValidationError if the file at path is not a valid persona."""
    text = path.read_text()
    try:
        post = frontmatter.loads(text)
    except Exception as e:
        raise ValidationError(f"frontmatter parse error: {e}")

    fm = post.metadata
    body = post.content

    for key in REQUIRED_KEYS:
        if key not in fm:
            raise ValidationError(f"missing required key: {key}")

    for key, allowed in ENUMS.items():
        if key in fm and fm[key] not in allowed:
            raise ValidationError(
                f"{key} value {fm[key]!r} not in allowed set {sorted(allowed)}"
            )

    ve = fm.get("variance_envelope")
    if not isinstance(ve, dict):
        raise ValidationError("variance_envelope must be a mapping")
    for vk in VARIANCE_ENVELOPE_KEYS:
        if vk not in ve:
            raise ValidationError(f"variance_envelope missing required key: {vk}")
        val = ve[vk]
        if not isinstance(val, list):
            raise ValidationError(f"variance_envelope.{vk} must be a list")
        if len(val) == 0:
            raise ValidationError(f"variance_envelope.{vk} must not be empty")

    for section in REQUIRED_BODY_SECTIONS:
        if section not in body:
            raise ValidationError(f"missing body section: {section}")

    sections = _split_sections(body)
    for section_name, section_body in sections.items():
        for placeholder in PLACEHOLDER_PATTERNS:
            if placeholder in section_body:
                raise ValidationError(
                    f"placeholder {placeholder!r} found in section: {section_name}"
                )
        if section_body.strip() == "":
            raise ValidationError(f"empty body section: {section_name}")


def _split_sections(body: str) -> dict[str, str]:
    """Split markdown body by ## headers into {header: content}."""
    sections = {}
    current_header = None
    current_lines: list[str] = []
    for line in body.splitlines():
        if line.startswith("## "):
            if current_header is not None:
                sections[current_header] = "\n".join(current_lines).strip()
            current_header = line.strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_header is not None:
        sections[current_header] = "\n".join(current_lines).strip()
    return sections


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: validate_persona.py <path-to-persona.md> [more paths...]")
        return 2
    failures = 0
    for arg in sys.argv[1:]:
        path = Path(arg)
        if path.name.startswith("_"):
            print(f"SKIP: {path} (meta file)")
            continue
        try:
            validate_persona(path)
            print(f"OK: {path}")
        except ValidationError as e:
            print(f"FAIL: {path}: {e}")
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
