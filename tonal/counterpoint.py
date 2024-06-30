"""
Tools for counterpoint.

The `translate_in_scale` allows you to translate a sequence of notes, or multiple 
tracks of notes by the given number of steps within the given scale.

>>> stream = translate_in_scale(['C4', 'E4', 'B3', 'C4'], -2, 'C')
>>> stream  # doctest: +ELLIPSIS
<music21.stream.Stream ...>
>>> note_names(stream)
['A3', 'C4', 'G3', 'A3']

For multiple tracks:

>>> tracks = [['C4', 'E4', 'G4'], ['A4', 'C5', 'E5']]
>>> translated_tracks = translate_in_scale(tracks, -2, 'C')
>>> multi_note_names(translated_tracks)
[['A3', 'C4', 'E4'], ['F4', 'A4', 'C5']]

Using some other scales:

With a E major scale:

>>> tracks = [['E4', 'G#4', 'B4'], ['C#5', 'E5', 'G#5']]
>>> translated_tracks = translate_in_scale(tracks, 1, 'E')
>>> multi_note_names(translated_tracks)
[['F#4', 'A4', 'C#5'], ['D#5', 'F#5', 'A5']]

With a D flat major scale:

>>> tracks = [['Db4', 'F4', 'Ab4'], ['Bb4', 'Db5', 'F5']]
>>> translated_tracks = translate_in_scale(tracks, -3, 'Db')
>>> multi_note_names(translated_tracks)
[['A-3', 'C4', 'E-4'], ['F4', 'A-4', 'C5']]

Now let's use a different, "custom" scale, as well as demonstrate the use
of a partial function to get a translator with a fixed input scale:

>>> from functools import partial
>>> from music21.scale import HarmonicMinorScale
>>> translate = partial(
...     translate_in_scale, input_scale='A', scale_creator=HarmonicMinorScale
... )
>>> tracks = [['A4', 'C5', 'E5'], ['G#5', 'A5', 'C6']]
>>> translated_tracks = translate(tracks, 2)
>>> multi_note_names(translated_tracks)
[['C5', 'E5', 'G#5'], ['B5', 'C6', 'E6']]
"""

from typing import Callable, Iterable, List, Union, Generator
from music21.scale import Scale, MajorScale
from music21.stream import Stream, Score, Part
from music21.note import Note
from operator import attrgetter

NoteString = str
NoteSpec = Union[NoteString, Note]
NotesSpec = Iterable[NoteSpec]
TrackSpec = Union[Stream, NotesSpec]
TracksSpec = List[TrackSpec]
ScaleCreator = Callable[[str], Scale]


def ensure_scale(
    input_scale: Union[str, Scale], scale_creator: ScaleCreator = MajorScale
) -> Scale:
    """
    Ensures the input is a Scale object. Converts a string to a Scale using the provided scale creator.

    Args:
        input_scale (Union[str, Scale]): The input scale.
        scale_creator (Callable[[str], Scale]): A function to create a Scale from a string.

    Returns:
        Scale: The corresponding Scale object.

    Raises:
        AssertionError: If the input cannot be converted to a Scale.
    """
    if isinstance(input_scale, str):
        input_scale = scale_creator(input_scale)
    assert isinstance(
        input_scale, Scale
    ), f"The input scale must be a music21.scale.Scale object: {input_scale=}"
    return input_scale


def get_scale_notes(input_note: Note, input_scale: Scale) -> List[str]:
    """
    Returns the names of the pitches in the scale within one octave around the input note.

    Args:
        input_note (Note): The input note.
        input_scale (Scale): The scale in which to find the pitches.

    Returns:
        List[str]: A list of pitch names within the scale.
    """
    scale_notes = input_scale.getPitches(
        input_note.pitch.transpose(-12), input_note.pitch.transpose(12)
    )
    return [p.nameWithOctave for p in scale_notes]


from music21.scale import (
    HarmonicMinorScale,
)  # Add this import at the top of your module


def _translate_note_in_scale(
    input_note: NoteString,
    translation: int,
    input_scale: Union[str, Scale],
    *,
    scale_creator: ScaleCreator = MajorScale,
) -> str:
    """
    Translates the input note by the given number of steps within the given scale.

    Args:
        input_note (str): The input note (e.g., 'C4', 'D#5').
        translation (int): The number of steps to translate the note.
        input_scale (Union[str, Scale]): The scale in which to perform the translation.
        scale_creator (ScaleCreator): A function to create a Scale from a string.

    Returns:
        str: The translated note.

    Raises:
        ValueError: If the input note is not in the specified scale.

    Examples:
        >>> _translate_note_in_scale('C4', 0, 'C')
        'C4'
        >>> _translate_note_in_scale('E4', -2, 'C')
        'C4'
        >>> _translate_note_in_scale('B4', 3, 'C')
        'E5'

        Use the E major scale
        >>> _translate_note_in_scale('E4', 1, 'E')
        'F#4'
        >>> _translate_note_in_scale('G#4', -1, 'E')
        'F#4'
        >>> _translate_note_in_scale('B4', 2, 'E')
        'D#5'

        Use the D flat major scale
        >>> _translate_note_in_scale('Db4', -1, 'Db')
        'C4'
        >>> _translate_note_in_scale('F4', 2, 'Db')
        'A-4'
        >>> _translate_note_in_scale('Ab4', -3, 'Db')
        'E-4'

        Now let's use a different, "custom" scale, as well as demonstrate the use
        of a partial function to get a translator with a fixed input scale:

        >>> from functools import partial
        >>> from music21.scale import HarmonicMinorScale
        >>> translate = partial(
        ...     _translate_note_in_scale, input_scale='A', scale_creator=HarmonicMinorScale
        ... )
        >>> translate('A4', 2)
        'C5'
        >>> translate('C5', -2)
        'A4'
        >>> translate('C5', 4)
        'G#5'
        >>> translate('G#5', 1)
        'A5'
    """
    n = Note(input_note)
    input_scale = ensure_scale(input_scale, scale_creator)
    scale_pitch_names = get_scale_notes(n, input_scale)

    # Find the index of the input note in the scale
    try:
        index = scale_pitch_names.index(n.nameWithOctave)
    except ValueError:
        raise ValueError("The input note is not in the specified scale.")

    # Calculate the new index with wrap around
    new_index = (index + translation) % len(scale_pitch_names)

    return scale_pitch_names[new_index]


def ensure_iterable_of_notes(notes: TrackSpec) -> Generator[Note, None, None]:
    """
    Ensures the input is an iterable of Note objects.

    Args:
        notes (TrackSpec): The input notes.

    Returns:
        Generator[Note, None, None]: A generator of Note objects.
    """
    if isinstance(notes, Stream):
        return (n for n in notes.notes)

    def _notes():
        for n in notes:
            if isinstance(n, str):
                n = Note(n)
            yield n

    return _notes()


def note_names(notes: TrackSpec) -> List[str]:
    """
    Returns the names of the notes in the input iterable.

    Args:
        notes (TrackSpec): The input notes.

    Returns:
        List[str]: A list of note names.

    Examples:
        >>> note_names(['C4', 'E4', 'G4'])
        ['C4', 'E4', 'G4']
        >>> s = Stream([Note('C4'), Note('E4'), Note('G4')])
        >>> note_names(s)
        ['C4', 'E4', 'G4']
    """
    return list(map(attrgetter('nameWithOctave'), ensure_iterable_of_notes(notes)))


def translate_notes_in_scale(
    input_notes: TrackSpec,
    translation: int,
    input_scale: Union[str, Scale],
    *,
    scale_creator: ScaleCreator = MajorScale,
) -> Stream:
    """
    Translates a sequence of notes by the given number of steps within the given scale.

    Args:
        input_notes (TrackSpec): The input notes.
        translation (int): The number of steps to translate the notes.
        input_scale (Union[str, Scale]): The scale in which to perform the translation.
        scale_creator (ScaleCreator): A function to create a Scale from a string.

    Returns:
        Stream: A stream of translated notes.

    Examples:
        >>> result_stream = translate_notes_in_scale(['C4', 'E4', 'B3', 'C4'], -2, 'C')
        >>> note_names(result_stream)
        ['A3', 'C4', 'G3', 'A3']
    """
    input_notes = ensure_iterable_of_notes(input_notes)
    return Stream(
        [
            Note(
                _translate_note_in_scale(
                    n.nameWithOctave,
                    translation,
                    input_scale,
                    scale_creator=scale_creator,
                )
            )
            for n in input_notes
        ]
    )


def translate_in_scale(
    tracks: Union[TrackSpec, TracksSpec],
    translation: int,
    input_scale: Union[str, Scale],
    *,
    scale_creator: ScaleCreator = MajorScale,
) -> Union[Stream, List[Stream]]:
    """
    Translates the input notes or tracks by the given number of steps within the given scale.

    Args:
        tracks (Union[TrackSpec, TracksSpec]): The input notes or tracks.
        translation (int): The number of steps to translate the notes.
        input_scale (Union[str, Scale]): The scale in which to perform the translation.
        scale_creator (ScaleCreator): A function to create a Scale from a string.

    Returns:
        Union[Stream, List[Stream]]: A stream of translated notes or a list of streams of translated notes.

    Examples:
        For a single track of notes:

        >>> stream = translate_in_scale(['C4', 'E4', 'B3', 'C4'], -2, 'C')
        >>> stream  # doctest: +ELLIPSIS
        <music21.stream.Stream ...>
        >>> note_names(stream)
        ['A3', 'C4', 'G3', 'A3']

        For multiple tracks:

        >>> tracks = [['C4', 'E4', 'G4'], ['A4', 'C5', 'E5']]
        >>> translated_tracks = translate_in_scale(tracks, -2, 'C')
        >>> multi_note_names(translated_tracks)
        [['A3', 'C4', 'E4'], ['F4', 'A4', 'C5']]

        Using some other scales:

        With a E major scale:

        >>> tracks = [['E4', 'G#4', 'B4'], ['C#5', 'E5', 'G#5']]
        >>> translated_tracks = translate_in_scale(tracks, 1, 'E')
        >>> multi_note_names(translated_tracks)
        [['F#4', 'A4', 'C#5'], ['D#5', 'F#5', 'A5']]

        With a D flat major scale:

        >>> tracks = [['Db4', 'F4', 'Ab4'], ['Bb4', 'Db5', 'F5']]
        >>> translated_tracks = translate_in_scale(tracks, -3, 'Db')
        >>> multi_note_names(translated_tracks)
        [['A-3', 'C4', 'E-4'], ['F4', 'A-4', 'C5']]

        Now let's use a different, "custom" scale, as well as demonstrate the use
        of a partial function to get a translator with a fixed input scale:

        >>> from functools import partial
        >>> from music21.scale import HarmonicMinorScale
        >>> translate = partial(
        ...     translate_in_scale, input_scale='A', scale_creator=HarmonicMinorScale
        ... )
        >>> tracks = [['A4', 'C5', 'E5'], ['G#5', 'A5', 'C6']]
        >>> translated_tracks = translate(tracks, 2)
        >>> multi_note_names(translated_tracks)
        [['C5', 'E5', 'G#5'], ['B5', 'C6', 'E6']]
    """
    if isinstance(tracks, list) and all(
        isinstance(item, (list, Stream)) for item in tracks
    ):
        translated_tracks = [
            translate_notes_in_scale(
                track, translation, input_scale, scale_creator=scale_creator
            )
            for track in tracks
        ]
        return translated_tracks
    else:
        if isinstance(tracks, (str, Note)):
            tracks = [tracks]  # in case it's just a single note
        return translate_notes_in_scale(
            tracks, translation, input_scale, scale_creator=scale_creator
        )


def create_score_from_tracks(tracks: List[Stream]) -> Score:
    """
    Creates a music21 Score from a list of tracks (Stream objects).

    Args:
        tracks (List[Stream]): A list of Stream objects, each representing a track (voice).

    Returns:
        Score: A Score object containing the tracks as separate parts.

    Examples:
        >>> stream1 = Stream([Note('C4'), Note('E4'), Note('G4')])
        >>> stream2 = Stream([Note('A4'), Note('C5'), Note('E5')])
        >>> score = create_score_from_tracks([stream1, stream2])
        >>> len(score.parts)
        2
    """
    score = Score()
    for track in tracks:
        part = Part()
        for element in track:
            part.append(element)
        score.append(part)
    return score


def multi_note_names(tracks: TracksSpec) -> List[List[NoteString]]:
    """
    Returns the names of the notes in the input iterable.

    Args:
        tracks (TracksSpec): The input tracks.

    Returns:
        List[List[NoteString]]: A list of lists of note names.

    Examples:
        >>> tracks = [['C4', 'E4', 'G4'], ['A4', 'C5', 'E5']]
        >>> multi_note_names(tracks)
        [['C4', 'E4', 'G4'], ['A4', 'C5', 'E5']]
        >>> stream1 = Stream([Note('C4'), Note('E4'), Note('G4')])
        >>> stream2 = Stream([Note('A4'), Note('C5'), Note('E5')])
        >>> multi_note_names([stream1, stream2])
        [['C4', 'E4', 'G4'], ['A4', 'C5', 'E5']]
    """
    return [note_names(track) for track in tracks]


__import__('doctest').testmod()
