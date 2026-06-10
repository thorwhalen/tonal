"""Tests for tonal.chords chord symbol parsing."""

import pytest

from tonal.chords import chord_to_notes


@pytest.mark.parametrize(
    "symbol, expected_intervals",
    [
        ("C", (0, 4, 7)),
        ("C-", (0, 3, 7)),
        ("C^7", (0, 4, 7, 11)),
        ("C-7", (0, 3, 7, 10)),
        ("Co7", (0, 3, 6, 9)),
        ("Ch7", (0, 3, 6, 10)),
    ],
)
def test_chord_to_notes_supports_ireal_symbols(symbol: str, expected_intervals):
    """Support iReal-style chord qualities used by accompy."""
    notes = chord_to_notes(symbol)
    assert len(notes) == len(expected_intervals)
    root = notes[0]
    assert tuple(n - root for n in notes) == tuple(expected_intervals)


def test_chord_to_notes_ignores_slash_bass_note():
    """Slash chords should parse without error (bass inversion is ignored)."""
    a = chord_to_notes("C^7/G")
    b = chord_to_notes("C^7")
    assert [n % 12 for n in a] == [n % 12 for n in b]


def test_chord_to_notes_simplifies_common_alterations():
    """Undefined alterations fall back to the base quality (suffix stripped)."""
    # 7#11 is not a defined quality, so it strips to a plain dominant 7th.
    notes = chord_to_notes("A7#11")
    assert len(notes) == 4
    assert notes[3] - notes[0] == 10  # dominant 7th


def test_chord_to_notes_honors_defined_alterations():
    """Alterations that are defined qualities are honored, not stripped."""
    notes = chord_to_notes("A7b9")
    assert len(notes) == 5
    root = notes[0]
    assert tuple(n - root for n in notes) == (0, 4, 7, 10, 13)  # dominant 7th flat 9
