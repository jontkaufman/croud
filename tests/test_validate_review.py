import pytest
import yaml
from pathlib import Path

from scripts.validate_review import validate_review, ValidationError


VALID_FRONTMATTER = {
    "persona": "marcus-webb",
    "site": "example.com",
    "run_id": "2026-05-07-1830-marcus-webb-fresh",
    "run_type": "fresh-1",
    "entry_url": "https://example.com/",
    "entry_context": "phone, lunch break, frustrated mood",
    "device_used": "Android phone",
    "domain_expertise_overlap": "low",
    "session": {
        "time_on_site_seconds": 14,
        "pages_visited": ["/"],
        "click_path": [],
        "scroll_depth_max_pct": 35,
        "bounce_point": "hero",
        "bounce_reason": "AI-generated stock photo",
    },
    "scores": {
        "trust": 2,
        "clarity": 4,
        "intent_to_act": 1,
        "visual_appeal": 3,
        "copy_quality": 2,
        "emotional_response": "skeptical",
        "would_return": False,
        "would_recommend": False,
    },
    "elements_noticed": [
        {"type": "hero_image", "sentiment": "negative", "note": "AI-generated"},
    ],
    "elements_ignored": ["footer"],
}

VALID_BODY = "Opened it on my phone during lunch. Hero photo looks fake. Closed the tab."


def write_review(tmp_path: Path, frontmatter: dict, body: str) -> Path:
    content = "---\n" + yaml.safe_dump(frontmatter, sort_keys=False) + "---\n" + body
    p = tmp_path / "marcus-webb.md"
    p.write_text(content)
    return p


def test_valid_review_passes(tmp_path):
    p = write_review(tmp_path, VALID_FRONTMATTER, VALID_BODY)
    validate_review(p)


def test_missing_persona_fails(tmp_path):
    fm = dict(VALID_FRONTMATTER)
    del fm["persona"]
    p = write_review(tmp_path, fm, VALID_BODY)
    with pytest.raises(ValidationError, match="missing required key.*persona"):
        validate_review(p)


def test_score_out_of_range_fails(tmp_path):
    fm = {**VALID_FRONTMATTER, "scores": {**VALID_FRONTMATTER["scores"], "trust": 11}}
    p = write_review(tmp_path, fm, VALID_BODY)
    with pytest.raises(ValidationError, match="trust.*0-10"):
        validate_review(p)


def test_invalid_run_type_fails(tmp_path):
    fm = {**VALID_FRONTMATTER, "run_type": "wat"}
    p = write_review(tmp_path, fm, VALID_BODY)
    with pytest.raises(ValidationError, match="run_type"):
        validate_review(p)


def test_invalid_emotional_response_fails(tmp_path):
    fm = {**VALID_FRONTMATTER, "scores": {**VALID_FRONTMATTER["scores"], "emotional_response": "vibey"}}
    p = write_review(tmp_path, fm, VALID_BODY)
    with pytest.raises(ValidationError, match="emotional_response"):
        validate_review(p)


def test_empty_body_fails(tmp_path):
    p = write_review(tmp_path, VALID_FRONTMATTER, "   ")
    with pytest.raises(ValidationError, match="narrative.*empty"):
        validate_review(p)


def test_non_bool_would_return_fails(tmp_path):
    fm = {**VALID_FRONTMATTER, "scores": {**VALID_FRONTMATTER["scores"], "would_return": "maybe"}}
    p = write_review(tmp_path, fm, VALID_BODY)
    with pytest.raises(ValidationError, match="would_return.*bool"):
        validate_review(p)


def test_bool_score_fails(tmp_path):
    fm = {**VALID_FRONTMATTER, "scores": {**VALID_FRONTMATTER["scores"], "trust": True}}
    p = write_review(tmp_path, fm, VALID_BODY)
    with pytest.raises(ValidationError, match="trust.*0-10"):
        validate_review(p)


def test_invalid_frontmatter_fails(tmp_path):
    p = tmp_path / "broken.md"
    p.write_text("---\nnot: valid: yaml: :::\n---\nbody")
    with pytest.raises(ValidationError, match="frontmatter parse error"):
        validate_review(p)
