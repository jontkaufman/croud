import pytest
from pathlib import Path
from scripts.validate_persona import validate_persona, ValidationError


def write_persona(tmp_path: Path, frontmatter: dict, body: str) -> Path:
    """Helper: write a persona file with the given frontmatter and body."""
    import yaml
    content = "---\n" + yaml.safe_dump(frontmatter, sort_keys=False) + "---\n" + body
    p = tmp_path / "test-persona.md"
    p.write_text(content)
    return p


REQUIRED_KEYS_MINIMAL = {
    "slug": "test-persona",
    "name": "Test Person",
    "created": "2026-05-07",
    "age": 30,
    "age_bucket": "26-34",
    "gender": "F",
    "race": "White",
    "ethnicity": "American",
    "location": "Portland, OR",
    "location_type": "urban",
    "income_bracket": "middle",
    "education": "bachelor",
    "profession": "software engineer",
    "family_status": "single",
    "device_primary": "MacBook Pro",
    "device_secondary": "iPhone",
    "internet_quality": "fiber",
    "tech_literacy": "professional",
    "language_primary": "en",
    "language_fluency": "native",
    "disability": "none",
    "patience": "medium",
    "trust_disposition": "skeptical",
    "buying_style": "research-heavy",
    "political_lean": "left",
    "religious_observance": "none",
    "typical_mood_online": "curious",
    "reading_style": "scanner",
    "attention_span": "focused",
    "browsing_context_typical": "at-desk",
    "time_of_day_typical": "evening",
    "trust_signals_valued": ["reviews"],
    "ui_pet_peeves": ["popups"],
    "sexual_orientation": "straight",
    "gender_identity": "cis",
    "immigrant_generation": "native",
    "cultural_political_bubble": "mainstream",
    "color_vision": "standard",
    "reading_literacy": "advanced",
    "motor_dexterity": "standard",
    "domain_expertise_areas": ["software"],
    "past_online_traumas": [],
    "brand_sophistication": "mid",
    "visual_preference": "minimalist",
    "aesthetic_suspicion_threshold": "medium",
    "currency_default": "USD",
    "measurement_default": "imperial",
    "privacy_posture": "cautious",
    "risk_tolerance": "cautious",
    "variance_envelope": {
        "mood_range": ["curious", "tired"],
        "context_range": ["at-desk", "evening-couch-on-phone"],
        "patience_range": ["low", "medium"],
        "time_of_day_range": ["midday", "evening"],
        "device_range": ["MacBook Pro", "iPhone"],
    },
    "tags": ["tech-savvy"],
}

VALID_BODY = """# Test Person, 30

## Life
She works as a software engineer in Portland. She reads a lot, runs a lot, and is suspicious of marketing copy that uses the word "innovative."

## Online behavior
She skims headlines, opens tabs aggressively, and rarely fills out forms.

## Voice
"Yeah, I'd probably check the docs first. If the docs are bad, I bounce."

## Biases & triggers
Trusts: open-source projects, GitHub stars. Distrusts: 'enterprise' branding.

## Browsing protocol
Reads the hero, scrolls once, looks for a 'docs' or 'pricing' link.
"""


def test_valid_persona_passes(tmp_path):
    p = write_persona(tmp_path, REQUIRED_KEYS_MINIMAL, VALID_BODY)
    validate_persona(p)  # should not raise


def test_missing_required_key_fails(tmp_path):
    fm = dict(REQUIRED_KEYS_MINIMAL)
    del fm["slug"]
    p = write_persona(tmp_path, fm, VALID_BODY)
    with pytest.raises(ValidationError, match="missing required key.*slug"):
        validate_persona(p)


def test_missing_body_section_fails(tmp_path):
    body = VALID_BODY.replace("## Voice\n", "")
    p = write_persona(tmp_path, REQUIRED_KEYS_MINIMAL, body)
    with pytest.raises(ValidationError, match="missing body section.*Voice"):
        validate_persona(p)


def test_placeholder_in_body_section_fails(tmp_path):
    body = VALID_BODY.replace(
        '## Voice\n"Yeah, I\'d probably check the docs first. If the docs are bad, I bounce."',
        "## Voice\n[TBD]",
    )
    p = write_persona(tmp_path, REQUIRED_KEYS_MINIMAL, body)
    with pytest.raises(ValidationError, match="placeholder.*Voice"):
        validate_persona(p)


def test_empty_body_section_fails(tmp_path):
    body = VALID_BODY.replace(
        '## Voice\n"Yeah, I\'d probably check the docs first. If the docs are bad, I bounce."\n',
        "## Voice\n",
    )
    p = write_persona(tmp_path, REQUIRED_KEYS_MINIMAL, body)
    with pytest.raises(ValidationError, match="empty body section.*Voice"):
        validate_persona(p)


def test_invalid_frontmatter_fails(tmp_path):
    p = tmp_path / "broken.md"
    p.write_text("---\nnot: valid: yaml: :::\n---\nbody")
    with pytest.raises(ValidationError, match="frontmatter parse error"):
        validate_persona(p)


def test_invalid_age_bucket_fails(tmp_path):
    fm = dict(REQUIRED_KEYS_MINIMAL)
    fm["age_bucket"] = "999"
    p = write_persona(tmp_path, fm, VALID_BODY)
    with pytest.raises(ValidationError, match="age_bucket"):
        validate_persona(p)


def test_variance_envelope_missing_key_fails(tmp_path):
    fm = dict(REQUIRED_KEYS_MINIMAL)
    fm["variance_envelope"] = {
        "mood_range": ["curious"],
        # missing context_range, patience_range, time_of_day_range, device_range
    }
    p = write_persona(tmp_path, fm, VALID_BODY)
    with pytest.raises(ValidationError, match="variance_envelope.*missing"):
        validate_persona(p)


def test_variance_envelope_empty_list_fails(tmp_path):
    fm = dict(REQUIRED_KEYS_MINIMAL)
    fm["variance_envelope"] = {**REQUIRED_KEYS_MINIMAL["variance_envelope"], "mood_range": []}
    p = write_persona(tmp_path, fm, VALID_BODY)
    with pytest.raises(ValidationError, match="mood_range.*empty"):
        validate_persona(p)


def test_main_skips_underscore_files(tmp_path, monkeypatch, capsys):
    """main() should skip files whose basename starts with underscore (meta files)."""
    import scripts.validate_persona as vp

    meta = tmp_path / "_index.md"
    meta.write_text("anything goes here, won't be validated")

    monkeypatch.setattr(vp.sys, "argv", ["validate_persona.py", str(meta)])
    rc = vp.main()
    out = capsys.readouterr().out
    assert rc == 0
    assert f"SKIP: {meta}" in out
    assert "FAIL" not in out
