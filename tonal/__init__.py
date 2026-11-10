"""Tools to generate music.

The package namespace is lazy (PEP 562): the names below are imported from their
submodules on first access, so ``import tonal.notes`` does not pull in the heavy
dependencies (music21, mido) that ``tonal.chords`` and ``tonal.util`` need.
"""

from importlib import import_module

# Public name -> submodule that defines it.
_LAZY_ATTRS = {
    "chords_to_wav": "tonal.chords",
    "chords_to_midi": "tonal.chords",
    "DFLT_SOUNDFONT": "tonal.util",
    "convert": "tonal.converters",
    "midi_to_wav": "tonal.converters",
    "scale_midi_notes": "tonal.notes",
}

# Submodules that were reachable as ``tonal.<name>`` after ``import tonal``.
_LAZY_SUBMODULES = ("chords", "converters", "notes", "util")

__all__ = [*_LAZY_ATTRS, *_LAZY_SUBMODULES]


def __getattr__(name):
    if name in _LAZY_ATTRS:
        value = getattr(import_module(_LAZY_ATTRS[name]), name)
    elif name in _LAZY_SUBMODULES:
        value = import_module(f"{__name__}.{name}")
    else:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    globals()[name] = value  # cache, so __getattr__ is not called again
    return value


def __dir__():
    return sorted(set(globals()) | set(_LAZY_ATTRS) | set(_LAZY_SUBMODULES))
