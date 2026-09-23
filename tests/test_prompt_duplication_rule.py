#!/usr/bin/env python3
"""Quality rule: an exercise prompt must not repeat its sentence or its step
title (alc-programming#26).

The app's cloze renderer shows ``prompt`` as the heading and ``sentence`` as
the question box (with read-aloud); the step ``title`` is the heading above
the exercise. When ``prompt`` carries the same text as either, the learner
reads the identical question twice on one screen. Ten exercises of the two
React sets shipped that way (six multiselect clozes with ``prompt ==
sentence``, four select clozes with ``prompt == step title``).

Runs under pytest; the last test walks every lesson under ``sets/`` so the
content itself stays clean, not only the rule.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_content as vc  # noqa: E402

RULE_MARKER = "prompt repeats"


def duplication_errors(lesson: dict) -> list[str]:
    errors: list[str] = []
    vc.validate_lesson_quality(lesson, "de", "<lesson>", errors)
    return [e for e in errors if RULE_MARKER in e]


def lesson_with_exercise(exercise: dict, step_title: str = "Ex") -> dict:
    return {
        "id": "l1",
        "title": "T",
        "cards": [],
        "steps": [
            {"id": "s1", "type": "theory", "title": "Th", "body": "b"},
            {"id": "s2", "type": "exercise", "title": step_title, "exercise": exercise},
        ],
    }


def multiselect(prompt: str, sentence: str) -> dict:
    return {
        "id": "e1",
        "type": "cloze",
        "prompt": prompt,
        "card_ids": [],
        "sentence": sentence,
        "accept": ["a", "b"],
        "distractors": ["c"],
        "cloze_mode": "multiselect",
    }


def select(prompt: str) -> dict:
    return {
        "id": "e1",
        "type": "cloze",
        "prompt": prompt,
        "card_ids": [],
        "sentence": "___",
        "accept": ["a"],
        "distractors": ["b", "c"],
        "cloze_mode": "select",
    }


def test_prompt_equal_to_sentence_is_flagged():
    """Reproduction: the shipped multiselect shape (issue #26, useEffect)."""
    question = "Welche Aussagen über useEffect treffen zu?"
    errors = duplication_errors(lesson_with_exercise(multiselect(question, question)))
    assert len(errors) == 1
    assert "sentence" in errors[0]
    assert "e1" in errors[0]


def test_prompt_equal_to_step_title_is_flagged():
    """Reproduction: the shipped select shape (issue #26, useMemo)."""
    question = "Was cached useMemo?"
    errors = duplication_errors(lesson_with_exercise(select(question), step_title=question))
    assert len(errors) == 1
    assert "step title" in errors[0]
    assert "e1" in errors[0]


def test_instruction_prompt_with_question_in_sentence_passes():
    """Happy path: the corrected shape (instruction above, question below)."""
    exercise = multiselect(
        "Wähle alle zutreffenden Aussagen.", "Welche Aussagen über useEffect treffen zu?"
    )
    assert duplication_errors(lesson_with_exercise(exercise, "Aussagen über useEffect")) == []


@pytest.mark.parametrize(
    ("prompt", "sentence", "step_title"),
    [
        pytest.param(None, "Frage?", "Frage?", id="no-prompt-nothing-to-repeat"),
        pytest.param("Frage?", None, "Titel", id="no-sentence-distinct-title"),
        pytest.param("", "", "", id="empty-strings-are-not-a-repeat"),
        pytest.param("Frage?", "___", "Titel", id="select-blank-sentence"),
        pytest.param("Frage?", "Frage!", "Frage.", id="punctuation-differs"),
    ],
)
def test_edge_cases_pass(prompt, sentence, step_title):
    exercise = select("x")
    exercise.pop("prompt")
    if prompt is not None:
        exercise["prompt"] = prompt
    exercise.pop("sentence")
    if sentence is not None:
        exercise["sentence"] = sentence
    assert duplication_errors(lesson_with_exercise(exercise, step_title)) == []


@pytest.mark.parametrize(
    ("prompt", "sentence", "step_title", "expected"),
    [
        pytest.param("Frage? ", "Frage?", "T", "sentence", id="trailing-space-still-a-repeat"),
        pytest.param("Frage?", "S", " Frage?", "step title", id="leading-space-still-a-repeat"),
    ],
)
def test_boundary_whitespace_only_differences_are_flagged(prompt, sentence, step_title, expected):
    errors = duplication_errors(lesson_with_exercise(multiselect(prompt, sentence), step_title))
    assert len(errors) == 1
    assert expected in errors[0]


def test_prompt_repeating_both_reports_both():
    question = "Was ist JSX?"
    errors = duplication_errors(lesson_with_exercise(multiselect(question, question), question))
    assert len(errors) == 2
    assert any("sentence" in e for e in errors)
    assert any("step title" in e for e in errors)


def test_shipped_lessons_carry_no_duplicated_prompt():
    """Content pin: every lesson under sets/ passes the rule."""
    lesson_files = sorted((REPO_ROOT / "sets").glob("*/*/lessons/*.json"))
    assert lesson_files, "no lesson files found under sets/"
    findings: list[str] = []
    for path in lesson_files:
        lesson = json.loads(path.read_text(encoding="utf-8"))
        errors: list[str] = []
        vc.validate_lesson_quality(lesson, "de", str(path.relative_to(REPO_ROOT)), errors)
        findings.extend(e for e in errors if RULE_MARKER in e)
    assert findings == []
