"""Utils for sonify."""

from importlib.resources import files
from config2py import (
    process_path,
    simple_config_getter,
)

pkg_name = 'tonal'

data_files = files(pkg_name) / 'data'

get_config = simple_config_getter(pkg_name)


DFLT_OUTPUT_NAME = 'audio_output'
DFLT_MIDI_OUTPUT = f"{DFLT_OUTPUT_NAME}.mid"
DFLT_WAV_OUTPUT = f"{DFLT_OUTPUT_NAME}.wav"
DFLT_SOUNDFONT = process_path(
    get_config('TONAL_DFLT_SOUNDFONT_PATH'),
)

from music21.stream import Score, Stream
from music21.midi.realtime import StreamPlayer


def play_music21_object(music21_obj):
    """
    Plays a music21 object (Chord, Part, Stream, etc.) using the StreamPlayer.

    Args:
        music21_obj: A music21 object (Chord, Part, Stream, etc.) to be played.
    """
    if isinstance(music21_obj, Score):
        s = music21_obj
    else:
        # Create a Stream object
        s = Stream()
        # Add the music21 object to the Stream
        s.append(music21_obj)

    # Play the Stream using StreamPlayer
    sp = StreamPlayer(s)
    sp.play()
