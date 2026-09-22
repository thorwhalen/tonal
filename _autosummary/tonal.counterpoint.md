# tonal.counterpoint

Tools for counterpoint.

The `translate_in_scale` allows you to translate a sequence of notes, or multiple
tracks of notes by the given number of steps within the given scale.

```pycon
>>> stream = translate_in_scale(['C4', 'E4', 'B3', 'C4'], -2, 'C')
>>> stream
<music21.stream.Stream ...>
>>> note_names(stream)
['A3', 'C4', 'G3', 'A3']
```

For multiple tracks:

```pycon
>>> motif = [['C4', 'E4', 'G4'], ['A4', 'C5', 'E5']]
>>> translated_tracks = translate_in_scale(motif, -2, 'C')
>>> multi_note_names(translated_tracks)
[['A3', 'C4', 'E4'], ['F4', 'A4', 'C5']]
```

Using some other scales:

With a E major scale:

```pycon
>>> motif = [['E4', 'G#4', 'B4'], ['C#5', 'E5', 'G#5']]
>>> translated_tracks = translate_in_scale(motif, 1, 'E')
>>> multi_note_names(translated_tracks)
[['F#4', 'A4', 'C#5'], ['D#5', 'F#5', 'A5']]
```

With a D flat major scale:

```pycon
>>> motif = [['Db4', 'F4', 'Ab4'], ['Bb4', 'Db5', 'F5']]
>>> translated_tracks = translate_in_scale(motif, -3, 'Db')
>>> multi_note_names(translated_tracks)
[['A-3', 'C4', 'E-4'], ['F4', 'A-4', 'C5']]
```

Now let’s use a different, “custom” scale, as well as demonstrate the use
of a partial function to get a translator with a fixed input scale:

```pycon
>>> from functools import partial
>>> from music21.scale import HarmonicMinorScale
>>> translate = partial(
...     translate_in_scale, input_scale='A', scale_creator=HarmonicMinorScale
... )
>>> motif = [['A4', 'C5', 'E5'], ['G#5', 'A5', 'C6']]
>>> translated_tracks = translate(motif, 2)
>>> multi_note_names(translated_tracks)
[['C5', 'E5', 'G#5'], ['B5', 'C6', 'E6']]
```

### Functions

| [`translate_in_scale`](#tonal.counterpoint.translate_in_scale)(motif, translation, ...)       | Translates the input notes or tracks by the given number of steps within the given scale.   |
|----------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| [`translate_notes_in_scale`](#tonal.counterpoint.translate_notes_in_scale)(input_notes, ...[, ...]) | Translates a sequence of notes by the given number of steps within the given scale.         |

### tonal.counterpoint.translate_in_scale(motif, translation, input_scale, \*, scale_creator=<class 'music21.scale.MajorScale'>)

Translates the input notes or tracks by the given number of steps within the given scale.

* **Parameters:**
  * **motif** (`Union`[`Stream`, [`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[`Union`[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), `Note`]], [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[`Union`[`Stream`, [`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[`Union`[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), `Note`]]]]]) – The motif; input notes or tracks.
  * **translation** ([`int`](https://docs.python.org/3/builtins/functions.html#int) | [`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]) – The number of steps to translate the notes.
  * **input_scale** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str) | `Scale`) – The scale in which to perform the translation.
  * **scale_creator** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)], `Scale`]) – A function to create a Scale from a string.
* **Returns:**
  A stream of translated notes or a list of streams of translated notes.
* **Return type:**
  `Stream` | [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[`Stream`]

### Examples

For a single track of notes:

```pycon
>>> stream = translate_in_scale(['C4', 'E4', 'B3', 'C4'], -2, 'C')
>>> stream
<music21.stream.Stream ...>
>>> note_names(stream)
['A3', 'C4', 'G3', 'A3']
```

For multiple tracks:

```pycon
>>> motif = [['C4', 'E4', 'G4'], ['A4', 'C5', 'E5']]
>>> translated_tracks = translate_in_scale(motif, -2, 'C')
>>> multi_note_names(translated_tracks)
[['A3', 'C4', 'E4'], ['F4', 'A4', 'C5']]
```

Using some other scales:

With a E major scale, and two translations:

```pycon
>>> motif = [['E4', 'G#4', 'B4'], ['C#5', 'E5', 'G#5']]
>>> translated_tracks = translate_in_scale(motif, [1, 2], 'E')
>>> multi_note_names(translated_tracks)
[['F#4', 'A4', 'C#5', 'G#4', 'B4', 'D#5'],
['D#5', 'F#5', 'A5', 'E5', 'G#5', 'B5']]
```

With a D flat major scale:

```pycon
>>> motif = [['Db4', 'F4', 'Ab4'], ['Bb4', 'Db5', 'F5']]
>>> translated_tracks = translate_in_scale(motif, -3, 'Db')
>>> multi_note_names(translated_tracks)
[['A-3', 'C4', 'E-4'], ['F4', 'A-4', 'C5']]
```

Now let’s use a different, “custom” scale, as well as demonstrate the use
of a partial function to get a translator with a fixed input scale:

```pycon
>>> from functools import partial
>>> from music21.scale import HarmonicMinorScale
>>> translate = partial(
...     translate_in_scale, input_scale='A', scale_creator=HarmonicMinorScale
... )
>>> motif = [['A4', 'C5', 'E5'], ['G#5', 'A5', 'C6']]
>>> translated_tracks = translate(motif, 2)
>>> multi_note_names(translated_tracks)
[['C5', 'E5', 'G#5'], ['B5', 'C6', 'E6']]
```

### tonal.counterpoint.translate_notes_in_scale(input_notes, translation, input_scale, \*, scale_creator=<class 'music21.scale.MajorScale'>)

Translates a sequence of notes by the given number of steps within the given scale.

* **Parameters:**
  * **input_notes** (`Union`[`Stream`, [`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[`Union`[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), `Note`]]]) – The input notes.
  * **translation** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – The number of steps to translate the notes.
  * **input_scale** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str) | `Scale`) – The scale in which to perform the translation.
  * **scale_creator** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)], `Scale`]) – A function to create a Scale from a string.
* **Returns:**
  A stream of translated notes.
* **Return type:**
  `Stream`

### Examples

```pycon
>>> result_stream = translate_notes_in_scale(['C4', 'E4', 'B3', 'C4'], -2, 'C')
>>> note_names(result_stream)
['A3', 'C4', 'G3', 'A3']
```
