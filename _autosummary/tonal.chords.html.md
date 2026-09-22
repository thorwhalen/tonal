# tonal.chords

Tools for chords and chord progressions.

### Functions

| [`chord_to_notes`](#tonal.chords.chord_to_notes)(chord)                         | Parse a chord string and return the corresponding sequence of MIDI note numbers.   |
|------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| [`chords_to_midi`](#tonal.chords.chords_to_midi)([chord_sequence, ...])         | Generate a MIDI file from a chord sequence.                                        |
| [`chords_to_wav`](#tonal.chords.chords_to_wav)([chord_sequence, name, ...])    | Generate a WAV file directly from a chord sequence.                                |
| `play_arpeggio`(notes, track, duration, \*[, ...])                                             |                                                                                    |
| `play_simultaneously`(notes, track, duration, \*)                                              |                                                                                    |
| [`process_chord_sequence`](#tonal.chords.process_chord_sequence)(chord_sequence[, ...]) | Preprocess a chord sequence, to make sure to add time, etc.                        |
| `register_chord_render`(chord_renderer[, name])                                                |                                                                                    |
| `resolve_chord_render`(chord_renderer)                                                         |                                                                                    |

### tonal.chords.chord_to_notes(chord)

Parse a chord string and return the corresponding sequence of MIDI note numbers.

* **Parameters:**
  **chord** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – The chord string (e.g., ‘Cmaj7’).
* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]
* **Returns:**
  A sequence of MIDI note numbers representing the chord.

### tonal.chords.chords_to_midi(chord_sequence=[('Bdim', 120), ('Em11', 120), ('Amin9', 120), ('Dm7', 120), 'G7', 'Cmaj7'], \*, output_file=None, render_chord=<function play_simultaneously>, chord_definitions=<function chord_to_notes>)

Generate a MIDI file from a chord sequence.

* **Parameters:**
  * **chord_sequence** ([`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]]]) – List of tuples containing chords and their duration.
  * **chord_definitions** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)], [`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]]) – Dictionary mapping chords to MIDI note patterns.
  * **output_file** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of the output MIDI file.
  * **render_chord** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[`int`](https://docs.python.org/3/builtins/functions.html#int)], `any`, [`int`](https://docs.python.org/3/builtins/functions.html#int)], [`None`](https://docs.python.org/3/builtins/constants.html#None)]) – Function defining how the chords should be played.

### tonal.chords.chords_to_wav(chord_sequence=[('Bdim', 120), ('Em11', 120), ('Amin9', 120), ('Dm7', 120), 'G7', 'Cmaj7'], name='audio_output', \*, chord_definitions=<function chord_to_notes>, soundfont='/home/runner/work/tonal/tonal/tonal/data/Caeds Small Trash GM v1.06.sf2', render_chord=<function play_simultaneously>)

Generate a WAV file directly from a chord sequence.

* **Parameters:**
  * **chord_sequence** ([`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]]]) – List of tuples containing chords and their duration.
  * **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Base name for the output MIDI and WAV files.
  * **chord_definitions** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)], [`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]]) – Dictionary mapping chords to MIDI note patterns.
  * **soundfont** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to the SoundFont file.
  * **render_chord** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[`int`](https://docs.python.org/3/builtins/functions.html#int)], `any`, [`int`](https://docs.python.org/3/builtins/functions.html#int)], [`None`](https://docs.python.org/3/builtins/constants.html#None)]) – Function defining how the chords should be played.

### tonal.chords.process_chord_sequence(chord_sequence, default_duration=960)

Preprocess a chord sequence, to make sure to add time, etc.
