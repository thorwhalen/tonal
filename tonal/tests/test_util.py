"""Tests for small helpers in ``tonal.util``."""

import pytest

from tonal.util import (
    add_pattern_aliases,
    ensure_part_filter,
    identity_func,
    parse_note_name,
)


def test_parse_note_name_takes_letter_and_accidental():
    assert parse_note_name("C#4") == "C#"
    assert parse_note_name("bb3") == "bb"
    assert parse_note_name("G") == "G"
    with pytest.raises(ValueError, match="Invalid note string"):
        parse_note_name("4C")


def test_ensure_part_filter_accepts_int_container_none_and_callable():
    keep = lambda i, part: part == "x"
    assert ensure_part_filter(keep) is keep
    assert ensure_part_filter(1)(1, "p") and not ensure_part_filter(1)(0, "p")
    assert ensure_part_filter({0, 2})(2, "p") and not ensure_part_filter({0, 2})(1, "p")
    assert ensure_part_filter(None)(99, "p")


def test_ensure_part_filter_rejects_other_types():
    with pytest.raises(TypeError, match="part_filter must be"):
        ensure_part_filter(3.5)


def test_add_pattern_aliases_ignores_other_keys():
    assert dict(add_pattern_aliases({"maj": 1, "min7": 2, "dim7": 3, "aug": 4})) == {
        "M": 1,
        "m7": 2,
        "°7": 3,
    }
    assert identity_func(5) == 5
