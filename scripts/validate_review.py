"""Validator for review files."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import frontmatter


class ValidationError(Exception):
    pass


REQUIRED_TOP = [
    "persona", "site", "run_id", "run_type", "entry_url", "entry_context",
    "device_used", "domain_expertise_overlap", "session", "scores",
    "elements_noticed", "elements_ignored",
]

REQUIRED_SESSION = [
    "time_on_site_seconds", "pages_visited", "click_path",
    "scroll_depth_max_pct", "bounce_point", "bounce_reason",
]

REQUIRED_SCORES_NUMERIC = ["trust", "clarity", "intent_to_act", "visual_appeal", "copy_quality"]
REQUIRED_SCORES_OTHER = ["emotional_response", "would_return", "would_recommend"]

EMOTIONAL_RESPONSES = {"warm", "curious", "neutral", "skeptical", "annoyed", "repelled"}
EXPERTISE_OVERLAPS = {"low", "medium", "high"}
RUN_TYPE_RE = re.compile(r"^(fresh|return)-\d+$")


def validate_review(path: Path) -> None:
    """Raise ValidationError if the file at path is not a valid review."""
    text = path.read_text()
    try:
        post = frontmatter.loads(text)
    except Exception as e:
        raise ValidationError(f"frontmatter parse error: {e}")

    fm = post.metadata
    body = post.content

    for key in REQUIRED_TOP:
        if key not in fm:
            raise ValidationError(f"missing required key: {key}")

    if not RUN_TYPE_RE.match(str(fm["run_type"])):
        raise ValidationError(f"run_type must match fresh-N or return-N, got {fm['run_type']!r}")

    if fm["domain_expertise_overlap"] not in EXPERTISE_OVERLAPS:
        raise ValidationError(
            f"domain_expertise_overlap must be one of {sorted(EXPERTISE_OVERLAPS)}"
        )

    session = fm["session"]
    if not isinstance(session, dict):
        raise ValidationError("session must be a mapping")
    for key in REQUIRED_SESSION:
        if key not in session:
            raise ValidationError(f"session missing required key: {key}")

    scores = fm["scores"]
    if not isinstance(scores, dict):
        raise ValidationError("scores must be a mapping")
    for key in REQUIRED_SCORES_NUMERIC:
        if key not in scores:
            raise ValidationError(f"scores missing required key: {key}")
        val = scores[key]
        if isinstance(val, bool) or not isinstance(val, int) or val < 0 or val > 10:
            raise ValidationError(f"scores.{key} must be int 0-10, got {val!r}")
    for key in REQUIRED_SCORES_OTHER:
        if key not in scores:
            raise ValidationError(f"scores missing required key: {key}")

    if scores["emotional_response"] not in EMOTIONAL_RESPONSES:
        raise ValidationError(
            f"emotional_response must be one of {sorted(EMOTIONAL_RESPONSES)}"
        )
    for boolkey in ("would_return", "would_recommend"):
        if not isinstance(scores[boolkey], bool):
            raise ValidationError(f"scores.{boolkey} must be bool, got {type(scores[boolkey]).__name__}")

    if not isinstance(fm["elements_noticed"], list):
        raise ValidationError("elements_noticed must be a list")
    if not isinstance(fm["elements_ignored"], list):
        raise ValidationError("elements_ignored must be a list")

    if not body or body.strip() == "":
        raise ValidationError("narrative body must not be empty")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: validate_review.py <path-to-review.md> [more paths...]")
        return 2
    failures = 0
    for arg in sys.argv[1:]:
        path = Path(arg)
        try:
            validate_review(path)
            print(f"OK: {path}")
        except ValidationError as e:
            print(f"FAIL: {path}: {e}")
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
