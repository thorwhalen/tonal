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

>>> motif = [['C4', 'E4', 'G4'], ['A4', 'C5', 'E5']]
>>> translated_tracks = translate_in_scale(motif, -2, 'C')
>>> multi_note_names(translated_tracks)
[['A3', 'C4', 'E4'], ['F4', 'A4', 'C5']]

Using some other scales:

With a E major scale:

>>> motif = [['E4', 'G#4', 'B4'], ['C#5', 'E5', 'G#5']]
>>> translated_tracks = translate_in_scale(motif, 1, 'E')
>>> multi_note_names(translated_tracks)
[['F#4', 'A4', 'C#5'], ['D#5', 'F#5', 'A5']]

With a D flat major scale:

>>> motif = [['Db4', 'F4', 'Ab4'], ['Bb4', 'Db5', 'F5']]
>>> translated_tracks = translate_in_scale(motif, -3, 'Db')
>>> multi_note_names(translated_tracks)
[['A-3', 'C4', 'E-4'], ['F4', 'A-4', 'C5']]

Now let's use a different, "custom" scale, as well as demonstrate the use
of a partial function to get a translator with a fixed input scale:

>>> from functools import partial
>>> from music21.scale import HarmonicMinorScale
>>> translate = partial(
...     translate_in_scale, input_scale='A', scale_creator=HarmonicMinorScale
... )
>>> motif = [['A4', 'C5', 'E5'], ['G#5', 'A5', 'C6']]
>>> translated_tracks = translate(motif, 2)
>>> multi_note_names(translated_tracks)
[['C5', 'E5', 'G#5'], ['B5', 'C6', 'E6']]
"""

from typing import List, Union, Iterable
from music21.scale import Scale, MajorScale
from music21.stream import Stream
from music21.note import Note
from tonal.util import (
    NoteString,
    TrackSpec,
    TracksSpec,
    ScaleCreator,
    note_names,
    multi_note_names,
    get_scale_notes,
    ensure_scale,
    ensure_iterable_of_notes,
    concatenate_streams,
)


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
    motif: Union[TrackSpec, TracksSpec],
    translation: Union[int, Iterable[int]],
    input_scale: Union[str, Scale],
    *,
    scale_creator: ScaleCreator = MajorScale,
) -> Union[Stream, List[Stream]]:
    """
    Translates the input notes or tracks by the given number of steps within the given scale.

    Args:
        motif (Union[TrackSpec, TracksSpec]): The motif; input notes or tracks.
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

        >>> motif = [['C4', 'E4', 'G4'], ['A4', 'C5', 'E5']]
        >>> translated_tracks = translate_in_scale(motif, -2, 'C')
        >>> multi_note_names(translated_tracks)
        [['A3', 'C4', 'E4'], ['F4', 'A4', 'C5']]

        Using some other scales:

        With a E major scale, and two translations:

        >>> motif = [['E4', 'G#4', 'B4'], ['C#5', 'E5', 'G#5']]
        >>> translated_tracks = translate_in_scale(motif, [1, 2], 'E')
        >>> multi_note_names(translated_tracks)  # doctest: +NORMALIZE_WHITESPACE
        [['F#4', 'A4', 'C#5', 'G#4', 'B4', 'D#5'],
        ['D#5', 'F#5', 'A5', 'E5', 'G#5', 'B5']]

        With a D flat major scale:

        >>> motif = [['Db4', 'F4', 'Ab4'], ['Bb4', 'Db5', 'F5']]
        >>> translated_tracks = translate_in_scale(motif, -3, 'Db')
        >>> multi_note_names(translated_tracks)
        [['A-3', 'C4', 'E-4'], ['F4', 'A-4', 'C5']]

        Now let's use a different, "custom" scale, as well as demonstrate the use
        of a partial function to get a translator with a fixed input scale:

        >>> from functools import partial
        >>> from music21.scale import HarmonicMinorScale
        >>> translate = partial(
        ...     translate_in_scale, input_scale='A', scale_creator=HarmonicMinorScale
        ... )
        >>> motif = [['A4', 'C5', 'E5'], ['G#5', 'A5', 'C6']]
        >>> translated_tracks = translate(motif, 2)
        >>> multi_note_names(translated_tracks)
        [['C5', 'E5', 'G#5'], ['B5', 'C6', 'E6']]
    """
    if isinstance(translation, Iterable):
        tracks_to_concatinate = [
            translate_in_scale(motif, t, input_scale, scale_creator=scale_creator)
            for t in translation
        ]
        return concatenate_streams(tracks_to_concatinate)

    else:
        if isinstance(motif, list) and all(
            isinstance(item, (list, Stream)) for item in motif
        ):
            translated_tracks = [
                translate_notes_in_scale(
                    track, translation, input_scale, scale_creator=scale_creator
                )
                for track in motif
            ]
            return translated_tracks
        else:
            if isinstance(motif, (str, Note)):
                motif = [motif]  # in case it's just a single note
            return translate_notes_in_scale(
                motif, translation, input_scale, scale_creator=scale_creator
            )
