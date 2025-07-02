"""Tools for chords and chord progressions."""

from mido import MidiFile, MidiTrack, Message
import subprocess
from typing import Sequence, Tuple, Callable, Mapping, Dict
import os
import re
from config2py import process_path
from tonal.util import (
    DFLT_OUTPUT_NAME,
    DFLT_MIDI_OUTPUT,
    DFLT_SOUNDFONT,
    note_name_pattern,
    parse_note_name,
    add_pattern_aliases,
)
from tonal.notes import root_notes, chord_quality
from music21.note import Note

DFLT_CHORD_SEQUENCE = [
    ("Bdim", 120),
    ("Em11", 120),
    ("Amin9", 120),
    ("Dm7", 120),
    "G7",
    "Cmaj7",
]

# Type aliases for this module
Chord = str
Notes = Sequence[Note]
ChordTimed = Tuple[Chord, Notes]
ChordSequence = Sequence[ChordTimed]
ChordDefinitions = Callable[[Chord], Notes]
ChordRenderer = Callable[[Notes, any, int], None]


def chord_to_notes(chord: Chord) -> Notes:
    """
    Parse a chord string and return the corresponding sequence of MIDI note numbers.

    :param chord: The chord string (e.g., 'Cmaj7').
    :return: A sequence of MIDI note numbers representing the chord.
    """
    root = parse_note_name(chord)
    quality_extension = chord[len(root) :]
    root_midi = root_notes.get(root)
    # print(root, root_midi, quality_extension)

    if root_midi is None:
        raise ValueError(f"Unknown root note: {root}")

    intervals = chord_quality.get(quality_extension)

    if intervals is None:
        raise ValueError(f"Unknown quality/extension: {quality_extension}")

    return [root_midi + interval for interval in intervals]


if not os.path.exists(DFLT_SOUNDFONT):
    from warnings import warn

    warn(f"Soundfont not found at {DFLT_SOUNDFONT}")


chord_renders = {}


def register_chord_render(chord_renderer: ChordRenderer, name=None):
    if name is None:
        name = chord_renderer.__name__
    chord_renders[chord_renderer.__name__] = chord_renderer
    return chord_renderer


@register_chord_render
def play_simultaneously(
    notes: Sequence[int], track: MidiTrack, duration: int, *, velocity=64
):
    v = velocity
    for note in notes:
        track.append(Message("note_on", note=note, velocity=v, time=0))
    _notes = iter(notes)
    track.append(Message("note_off", note=next(_notes), velocity=v, time=duration))
    for note in _notes:
        track.append(Message("note_off", note=note, velocity=v, time=0))


# TODO: Need a better implementation for arpeggios.
@register_chord_render
def play_arpeggio(
    notes: Sequence[int], track: MidiTrack, duration: int, *, velocity=64
):
    v = velocity
    note_duration = duration // len(notes)
    current_time = 0
    for note in notes:
        track.append(Message("note_on", note=note, velocity=v, time=current_time))
        current_time += note_duration
        track.append(Message("note_off", note=note, velocity=v, time=current_time))


def resolve_chord_render(chord_renderer: ChordRenderer) -> ChordRenderer:
    if isinstance(chord_renderer, str):
        name = chord_renderer
        chord_renderer = chord_renders.get(name)
        if chord_renderer is None:
            raise ValueError(
                f"Unknown chord renderer: {name}. "
                '(Available: {", ".join(chord_renders)}). '
                "You can register a new chord renderer with `register_chord_render`."
            )
        return chord_renderer
    return chord_renderer


DFLT_DURATION = 240 * 4


def process_chord_sequence(
    chord_sequence: ChordSequence, default_duration=DFLT_DURATION
):
    """Preprocess a chord sequence, to make sure to add time, etc."""
    for chord in chord_sequence:
        if isinstance(chord, str):
            yield chord, default_duration
        elif isinstance(chord, tuple):
            yield chord
        else:
            raise ValueError(f"Invalid chord: {chord}")


def chords_to_midi(
    chord_sequence: ChordSequence = DFLT_CHORD_SEQUENCE,
    *,
    output_file: str = None,  # DFLT_MIDI_OUTPUT,
    render_chord: ChordRenderer = play_simultaneously,
    chord_definitions: ChordDefinitions = chord_to_notes,
):
    """
    Generate a MIDI file from a chord sequence.

    :param chord_sequence: List of tuples containing chords and their duration.
    :param chord_definitions: Dictionary mapping chords to MIDI note patterns.
    :param output_file: Name of the output MIDI file.
    :param render_chord: Function defining how the chords should be played.
    """
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)

    render_chord = resolve_chord_render(render_chord)
    chord_sequence = process_chord_sequence(chord_sequence)

    track.append(Message("program_change", program=0, time=0))  # Acoustic Grand Piano

    for chord, duration in chord_sequence:
        pattern = chord_definitions(chord)
        if pattern:
            render_chord(pattern, track, duration)

    if output_file:
        midi.save(output_file)
        return output_file
    else:
        return midi


def chords_to_wav(
    chord_sequence: ChordSequence = DFLT_CHORD_SEQUENCE,
    name: str = DFLT_OUTPUT_NAME,
    *,
    chord_definitions: ChordDefinitions = chord_to_notes,
    soundfont: str = DFLT_SOUNDFONT,
    render_chord: ChordRenderer = play_simultaneously,
):
    """
    Generate a WAV file directly from a chord sequence.

    :param chord_sequence: List of tuples containing chords and their duration.
    :param name: Base name for the output MIDI and WAV files.
    :param chord_definitions: Dictionary mapping chords to MIDI note patterns.
    :param soundfont: Path to the SoundFont file.
    :param render_chord: Function defining how the chords should be played.
    """
    from sonification.converters import midi_to_wav

    midi_file = f"{name}.mid"
    wav_file = f"{name}.wav"

    chords_to_midi(
        chord_sequence,
        chord_definitions=chord_definitions,
        output_file=midi_file,
        render_chord=render_chord,
    )
    midi_to_wav(midi_file=midi_file, output_wav=wav_file, soundfont=soundfont)
    return wav_file
