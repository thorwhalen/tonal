# tonal

Tools to generate music.

The package namespace is lazy (PEP 562): the names below are imported from their
submodules on first access, so `import tonal.notes` does not pull in the heavy
dependencies (music21, mido) that `tonal.chords` and `tonal.util` need.

### Functions

| [`chords_to_wav`](#tonal.chords_to_wav)([chord_sequence, name, ...])      | Generate a WAV file directly from a chord sequence.                                            |
|--------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| [`chords_to_midi`](#tonal.chords_to_midi)([chord_sequence, ...])           | Generate a MIDI file from a chord sequence.                                                    |
| [`convert`](#tonal.convert)(src[, dest, src_format, ...])           | Convert between different music formats.                                                       |
| [`midi_to_wav`](#tonal.midi_to_wav)(midi_file[, output_wav, soundfont]) | Synthesize audio from a MIDI file using FluidSynth.                                            |
| [`scale_midi_notes`](#tonal.scale_midi_notes)([scale, midi_range, ...])      | Return a tuple of all MIDI note numbers in the given range that belong to the specified scale. |

### tonal.chords_to_midi(chord_sequence=[('Bdim', 120), ('Em11', 120), ('Amin9', 120), ('Dm7', 120), 'G7', 'Cmaj7'], \*, output_file=None, render_chord=<function play_simultaneously>, chord_definitions=<function chord_to_notes>)

Generate a MIDI file from a chord sequence.

* **Parameters:**
  * **chord_sequence** ([`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]]]) – List of tuples containing chords and their duration.
  * **chord_definitions** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)], [`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]]) – Dictionary mapping chords to MIDI note patterns.
  * **output_file** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of the output MIDI file.
  * **render_chord** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[`int`](https://docs.python.org/3/builtins/functions.html#int)], `any`, [`int`](https://docs.python.org/3/builtins/functions.html#int)], [`None`](https://docs.python.org/3/builtins/constants.html#None)]) – Function defining how the chords should be played.

### tonal.chords_to_wav(chord_sequence=[('Bdim', 120), ('Em11', 120), ('Amin9', 120), ('Dm7', 120), 'G7', 'Cmaj7'], name='audio_output', \*, chord_definitions=<function chord_to_notes>, soundfont='/home/runner/work/tonal/tonal/tonal/data/Caeds Small Trash GM v1.06.sf2', render_chord=<function play_simultaneously>)

Generate a WAV file directly from a chord sequence.

* **Parameters:**
  * **chord_sequence** ([`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]]]) – List of tuples containing chords and their duration.
  * **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Base name for the output MIDI and WAV files.
  * **chord_definitions** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)], [`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]]) – Dictionary mapping chords to MIDI note patterns.
  * **soundfont** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to the SoundFont file.
  * **render_chord** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[`int`](https://docs.python.org/3/builtins/functions.html#int)], `any`, [`int`](https://docs.python.org/3/builtins/functions.html#int)], [`None`](https://docs.python.org/3/builtins/constants.html#None)]) – Function defining how the chords should be played.

### tonal.convert(src, dest=None, , src_format=None, dest_format=None, format_for_extension={'.jpeg': 'image', '.jpg': 'image', '.mid': 'midi', '.midi': 'midi', '.musicxml': 'musicxml', '.png': 'image', '.wav': 'wav', '.xml': 'musicxml'})

Convert between different music formats.

* **Parameters:**
  * **src** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str) | [`bytes`](https://docs.python.org/3/builtins/stdtypes.html#bytes)) – Source as a filepath or bytes data
  * **dest** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str) | [`None`](https://docs.python.org/3/builtins/constants.html#None)) – Destination filepath, format string, or None to return bytes
  * **src_format** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str) | [`None`](https://docs.python.org/3/builtins/constants.html#None)) – Source format, inferred from filepath extension if None
  * **dest_format** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str) | [`None`](https://docs.python.org/3/builtins/constants.html#None)) – Destination format, inferred from dest if None
  * **format_for_extension** – Mapping of file extensions to format names
* **Returns:**
  returns the destination filepath
  If dest is None or a format string or src is bytes: returns the converted bytes
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str) | [`bytes`](https://docs.python.org/3/builtins/stdtypes.html#bytes)

### Examples

# File to file conversion
convert(‘my_score.musicxml’, ‘my_score.mid’)

### File to bytes with specified format

midi_bytes = convert(‘my_score.musicxml’, dest_format=’midi’)

### File to bytes using format string shorthand

midi_bytes = convert(‘my_score.musicxml’, ‘midi’)

### Bytes to file

convert(midi_bytes, ‘output.wav’, src_format=’midi’)

### Bytes to bytes

wav_bytes = convert(midi_bytes, src_format=’midi’, dest_format=’wav’)

### Bytes to bytes with format string shorthand

wav_bytes = convert(midi_bytes, ‘wav’, src_format=’midi’)

### tonal.midi_to_wav(midi_file, output_wav=None, , soundfont='/home/runner/work/tonal/tonal/tonal/data/Caeds Small Trash GM v1.06.sf2')

Synthesize audio from a MIDI file using FluidSynth.

* **Parameters:**
  * **midi_file** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of the input MIDI file.
  * **output_wav** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of the output WAV file.
  * **soundfont** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to the SoundFont file.

### tonal.scale_midi_notes(scale='C major', midi_range=(0, 127), , default_root='C')

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

### Modules

| [`chords`](tonal.chords.html.md#module-tonal.chords)             | Tools for chords and chord progressions.   |
|-----------------------------------------------------------------------------------------|--------------------------------------------|
| [`converters`](tonal.converters.html.md#module-tonal.converters)     | Convert music into various formats.        |
| [`notes`](tonal.notes.html.md#module-tonal.notes)               | Notes, scales, and chords definitions.     |
| [`util`](tonal.util.html.md#module-tonal.util)                 | Utils for sonification.                    |
| [`counterpoint`](tonal.counterpoint.html.md#module-tonal.counterpoint) | Tools for counterpoint.                    |
