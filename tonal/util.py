"""Utils for sonify."""

from importlib.resources import files
from functools import partial
from dol import Pipe
from config2py import (
    process_path,
    simple_config_getter,
)

pkg_name = 'sonify'

data_files = files(pkg_name) / 'data'

get_config = simple_config_getter(pkg_name)


DFLT_OUTPUT_NAME = 'audio_output'
DFLT_MIDI_OUTPUT = f"{DFLT_OUTPUT_NAME}.mid"
DFLT_WAV_OUTPUT = f"{DFLT_OUTPUT_NAME}.wav"
DFLT_SOUNDFONT = process_path(
    get_config('SONIFY_DFLT_SOUNDFONT_PATH'),
)
