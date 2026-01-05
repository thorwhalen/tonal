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
    """Common alterations should not cause failures (base quality is used)."""
    notes = chord_to_notes("A7b9")
    assert len(notes) == 4
    assert notes[3] - notes[0] == 10  # dominant 7th
