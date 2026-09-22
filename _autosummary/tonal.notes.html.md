# tonal.notes

Notes, scales, and chords definitions.

A few definitions:

* Scale Quality: The characteristic sound or “flavor” of a scale, determined by its
  specific pattern of intervals (semitones) from the root note.

Examples include major, minor, pentatonic, blues, or whole-tone.

* Chord Quality: The characteristic sound or “flavor” of a chord, determined by its
  specific combination of intervals (semitones) above its root note.

Common examples include major, minor, diminished, augmented, or dominant 7th.

* Semitone Pattern: A numerical representation of a musical scale or chord, showing
  the precise distance in semitones (half-steps) of each note from the starting (root)
  note. For example, the semitone pattern for a major scale is [0, 2, 4, 5, 7, 9, 11].

### Functions

| [`add_pattern_aliases`](#tonal.notes.add_pattern_aliases)(quality_extensions)        | Generate common textual aliases for quality-extension keys.                                                 |
|-------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| [`canonical_quality_name`](#tonal.notes.canonical_quality_name)(quality)                | Return the canonical quality key from `scale_quality`.                                                      |
| [`list_chord_qualities`](#tonal.notes.list_chord_qualities)()                         | List all registered chord qualities.                                                                        |
| [`list_root_notes`](#tonal.notes.list_root_notes)()                              | List all registered root notes.                                                                             |
| [`list_scale_qualities`](#tonal.notes.list_scale_qualities)([include_aliases])        | List all registered scale qualities.                                                                        |
| [`list_scale_quality_aliases`](#tonal.notes.list_scale_quality_aliases)()                   | List all registered scale quality aliases.                                                                  |
| [`list_scales_string`](#tonal.notes.list_scales_string)()                           | Return a user-friendly help string describing scale syntax and valid values.                                |
| [`parse_note_name`](#tonal.notes.parse_note_name)(note_str)                      | Parse a note name prefix from a string.                                                                     |
| [`register_chord_quality`](#tonal.notes.register_chord_quality)(quality_name, ...)      | Register a new chord quality with its semitone pattern.                                                     |
| [`register_root_note`](#tonal.notes.register_root_note)(note_name, midi_value)      | Register a new root note with its MIDI value.                                                               |
| [`register_scale_quality`](#tonal.notes.register_scale_quality)(quality_name, ...)      | Register a new scale quality with its semitone pattern.                                                     |
| [`register_scale_quality_alias`](#tonal.notes.register_scale_quality_alias)(alias, ...)       | Register an alias for an existing scale quality.                                                            |
| [`scale_midi_notes`](#tonal.notes.scale_midi_notes)([scale, midi_range, ...])     | Return a tuple of all MIDI note numbers in the given range that belong to the specified scale.              |
| [`scale_params`](#tonal.notes.scale_params)(scale[, midi_notes])              | Parse a scale specification string and return (root_note, scale_quality).                                   |
| [`semitone_pattern`](#tonal.notes.semitone_pattern)(quality)                      | Get the semitone pattern for a given scale quality string.                                                  |
| [`validate_scale_aliases`](#tonal.notes.validate_scale_aliases)(scale_quality, ...)     | Validates that all values in the scale_aliases dictionary are valid keys in the scale_qualities dictionary. |
| [`validate_scale_semitone_pattern_uniquness`](#tonal.notes.validate_scale_semitone_pattern_uniquness)(...) | Validates that all scale qualities have unique semitone patterns.                                           |

### Exceptions

| [`IncorrectScaleSpecification`](#tonal.notes.IncorrectScaleSpecification)   | Raised when a scale string cannot be parsed/validated into root and quality.   |
|--------------------------------------------------------------------------------|--------------------------------------------------------------------------------|

### *exception* tonal.notes.IncorrectScaleSpecification

Bases: [`ValueError`](https://docs.python.org/3/builtins/exceptions.html#ValueError)

Raised when a scale string cannot be parsed/validated into root and quality.

### tonal.notes.add_pattern_aliases(quality_extensions)

Generate common textual aliases for quality-extension keys.

This is shared logic used by several modules (e.g. mapping maj->M, min->m).

* **Return type:**
  [`Iterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator)[[`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]]]

```pycon
>>> d = {'maj7': (0, 4, 7, 11), 'min7': (0, 3, 7, 10)}
>>> dict(add_pattern_aliases(d))['M7']
(0, 4, 7, 11)
```

### tonal.notes.canonical_quality_name(quality)

Return the canonical quality key from `scale_quality`.

Accepts aliases (including chains) and normalizes spaces to underscores.
Raises ValueError if no mapping exists.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

### Examples

- “minor” -> “natural_minor”
- “bebop_dom” -> “bebop_dominant”
- “minor pentatonic” -> “minor_pentatonic”

### tonal.notes.list_chord_qualities()

List all registered chord qualities.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]]
* **Returns:**
  Dictionary mapping quality names to semitone patterns

```pycon
>>> qualities = list_chord_qualities()
>>> 'maj' in qualities
True
>>> qualities['maj']
(0, 4, 7)
```

### tonal.notes.list_root_notes()

List all registered root notes.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`int`](https://docs.python.org/3/builtins/functions.html#int)]
* **Returns:**
  Dictionary mapping note names to MIDI values

```pycon
>>> notes = list_root_notes()
>>> 'C' in notes
True
>>> notes['C']
60
```

### tonal.notes.list_scale_qualities(include_aliases=False)

List all registered scale qualities.

* **Parameters:**
  **include_aliases** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, include aliases in the listing
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]]
* **Returns:**
  Dictionary mapping quality names to semitone patterns

```pycon
>>> qualities = list_scale_qualities()
>>> 'major' in qualities
True
>>> qualities['major']
(0, 2, 4, 5, 7, 9, 11)
```

### tonal.notes.list_scale_quality_aliases()

List all registered scale quality aliases.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]
* **Returns:**
  Dictionary mapping aliases to canonical names

```pycon
>>> aliases = list_scale_quality_aliases()
>>> 'maj' in aliases
True
>>> aliases['maj']
'major'
```

### tonal.notes.list_scales_string()

Return a user-friendly help string describing scale syntax and valid values.

Includes:

- Anatomy of a scale specification
- Valid roots
- Valid qualities (including aliases)

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

### tonal.notes.parse_note_name(note_str)

Parse a note name prefix from a string.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

```pycon
>>> parse_note_name('C#4')
'C#'
>>> parse_note_name('Eb')
'Eb'
```

### tonal.notes.register_chord_quality(quality_name, semitone_pattern)

Register a new chord quality with its semitone pattern.

* **Parameters:**
  * **quality_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – The name of the chord quality
  * **semitone_pattern** ([`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]) – Sequence of semitone intervals from root
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

```pycon
>>> register_chord_quality('my_chord', (0, 4, 7, 10, 13))
>>> chord_quality['my_chord']
(0, 4, 7, 10, 13)
```

### tonal.notes.register_root_note(note_name, midi_value)

Register a new root note with its MIDI value.

* **Parameters:**
  * **note_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – The name of the note (e.g., ‘C’, ‘C#’, ‘Db’)
  * **midi_value** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – The MIDI note number (0-127)
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

```pycon
>>> register_root_note('H', 71)  # German notation for B
>>> root_notes['H']
71
```

### tonal.notes.register_scale_quality(quality_name, semitone_pattern)

Register a new scale quality with its semitone pattern.

* **Parameters:**
  * **quality_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – The name of the scale quality
  * **semitone_pattern** ([`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]) – Sequence of semitone intervals from root
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

```pycon
>>> register_scale_quality('custom_scale', (0, 2, 5, 7, 10))
>>> scale_quality['custom_scale']
(0, 2, 5, 7, 10)
```

### tonal.notes.register_scale_quality_alias(alias, canonical_name)

Register an alias for an existing scale quality.

* **Parameters:**
  * **alias** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – The alias name
  * **canonical_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – The existing scale quality name or alias
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

```pycon
>>> register_scale_quality_alias('my_major', 'major')
>>> scale_quality_alias['my_major']
'major'
```

### tonal.notes.scale_midi_notes(scale='C major', midi_range=(0, 127), , default_root='C')

Return a tuple of all MIDI note numbers in the given range that belong to the specified scale.

* **Parameters:**
  * **scale** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – The scale string, e.g., ‘C major’, ‘D# minor pentatonic’.
  * **midi_range** ([`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`int`](https://docs.python.org/3/builtins/functions.html#int), [`int`](https://docs.python.org/3/builtins/functions.html#int)]) – The (min, max) MIDI note numbers to include.
  * **default_root** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – The root note to use if not found in the scale string (default ‘C’).
* **Returns:**
  MIDI note numbers in the scale within the specified range.
* **Return type:**
  [`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)

```pycon
>>> scale_midi_notes('E')
(1, 3, 4, 6, 8, 9, 11, 13, 15, 16, ...114, 116, 117, 119, 121, 123, 124, 126)
```

If it’s suprising that it starts at 1, because you were expecting ‘E’ (major)
to start with 4, remember that scale_midi_notes is designed to return all notes in the scale
within the MIDI range, not just the notes starting from the root note.
The first note in that range that is in E major is actually a C#, which the
midi note 1 is. You can control the range through:

```pycon
>>> scale_midi_notes('E', midi_range=(4, 30))
(4, 6, 8, 9, 11, 13, 15, 16, 18, 20, 21, 23, 25, 27, 28, 30)
```

You see that if no scale quality is specified, it defaults to ‘major’.
On the other hand, if no root note is specified, it defaults to ‘C’, or what ever
you tell `default_root` is should be.

```pycon
>>> assert (
...     scale_midi_notes('', midi_range=(60, 72))
...     == scale_midi_notes('C', midi_range=(60, 72))
...     == scale_midi_notes('major', midi_range=(60, 72))
...     == scale_midi_notes('C major', midi_range=(60, 72))
...     == (60, 62, 64, 65, 67, 69, 71, 72)
... )
```

```pycon
>>> scale_midi_notes('Db minor pentatonic', midi_range=(60, 72))
(61, 64, 66, 68, 71)
```

### tonal.notes.scale_params(scale, midi_notes=False)

Parse a scale specification string and return (root_note, scale_quality).
If midi_notes is True, returns (root_note_midi, semitone_pattern).
If midi_notes is False, returns (root_note_str, scale_quality_str).
The root_note can be an empty string (meaning default root).

```pycon
>>> scale_params('C major')
('C', 'major')
>>> scale_params('dorian')
('', 'dorian')
>>> scale_params('C')
('C', 'major')
>>> scale_params('C', midi_notes=True)
(60, (0, 2, 4, 5, 7, 9, 11))
>>> scale_params('dorian', midi_notes=True)
(None, (0, 2, 3, 5, 7, 9, 10))
```

### tonal.notes.semitone_pattern(quality)

Get the semitone pattern for a given scale quality string.
Looks in scale_quality, then in scale_quality_alias (using the alias to look in scale_quality).
Raises ValueError if not found.

* **Return type:**
  [`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)

```pycon
>>> semitone_pattern('major')
(0, 2, 4, 5, 7, 9, 11)
>>> semitone_pattern('maj')
(0, 2, 4, 5, 7, 9, 11)
>>> semitone_pattern('')
(0, 2, 4, 5, 7, 9, 11)
>>> semitone_pattern('dorian')
(0, 2, 3, 5, 7, 9, 10)
```

### tonal.notes.validate_scale_aliases(scale_quality, scale_aliases)

Validates that all values in the scale_aliases dictionary are valid keys
in the scale_qualities dictionary.

* **Parameters:**
  * **scale_quality** ([`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)) – The dictionary of canonical scale qualities and patterns.
  * **scale_aliases** ([`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)) – The dictionary of scale aliases.
* **Returns:**
  True if all aliases are valid, False otherwise.
* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)

### tonal.notes.validate_scale_semitone_pattern_uniquness(scale_quality)

Validates that all scale qualities have unique semitone patterns.

* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)
