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


# --- coverage pass: renderers, sequences, midi output ----------------------------------

import tonal.chords as chords
from mido import MidiFile


def _messages(track):
    return [
        (m.type, getattr(m, "note", None), m.time)
        for m in track
        if m.type != "program_change"
    ]


def test_play_simultaneously_starts_together_and_releases_after_the_duration():
    track = []
    chords.play_simultaneously([60, 64, 67], track, 480)
    assert _messages(track) == [
        ("note_on", 60, 0),
        ("note_on", 64, 0),
        ("note_on", 67, 0),
        ("note_off", 60, 480),
        ("note_off", 64, 0),
        ("note_off", 67, 0),
    ]


def test_play_arpeggio_spreads_the_notes_over_the_duration():
    track = []
    chords.play_arpeggio([60, 64], track, 400)
    assert _messages(track) == [
        ("note_on", 60, 0),
        ("note_off", 60, 200),
        ("note_on", 64, 200),
        ("note_off", 64, 400),
    ]


def test_resolve_chord_render_by_name_and_by_callable():
    assert chords.resolve_chord_render("play_arpeggio") is chords.play_arpeggio
    fn = lambda *a, **k: None
    assert chords.resolve_chord_render(fn) is fn
    with pytest.raises(ValueError, match="Unknown chord renderer: nope"):
        chords.resolve_chord_render("nope")


def test_register_chord_render_honours_an_explicit_name():
    def my_render(notes, track, duration, *, velocity=64): ...

    try:
        chords.register_chord_render(my_render, name="alias")
        assert "alias" in chords.chord_renders
    finally:
        chords.chord_renders.pop("my_render", None)
        chords.chord_renders.pop("alias", None)


def test_register_chord_render_defaults_to_the_function_name():
    def another(notes, track, duration, *, velocity=64): ...

    try:
        assert chords.register_chord_render(another) is another
        assert chords.chord_renders["another"] is another
    finally:
        chords.chord_renders.pop("another", None)


def test_unknown_renderer_message_lists_the_available_ones():
    with pytest.raises(ValueError) as exc:
        chords.resolve_chord_render("nope")
    assert "play_arpeggio" in str(exc.value)


def test_process_chord_sequence_adds_durations_and_rejects_junk():
    out = list(chords.process_chord_sequence(["C", ("G", 10)], default_duration=5))
    assert out == [("C", 5), ("G", 10)]
    with pytest.raises(ValueError, match="Invalid chord"):
        list(chords.process_chord_sequence([42]))


def test_chords_to_midi_returns_a_midifile_or_writes_one(tmp_path):
    midi = chords.chords_to_midi(["C", ("G7", 100)])
    assert isinstance(midi, MidiFile) and len(midi.tracks[0]) > 1
    out = tmp_path / "x.mid"
    assert chords.chords_to_midi(["C"], output_file=str(out)) == str(out)
    assert len(MidiFile(str(out)).tracks[0]) > 1


def test_chords_to_midi_accepts_a_renderer_name_and_custom_definitions():
    midi = chords.chords_to_midi(
        ["X"], render_chord="play_arpeggio", chord_definitions=lambda c: [60, 64]
    )
    assert any(m.type == "note_on" for m in midi.tracks[0])
    empty = chords.chords_to_midi(["X"], chord_definitions=lambda c: [])
    assert [m.type for m in empty.tracks[0]] == ["program_change"]


@pytest.mark.parametrize("bad", ["H", "Cwhatever", "", "  "])
def test_chord_to_notes_rejects_unknown_roots_and_qualities(bad):
    with pytest.raises(ValueError):
        chords.chord_to_notes(bad)
