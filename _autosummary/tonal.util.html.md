# tonal.util

Utils for sonification.

### Functions

| `add_pattern_aliases`(quality_extensions)                                                          |                                                                                        |
|----------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| [`add_streams`](#tonal.util.add_streams)(list_of_streams)                      | Concatenates multiple streams into a single stream.                                    |
| [`concatenate_streams`](#tonal.util.concatenate_streams)(streams_list)                 | Concatenates corresponding streams from a list of lists of streams.                    |
| [`create_score_from_tracks`](#tonal.util.create_score_from_tracks)(tracks)                  | Creates a music21 Score from a list of tracks (Stream objects).                        |
| [`delete_parts`](#tonal.util.delete_parts)(part_idx, score_input, \*[, ...])    | Delete parts from a score based on the provided part indices.                          |
| [`ensure_iterable_of_notes`](#tonal.util.ensure_iterable_of_notes)(notes[, str_to_note])    | Ensures the input is an iterable of Note objects.                                      |
| `ensure_part_filter`(part_filter)                                                                  |                                                                                        |
| [`ensure_scale`](#tonal.util.ensure_scale)(input_scale[, scale_creator])        | Ensures the input is a Scale object.                                                   |
| [`filter_parts`](#tonal.util.filter_parts)(part_filter, score_input, \*[, ...]) | Filter parts from a score based on the provided filter function or part indices.       |
| [`get_scale_notes`](#tonal.util.get_scale_notes)(input_note, input_scale)          | Returns the names of the pitches in the scale within one octave around the input note. |
| `identity_func`(x)                                                                                 |                                                                                        |
| [`is_existing_filepath`](#tonal.util.is_existing_filepath)(obj)                         | Returns True if the input object is a string representing an existing file path.       |
| [`mk_score`](#tonal.util.mk_score)(obj, \*\*kwargs)                         | Creates a music21 Score object from the input object.                                  |
| [`mk_stream`](#tonal.util.mk_stream)(obj, \*\*kwargs)                        | Creates a music21 Stream object from the input object.                                 |
| [`multi_note_names`](#tonal.util.multi_note_names)(tracks)                          | Returns the names of the notes in the input iterable.                                  |
| [`note_names`](#tonal.util.note_names)(notes[, name_attr])                    | Returns the names of the notes in the input iterable.                                  |
| `parse_note_name`(note_str)                                                                        |                                                                                        |
| [`play_music21_object`](#tonal.util.play_music21_object)(music21_obj)                  | Plays a music21 object (Chord, Part, Stream, etc.) using the StreamPlayer.             |
| [`resolve_format_from_filepath`](#tonal.util.resolve_format_from_filepath)(filepath)            | Resolves the format of a file from the file extension.                                 |
| [`string_to_note`](#tonal.util.string_to_note)([note_or_notes, egress])           | Converts a string representation of a note to a music21 Note object.                   |

### tonal.util.add_streams(list_of_streams)

Concatenates multiple streams into a single stream.

* **Parameters:**
  **list_of_streams** ([`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[`Stream`]) – The list of streams to concatenate.
* **Returns:**
  A single stream containing all the concatenated streams.
* **Return type:**
  `Stream`

### Examples

```pycon
>>> s1 = Stream([Note('C4'), Note('E4'), Note('G4')])
>>> s2 = Stream([Note('A4'), Note('C5'), Note('E5')])
>>> result_stream = add_streams([s1, s2])
>>> note_names(result_stream)
['C4', 'E4', 'G4', 'A4', 'C5', 'E5']
```

### tonal.util.concatenate_streams(streams_list)

Concatenates corresponding streams from a list of lists of streams.

* **Parameters:**
  **streams_list** ([`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[`Stream`]]) – The list of lists of streams to concatenate.
* **Returns:**
  A list of concatenated streams.
* **Return type:**
  [`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[`Stream`]

### Examples

```pycon
>>> s11 = Stream([Note('C4'), Note('E4')])
>>> s12 = Stream([Note('G4')])
>>> s21 = Stream([Note('A4')])
>>> s22 = Stream([Note('C5'), Note('E5')])
>>> result_streams = concatenate_streams([[s11, s12], [s21, s22]])
>>> len(result_streams)
2
>>> note_names(result_streams[0])
['C4', 'E4', 'A4']
>>> note_names(result_streams[1])
['G4', 'C5', 'E5']
```

### tonal.util.create_score_from_tracks(tracks)

Creates a music21 Score from a list of tracks (Stream objects).

* **Parameters:**
  **tracks** ([`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[`Stream`]) – A list of Stream objects, each representing a track (voice).
* **Returns:**
  A Score object containing the tracks as separate parts.
* **Return type:**
  `Score`

### Examples

```pycon
>>> stream1 = Stream([Note('C4'), Note('E4'), Note('G4')])
>>> stream2 = Stream([Note('A4'), Note('C5'), Note('E5')])
>>> score = create_score_from_tracks([stream1, stream2])
>>> len(score.parts)
2
```

### tonal.util.delete_parts(part_idx, score_input, , save_to_filepath=None)

Delete parts from a score based on the provided part indices.

* **Parameters:**
  * **part_idx** (`Union`[[`int`](https://docs.python.org/3/builtins/functions.html#int), [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]]) – Union[int, List[int]]
    An integer or a list of integers representing the indices of parts to be deleted.
  * **score_input** (`Union`[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), `Score`]) – Union[str, Score]
    The input score, either as a file path or a music21 Score instance.
  * **save_to_filepath** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – str
    The file path to save the modified score. Default is None.
* **Returns:**
  The score with specified parts deleted.
* **Return type:**
  `Score`

### Examples

```pycon
>>> score = mk_score([['C4'], ['D4'], ['E4']])
>>> modified_score = delete_parts([1], score)
>>> note_names(modified_score)
[['C4'], ['E4']]
>>> modified_score = delete_parts([0, 2], score)
>>> note_names(modified_score)
[['D4']]
```

### tonal.util.ensure_iterable_of_notes(notes, str_to_note=<class 'music21.note.Note'>)

Ensures the input is an iterable of Note objects.

* **Parameters:**
  **notes** (`Union`[`Stream`, [`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[`Union`[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), `Note`]]]) – The input notes.
* **Returns:**
  A generator of Note objects.
* **Return type:**
  [`Generator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Generator)[`Note`, [`None`](https://docs.python.org/3/builtins/constants.html#None), [`None`](https://docs.python.org/3/builtins/constants.html#None)]

### Examples

```pycon
>>> list(ensure_iterable_of_notes(['C4', 'E4', 'G4']))
[<music21.note.Note C>, <music21.note.Note E>, <music21.note.Note G>]
>>> s = Stream([Note('C4'), Note('E4'), Note('G4')])
>>> list(ensure_iterable_of_notes(s))
[<music21.note.Note C>, <music21.note.Note E>, <music21.note.Note G>]
```

### tonal.util.ensure_scale(input_scale, scale_creator=<class 'music21.scale.MajorScale'>)

Ensures the input is a Scale object. Converts a string to a Scale using the provided scale creator.

* **Parameters:**
  * **input_scale** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str) | `Scale`) – The input scale.
  * **scale_creator** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)], `Scale`]) – A function to create a Scale from a string.
* **Returns:**
  The corresponding Scale object.
* **Return type:**
  `Scale`
* **Raises:**
  [**AssertionError**](https://docs.python.org/3/builtins/exceptions.html#AssertionError) – If the input cannot be converted to a Scale.

### tonal.util.filter_parts(part_filter, score_input, , save_to_filepath=None)

Filter parts from a score based on the provided filter function or part indices.

* **Parameters:**
  * **part_filter** (`Union`[[`int`](https://docs.python.org/3/builtins/functions.html#int), [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`int`](https://docs.python.org/3/builtins/functions.html#int)], [`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[`Part`], [`bool`](https://docs.python.org/3/builtins/functions.html#bool)], [`None`](https://docs.python.org/3/builtins/constants.html#None)]) – PartFilterSpec
    A function that takes a music21 Part object and returns a boolean value.
    If an integer or list of integers is provided, the function will filter in
    parts based on the indices.
  * **score_input** (`Union`[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), `Score`]) – Union[str, Score]
    The input score, either as a file path or a music21 Score instance.
  * **save_to_filepath** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – str
    The file path to save the modified score. Default is None.
* **Returns:**
  The score with the subset of parts that were filtered in.
* **Return type:**
  `Score`

```pycon
>>> s = mk_score([['C4'], ['D4'], ['E4']])
>>> # Test filtering by index
>>> filtered_score = filter_parts([0, 2], s)
>>> note_names(filtered_score)
[['C4'], ['E4']]
>>> # Test filtering by function
>>> filtered_score = filter_parts(lambda i, part: part.notes[0].name != 'D', s)
>>> note_names(filtered_score)
[['C4'], ['E4']]
>>> # Test no filtering (return all parts)
>>> filtered_score = filter_parts(None, s)
>>> note_names(filtered_score)
[['C4'], ['D4'], ['E4']]
```

### tonal.util.get_scale_notes(input_note, input_scale)

Returns the names of the pitches in the scale within one octave around the input note.

* **Parameters:**
  * **input_note** (`Note`) – The input note.
  * **input_scale** (`Scale`) – The scale in which to find the pitches.
* **Returns:**
  A list of pitch names within the scale.
* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]

### tonal.util.is_existing_filepath(obj)

Returns True if the input object is a string representing an existing file path.

* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)

### tonal.util.mk_score(obj, \*\*kwargs)

Creates a music21 Score object from the input object.

* **Parameters:**
  * **obj** (`Union`[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), `Score`]) – The input object.
  * **\*\*kwargs** – Additional keyword arguments to pass to the Score constructor.
* **Returns:**
  The corresponding Score object.
* **Return type:**
  `Score`

```pycon
>>> score = mk_score([['C4 B4'], ['E4'], ['G4']])
>>> score.show('text')
{0.0} <music21.stream.Part 0x...>
    {0.0} <music21.note.Note C>
    {1.0} <music21.note.Note B>
{2.0} <music21.stream.Part 0x...>
    {0.0} <music21.note.Note E>
{3.0} <music21.stream.Part 0x...>
    {0.0} <music21.note.Note G>
```

### tonal.util.mk_stream(obj, \*\*kwargs)

Creates a music21 Stream object from the input object.

* **Parameters:**
  * **obj** (`Union`[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)], [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[`Note`], `Stream`]) – The input object.
  * **\*\*kwargs** – Additional keyword arguments to pass to the Stream constructor.
* **Returns:**
  The corresponding Stream object.
* **Return type:**
  `Stream`

```pycon
>>> stream = mk_stream('C4 E4 G4')
>>> note_names(stream)
['C4', 'E4', 'G4']
```

### tonal.util.multi_note_names(tracks)

Returns the names of the notes in the input iterable.

* **Parameters:**
  **tracks** ([`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[`Union`[`Stream`, [`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[`Union`[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), `Note`]]]]) – The input tracks.
* **Returns:**
  A list of lists of note names.
* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]

### Examples

```pycon
>>> tracks = [['C4', 'E4', 'G4'], ['A4', 'C5', 'E5']]
>>> multi_note_names(tracks)
[['C4', 'E4', 'G4'], ['A4', 'C5', 'E5']]
>>> stream1 = Stream([Note('C4'), Note('E4'), Note('G4')])
>>> stream2 = Stream([Note('A4'), Note('C5'), Note('E5')])
>>> multi_note_names([stream1, stream2])
[['C4', 'E4', 'G4'], ['A4', 'C5', 'E5']]
```

### tonal.util.note_names(notes, name_attr='nameWithOctave')

Returns the names of the notes in the input iterable.

* **Parameters:**
  **notes** (`Union`[`Stream`, [`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[`Union`[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), `Note`]]]) – The input notes.
* **Returns:**
  A list of note names.
* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]

### Examples

```pycon
>>> note_names(['C4', 'E4', 'G4'])
['C4', 'E4', 'G4']
>>> s = Stream([Note('C4'), Note('E4'), Note('G4')])
>>> note_names(s)
['C4', 'E4', 'G4']
>>> score = mk_score([['C4', 'E4', 'G4'], ['A4', 'C5', 'E5']])
>>> note_names(score)
[['C4', 'E4', 'G4'], ['A4', 'C5', 'E5']]
```

#### SEE ALSO
multi_note_names

### tonal.util.play_music21_object(music21_obj)

Plays a music21 object (Chord, Part, Stream, etc.) using the StreamPlayer.

* **Parameters:**
  **music21_obj** – A music21 object (Chord, Part, Stream, etc.) to be played.

### tonal.util.resolve_format_from_filepath(filepath)

Resolves the format of a file from the file extension.

* **Parameters:**
  **filepath** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – The file path.
* **Returns:**
  The format of the file.
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

### Examples

```pycon
>>> resolve_format_from_filepath('output.mid')
'mid'
>>> resolve_format_from_filepath('output.wav')
'wav'
```

### tonal.util.string_to_note(note_or_notes=None, egress=<class 'list'>, \*\*note_kwargs)

Converts a string representation of a note to a music21 Note object.

* **Parameters:**
  **note_or_notes** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str) | [`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)] | [`None`](https://docs.python.org/3/builtins/constants.html#None)) – String representation of the note(s).
* **Returns:**
  The music21 Note object.
* **Return type:**
  `Note`

### Examples

```pycon
>>> string_to_note('C4')
<music21.note.Note C>
```

If you don’t specify a string (only keyword arguments), you get a partial
function. This is especially useful when you want to convert multiple strings.
Note also, in the example below, that the function is applied to a list of
strings.

```pycon
>>> my_str_to_note = string_to_note(quarterLength=2, microtone=50)
>>> notes = list(my_str_to_note(['C4', 'D4', 'E4']))
>>> note = notes[-1]
>>> print(f"{note.nameWithOctave=}, {note.duration.type=}, {note.pitch.microtone=}")
note.nameWithOctave='E4', note.duration.type='half', note.pitch.microtone=<music21.pitch.Microtone (+50c)>
```
