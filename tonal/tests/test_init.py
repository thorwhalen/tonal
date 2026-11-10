"""Test the lazy package namespace of ``tonal``."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

# Every name ``import tonal`` exposed before the namespace became lazy.
PUBLIC_NAMES = (
    "DFLT_SOUNDFONT",
    "chords",
    "chords_to_midi",
    "chords_to_wav",
    "convert",
    "converters",
    "midi_to_wav",
    "notes",
    "scale_midi_notes",
    "util",
)


@pytest.mark.parametrize("name", PUBLIC_NAMES)
def test_public_name_resolves(name):
    import tonal

    assert getattr(tonal, name) is not None
    exec(f"from tonal import {name}", {})
    assert name in dir(tonal)


def test_star_import_resolves_all_public_names():
    namespace = {}
    exec("from tonal import *", namespace)
    assert set(PUBLIC_NAMES) <= set(namespace)


def test_unknown_name_raises_attribute_error():
    import tonal

    with pytest.raises(AttributeError):
        tonal.no_such_name


def test_importing_notes_does_not_load_heavy_deps():
    code = (
        "import tonal.notes, sys; "
        "assert 'music21' not in sys.modules and 'mido' not in sys.modules"
    )
    import tonal

    # Run the child against THIS tonal, not whatever copy is installed.
    src_root = str(Path(tonal.__file__).resolve().parents[1])
    env = {**os.environ, "PYTHONPATH": os.pathsep.join([src_root, os.environ.get("PYTHONPATH", "")])}
    code += f"; import tonal; assert tonal.__file__.startswith({src_root!r}), tonal.__file__"
    subprocess.run([sys.executable, "-c", code], check=True, env=env)
