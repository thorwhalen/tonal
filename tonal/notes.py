"""
Notes, scales, and chords definitions.

"Scale quality": ou might also hear "scale family" or "scale class." For example, "major," "minor pentatonic," "harmonic minor," "whole-tone" are all scale qualities.
"""

from typing import Dict, Sequence, Tuple, Callable
from tonal.util import (
    note_name_pattern,
    parse_note_name,
    add_pattern_aliases,
)
from music21.note import Note

# Type aliases for this module
Chord = str
Notes = Sequence[Note]
ChordTimed = Tuple[Chord, Notes]
ChordSequence = Sequence[ChordTimed]
ChordDefinitions = Callable[[Chord], Notes]
ChordRenderer = Callable[[Notes, any, int], None]

# Define root notes to MIDI note numbers
root_notes: Dict[str, int] = {
    'C': 60,
    'C#': 61,
    'Db': 61,
    'D': 62,
    'D#': 63,
    'Eb': 63,
    'E': 64,
    'F': 65,
    'F#': 66,
    'Gb': 66,
    'G': 67,
    'G#': 68,
    'Ab': 68,
    'A': 69,
    'A#': 70,
    'Bb': 70,
    'B': 71,
}


scale_quality = {
    # Western Diatonic & Common Scales (retained as before)
    "major": (0, 2, 4, 5, 7, 9, 11),
    "natural minor": (0, 2, 3, 5, 7, 8, 10),
    "harmonic minor": (0, 2, 3, 5, 7, 8, 11),
    "melodic minor ascending": (0, 2, 3, 5, 7, 9, 11),
    "melodic minor descending": (0, 2, 3, 5, 7, 8, 10),
    "major pentatonic": (0, 2, 4, 7, 9),
    "minor pentatonic": (0, 3, 5, 7, 10),
    "blues": (0, 3, 5, 6, 7, 10),
    "chromatic": (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
    "whole tone": (0, 2, 4, 6, 8, 10),
    "diminished (whole-half)": (0, 2, 3, 5, 6, 8, 9, 11),
    "diminished (half-whole)": (0, 1, 3, 4, 6, 7, 9, 10),
    "augmented": (0, 3, 4, 7, 8, 11),
    "lydian": (0, 2, 4, 6, 7, 9, 11),
    "mixolydian": (0, 2, 4, 5, 7, 9, 10),
    "dorian": (0, 2, 3, 5, 7, 9, 10),
    "phrygian": (0, 1, 3, 5, 7, 8, 10),
    "locrian": (0, 1, 3, 4, 6, 8, 10),
    "aeolian": (0, 2, 3, 5, 7, 8, 10),
    "ionian": (0, 2, 4, 5, 7, 9, 11),
    # Major Jazz Scales (distinct or commonly named in jazz)
    "bebop dominant": (
        0,
        2,
        4,
        5,
        7,
        9,
        10,
        11,
    ),  # Mixolydian with added M7 (or b7, M7)
    "bebop major": (0, 2, 4, 5, 7, 8, 9, 11),  # Major with added b6 (or M6, b6)
    "bebop minor": (0, 2, 3, 4, 5, 7, 9, 10),  # Dorian with added M3 (or m3, M3)
    "bebop melodic minor": (0, 2, 3, 5, 7, 8, 9, 11),  # Melodic Minor with added b6
    "altered": (0, 1, 3, 4, 6, 8, 10),  # 7th mode of Melodic Minor, aka Super Locrian
    "lydian dominant": (
        0,
        2,
        4,
        6,
        7,
        9,
        10,
    ),  # 4th mode of Melodic Minor, aka Mixolydian #11
    "phrygian dominant": (
        0,
        1,
        4,
        5,
        7,
        8,
        10,
    ),  # 5th mode of Harmonic Minor (also common in Middle Eastern music)
    # Indian Ragas (distinct from Western scales, or now canonical here)
    # Re-checking semitone patterns and prioritizing jazz names
    "todi": (0, 1, 3, 6, 7, 8, 11),  # Hindustani Todi Thaat
    "poorvi": (0, 1, 4, 6, 7, 8, 11),  # Hindustani Poorvi Thaat
    "marwa": (0, 1, 4, 6, 7, 9, 11),  # Hindustani Marwa Thaat
    "chalanata": (0, 3, 5, 6, 7, 10, 11),  # Melakarta 36
    "hamsadhwani": (0, 4, 7, 9, 11),  # Pentatonic raga
    # Potential clashes:
    "bhairav": (0, 1, 4, 5, 7, 8, 11),  # Hindustani Bhairav Thaat
    "chakravakam": (0, 1, 4, 5, 7, 9, 10),  # Melakarta 16
    "malkauns": (0, 3, 5, 8, 10),  # Pentatonic raga
}


scale_quality_alias = {
    # Western Aliases (retained and expanded slightly)
    "maj": "major",
    "M": "major",
    "min": "natural minor",
    "m": "natural minor",
    "minor": "natural minor",
    "harmonic": "harmonic minor",
    "melodic": "melodic minor ascending",
    "penta major": "major pentatonic",
    "penta min": "minor pentatonic",
    "penta": "minor pentatonic",
    "minor penta": "minor pentatonic",
    "major penta": "major pentatonic",
    "whl tone": "whole tone",
    "dim": "diminished (whole-half)",
    "aug": "augmented",
    "chrom": "chromatic",
    "blues scale": "blues",
    "dor": "dorian",
    "phr": "phrygian",
    "lyd": "lydian",
    "mix": "mixolydian",
    "aeo": "aeolian",
    "ion": "ionian",
    "nat min": "natural minor",
    "harm min": "harmonic minor",
    "mel min asc": "melodic minor ascending",
    "mel min desc": "melodic minor descending",
    "w-h dim": "diminished (whole-half)",
    "h-w dim": "diminished (half-whole)",
    # Jazz Aliases
    "bebop dom": "bebop dominant",
    "bebop maj": "bebop major",
    "bebop min": "bebop minor",
    "bebop dorian": "bebop minor",  # Common alias for bebop minor
    "bebop melodic": "bebop melodic minor",
    "alt": "altered",
    "super locrian": "altered",
    "lyd dom": "lydian dominant",
    "mixolydian #11": "lydian dominant",
    "acoustic scale": "lydian dominant",  # Also sometimes called this
    "phryg dom": "phrygian dominant",
    "dominant phrygian": "phrygian dominant",
    "mixolydian b2 b6": "phrygian dominant",  # If you want to get descriptive
    # Indian Raga Aliases
    # Aliases for Ragas whose patterns match Western/Jazz scales:
    "bilawal": "major",  # Hindustani Thaat for Major
    "ionian raga": "major",
    "shankarabharanam": "major",  # Carnatic Melakarta 29 for Major
    "dheerasankarabharanam": "major",  # Carnatic Melakarta 29 for Major
    "kharaharapriya": "dorian",  # Carnatic Melakarta 22 for Dorian
    "melakarta 22": "dorian",
    "kafi": "dorian",  # Hindustani Thaat for Dorian
    "harikambhoji": "mixolydian",  # Carnatic Melakarta 28 for Mixolydian
    "melakarta 28": "mixolydian",
    "khamaj": "mixolydian",  # Hindustani Thaat for Mixolydian
    "natabhairavi": "natural minor",  # Carnatic Melakarta 20 for Natural Minor
    "melakarta 20": "natural minor",
    "asavari": "natural minor",  # Hindustani Thaat for Natural Minor / Aeolian
    "aeolian raga": "natural minor",
    "hanumatodi": "phrygian",  # Carnatic Melakarta 8 for Phrygian
    "melakarta 8": "phrygian",
    "phrygian raga": "phrygian",
    "kalyan": "lydian",  # Hindustani Thaat for Lydian
    "kirwani": "harmonic minor",  # Melakarta 21, identical to Harmonic Minor
    "melakarta 21": "harmonic minor",
    "mayamalavagowla": "bhairav",  # Carnatic Melakarta 15
    "melakarta 15": "bhairav",
    "bhupali": "major pentatonic",  # Hindustani Raga identical to Major Pentatonic
    "mohnam": "major pentatonic",  # Carnatic equivalent of Bhupali / Major Pentatonic
    "durga": "major pentatonic",
    "deshkar": "major pentatonic",
    "carnatic major": "major",  # Common reference for the Carnatic major scale
    "carnatic minor": "natural minor",  # Common reference for the Carnatic natural minor scale
    # Aliases for Ragas unique to scale_quality (or now canonical here)
    "bhairav thaat": "bhairav",
    "todi thaat": "todi",
    "poorvi thaat": "poorvi",
    "marwa thaat": "marwa",
    "melakarta 36": "chalanata",
    "melakarta 16": "chakravakam",
    "hansadhwani raga": "hamsadhwani",
    "malkauns raga": "malkauns",
    "indian m minor": "malkauns",  # A less common, but sometimes used, description
}


# TODO: Verify completeness and more chord definitions if needed
# TODO: See if defs can be infered from parsing the chord names
# Define quality and extension intervals
chord_quality: Dict[str, Sequence[int]] = {
    '': (0, 4, 7),  # Major triad, 'C' -> 'Cmaj
    'maj': (0, 4, 7),  # Major triad
    'min': (0, 3, 7),  # Minor triad
    'dim': (0, 3, 6),  # Diminished triad
    'aug': (0, 4, 8),  # Augmented triad
    '7': (0, 4, 7, 10),  # Dominant 7th
    'maj7': (0, 4, 7, 11),  # Major 7th
    'min7': (0, 3, 7, 10),  # Minor 7th
    'minmaj7': (0, 3, 7, 11),  # Minor major 7th
    'dim7': (0, 3, 6, 9),  # Diminished 7th
    'hdim7': (0, 3, 6, 10),  # Half-diminished 7th
    'aug7': (0, 4, 8, 10),  # Augmented 7th
    '6': (0, 4, 7, 9),  # Major 6th
    'min6': (0, 3, 7, 9),  # Minor 6th
    '9': (0, 4, 7, 10, 14),  # Dominant 9th
    'maj9': (0, 4, 7, 11, 14),  # Major 9th
    'min9': (0, 3, 7, 10, 14),  # Minor 9th
    '11': (0, 4, 7, 10, 14, 17),  # Dominant 11th
    'maj11': (0, 4, 7, 11, 14, 17),  # Major 11th
    'min11': (0, 3, 7, 10, 14, 17),  # Minor 11th
    '13': (0, 4, 7, 10, 14, 17, 21),  # Dominant 13th
    'maj13': (0, 4, 7, 11, 14, 17, 21),  # Major 13th
    'min13': (0, 3, 7, 10, 14, 17, 21),  # Minor 13th
}

# -----------------------------------------------------------------------------
# Registration
# -----------------------------------------------------------------------------


# TODO: Make a framework for user-defined aliases


# -----------------------------------------------------------------------------
# Validation
# -----------------------------------------------------------------------------


def validate_scale_semitone_pattern_uniquness(scale_quality: dict) -> bool:
    """
    Validates that all scale qualities have unique semitone patterns.
    """
    seen = {}
    for name, pattern in scale_quality.items():
        pattern_tuple = tuple(pattern)
        if pattern_tuple in seen:
            raise ValueError(
                f"Scale quality '{name}' has a non-unique semitone pattern. "
                f"Duplicates: {seen[pattern_tuple]} and {name}"
            )
        seen[pattern_tuple] = name
    return True


def validate_scale_aliases(scale_quality: dict, scale_aliases: dict) -> bool:
    """
    Validates that all values in the scale_aliases dictionary are valid keys
    in the scale_qualities dictionary.

    Args:
        scale_quality (dict): The dictionary of canonical scale qualities and patterns.
        scale_aliases (dict): The dictionary of scale aliases.

    Returns:
        bool: True if all aliases are valid, False otherwise.
    """
    all_valid = True
    invalid_aliases = []
    for alias_key, canonical_name in scale_aliases.items():
        if canonical_name not in scale_quality:
            print(
                f"Validation Error: Alias '{alias_key}' points to "
                f"non-existent scale quality '{canonical_name}' in scale_quality."
            )
            invalid_aliases.append(alias_key)
            all_valid = False

    if not all_valid:
        raise ValueError(f"Invalid aliases found: {invalid_aliases}")


# validate_scale_semitone_pattern_uniquness(scale_quality)  # Disabled: duplicate patterns are allowed for now
validate_scale_aliases(scale_quality, scale_quality_alias)
