"""Utils for sonification."""

# TODO: The big module (and even package) todo is to refactor everything to do with
#   the hierarchy of iterables (Score=I[Part]), Part=I[Measure], Measure=I[Note])
#   to be consistent.

import os
from typing import Callable
from importlib.resources import files
from functools import partial
from config2py import (
    process_path,
    simple_config_getter,
    get_app_data_folder,
)
from config2py.errors import ConfigNotFound

from dol import written_bytes


# from typing import Sequence, Callable, Tuple
# from music21.note import Note
# Chord = str
# Notes = Sequence[Note]
# ChordTimed = Tuple[Chord, Notes]
# ChordSequence = Sequence[ChordTimed]
# ChordDefinitions = Callable[[Chord], Notes]
# ChordRenderer = Callable[[Notes, any, int], None]

pkg_name = "tonal"

app_data_dir = process_path(get_app_data_folder("tonal"))
soundfonts_dir = process_path(
    os.path.join(app_data_dir, "soundfonts"), ensure_dir_exists=True
)

data_files = files(pkg_name) / "data"

get_config = simple_config_getter(pkg_name)


DFLT_OUTPUT_NAME = "audio_output"
DFLT_MIDI_OUTPUT = f"{DFLT_OUTPUT_NAME}.mid"
DFLT_WAV_OUTPUT = f"{DFLT_OUTPUT_NAME}.wav"

# TODO: The DFLT_SOUNDFONT is horribly unclean. Revise. config2py should have an easy default mechanism
try:
    DFLT_SOUNDFONT = process_path(
        get_config("TONAL_DFLT_SOUNDFONT_PATH"),
    )
except ConfigNotFound:
    # soundfont_url = "https://archive.org/download/free-soundfonts-sf2-2019-04/Arachno_SoundFont_Version_1.0.sf2" # 148.2 MB !!!
    # acquired from https://musical-artifacts.com/artifacts/2877/CT1MBGMRSV1.06.sf2
    DFLT_SOUNDFONT = str(data_files / "Caeds Small Trash GM v1.06.sf2")

from typing import (
    Callable,
    Iterable,
    List,
    Union,
    Generator,
    Optional,
    Container,
    Any,
    Sequence,
    Tuple,
    Mapping,
    Dict,
)
import os
from operator import attrgetter
import re

from music21.stream import Score, Stream, Part, Measure
from music21.midi.realtime import StreamPlayer
from music21.scale import Scale, MajorScale
from music21.note import Note
from music21 import converter


def identity_func(x):
    return x


def play_music21_object(music21_obj):
    """
    Plays a music21 object (Chord, Part, Stream, etc.) using the StreamPlayer.

    Args:
        music21_obj: A music21 object (Chord, Part, Stream, etc.) to be played.
    """
    if isinstance(music21_obj, Score):
        s = music21_obj
    else:
        # Create a Stream object
        s = Stream()
        # Add the music21 object to the Stream
        s.append(music21_obj)

    # Play the Stream using StreamPlayer
    sp = StreamPlayer(s)
    sp.play()


NoteString = str
NoteSpec = Union[NoteString, Note]
NotesSpec = Iterable[NoteSpec]
TrackSpec = Union[Stream, NotesSpec]
TracksSpec = List[TrackSpec]
ScaleCreator = Callable[[str], Scale]
StreamSpec = Union[str, Iterable[str], List[Note], Stream]
Streams = Iterable[Stream]

StrToNote = Callable[[str], Note]

Filepath = str
ScoreSpec = Union[Filepath, Score]
PartFilter = Callable[[Part], bool]
PartIdx = Union[int, List[int]]
PartFilterSpec = Optional[Union[PartIdx, PartFilter]]

# Regex for note names (e.g., C, C#, Db, etc.)
note_name_pattern = re.compile(r"([A-Ga-g][#b]?)")


def parse_note_name(note_str: str) -> str:
    match = note_name_pattern.match(note_str)
    if match:
        return match.group(1)
    else:
        raise ValueError(f"Invalid note string: {note_str}")


# General utility to add pattern-based aliases to a dictionary
def add_pattern_aliases(quality_extensions):
    for _qe in quality_extensions:
        if _qe.startswith("maj"):
            yield _qe.replace("maj", "M"), quality_extensions[_qe]
        elif _qe.startswith("min"):
            yield _qe.replace("min", "m"), quality_extensions[_qe]
        elif _qe.startswith("dim"):
            yield _qe.replace("dim", "°"), quality_extensions[_qe]


def string_to_note(
    note_or_notes: Optional[Union[NoteString, Iterable[NoteString]]] = None,
    egress: Callable = list,
    **note_kwargs,
) -> Note:
    """
    Converts a string representation of a note to a music21 Note object.

    Args:
        note_or_notes (str or iterable of str): String representation of the note(s).

    Returns:
        Note: The music21 Note object.

    Examples:
        >>> string_to_note('C4')
        <music21.note.Note C>

        If you don't specify a string (only keyword arguments), you get a partial
        function. This is especially useful when you want to convert multiple strings.
        Note also, in the example below, that the function is applied to a list of
        strings.

        >>> my_str_to_note = string_to_note(quarterLength=2, microtone=50)
        >>> notes = list(my_str_to_note(['C4', 'D4', 'E4']))
        >>> note = notes[-1]
        >>> print(f"{note.nameWithOctave=}, {note.duration.type=}, {note.pitch.microtone=}")
        note.nameWithOctave='E4', note.duration.type='half', note.pitch.microtone=<music21.pitch.Microtone (+50c)>

    """
    if note_or_notes is None:
        return partial(string_to_note, **note_kwargs, egress=egress)
    if isinstance(note_or_notes, str):
        return Note(note_or_notes, **note_kwargs)
    elif isinstance(note_or_notes, Iterable):
        return egress(map(partial(string_to_note, **note_kwargs), note_or_notes))


def is_existing_filepath(obj: Any) -> bool:
    """
    Returns True if the input object is a string representing an existing file path.
    """
    return isinstance(obj, str) and os.path.isfile(obj)


def mk_score(obj: ScoreSpec, **kwargs) -> Score:
    """
    Creates a music21 Score object from the input object.

    Args:
        obj (ScoreSpec): The input object.
        **kwargs: Additional keyword arguments to pass to the Score constructor.

    Returns:
        Score: The corresponding Score object.

    >>> score = mk_score([['C4 B4'], ['E4'], ['G4']])
    >>> score.show('text')  # doctest: +ELLIPSIS
    {0.0} <music21.stream.Part 0x...>
        {0.0} <music21.note.Note C>
        {1.0} <music21.note.Note B>
    {2.0} <music21.stream.Part 0x...>
        {0.0} <music21.note.Note E>
    {3.0} <music21.stream.Part 0x...>
        {0.0} <music21.note.Note G>
    """
    if is_existing_filepath(obj):
        return converter.parse(obj)
    if isinstance(obj, list) and obj:
        # assume we have a list of lists, i.e. we have multiple parts
        parts = obj
        score = Score(**kwargs)
        if not parts:  # empty list
            return score
        if not isinstance(obj[0], list):
            parts = [parts]
        for stream_spec in parts:
            part = Part()
            if isinstance(stream_spec, list):
                for note_spec in stream_spec:
                    for note_name in note_spec.split():
                        note = Note(note_name)
                        part.append(note)
            else:
                stream = mk_stream(stream_spec)
                part.append(stream)
            score.append(part)
        return score
    else:
        raise ValueError(f"Cannot create a Score from {obj=}")


def mk_stream(obj: StreamSpec, **kwargs) -> Stream:
    """
    Creates a music21 Stream object from the input object.

    Args:
        obj (StreamSpec): The input object.
        **kwargs: Additional keyword arguments to pass to the Stream constructor.

    Returns:
        Stream: The corresponding Stream object.

    >>> stream = mk_stream('C4 E4 G4')
    >>> note_names(stream)
    ['C4', 'E4', 'G4']
    """
    if isinstance(obj, list) and len(obj) == 1 and isinstance(obj[0], str):
        # if the list has a single string, assume it's a list of note names
        obj = obj[0]  # get the single string of the list (process it in the next step)
    if isinstance(obj, str):
        # first argument is a string, split into list of note names
        obj = obj.split()
    if isinstance(obj, list) and obj:
        if isinstance(obj[0], str):
            # first argument is a list of note names, convert to list of Note objs
            list_of_note_names = obj
            list_of_note_objs = [Note(n) for n in list_of_note_names]
            obj = list_of_note_objs

    return Stream(obj, **kwargs)


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
        input_note.pitch.transpose(-48), input_note.pitch.transpose(48)
    )
    return [p.nameWithOctave for p in scale_notes]


def ensure_iterable_of_notes(
    notes: TrackSpec, str_to_note: StrToNote = Note
) -> Generator[Note, None, None]:
    """
    Ensures the input is an iterable of Note objects.

    Args:
        notes (TrackSpec): The input notes.

    Returns:
        Generator[Note, None, None]: A generator of Note objects.

    Examples:

    >>> list(ensure_iterable_of_notes(['C4', 'E4', 'G4']))
    [<music21.note.Note C>, <music21.note.Note E>, <music21.note.Note G>]
    >>> s = Stream([Note('C4'), Note('E4'), Note('G4')])
    >>> list(ensure_iterable_of_notes(s))
    [<music21.note.Note C>, <music21.note.Note E>, <music21.note.Note G>]

    """
    if isinstance(notes, Stream):
        return (n for n in notes.notes)

    def _notes():
        for n in notes:
            if isinstance(n, str):
                n = str_to_note(n)
            yield n

    return _notes()


def note_names(notes: TrackSpec, name_attr="nameWithOctave") -> List[str]:
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
        >>> score = mk_score([['C4', 'E4', 'G4'], ['A4', 'C5', 'E5']])
        >>> note_names(score)
        [['C4', 'E4', 'G4'], ['A4', 'C5', 'E5']]

    See Also:
        multi_note_names

    """
    if isinstance(notes, Score):
        return list(map(partial(note_names, name_attr=name_attr), notes.parts))
    else:
        return list(map(attrgetter(name_attr), ensure_iterable_of_notes(notes)))


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


def add_streams(list_of_streams: Streams) -> Stream:
    """
    Concatenates multiple streams into a single stream.

    Args:
        list_of_streams (List[Stream]): The list of streams to concatenate.

    Returns:
        Stream: A single stream containing all the concatenated streams.

    Examples:

    >>> s1 = Stream([Note('C4'), Note('E4'), Note('G4')])
    >>> s2 = Stream([Note('A4'), Note('C5'), Note('E5')])
    >>> result_stream = add_streams([s1, s2])
    >>> note_names(result_stream)
    ['C4', 'E4', 'G4', 'A4', 'C5', 'E5']
    """
    combined_stream = Stream()
    for stream in list_of_streams:
        for element in stream:
            combined_stream.append(element)
    return combined_stream


def concatenate_streams(streams_list: List[Streams]) -> Streams:
    """
    Concatenates corresponding streams from a list of lists of streams.

    Args:
        streams_list (List[List[Stream]]): The list of lists of streams to concatenate.

    Returns:
        List[Stream]: A list of concatenated streams.

    Examples:
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
    """
    return list(map(add_streams, zip(*streams_list)))


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
    parts = [Part(iter(track)) for track in tracks]
    return Score(parts)


def ensure_part_filter(part_filter: PartFilterSpec) -> PartFilter:
    if isinstance(part_filter, int):
        part_filter = [part_filter]
    if isinstance(part_filter, Container):
        # make it into a PartFilter function
        desired_parts = part_filter
        part_filter = lambda i, part: i in desired_parts
    elif part_filter is None:
        part_filter = lambda i, part: True
    elif not callable(part_filter):
        raise TypeError(
            "part_filter must be an int, list of ints, a callable, or None."
            f"Was: {part_filter}"
        )
    return part_filter


def resolve_format_from_filepath(filepath: Filepath) -> str:
    """
    Resolves the format of a file from the file extension.

    Args:
        filepath (Filepath): The file path.

    Returns:
        str: The format of the file.

    Examples:
        >>> resolve_format_from_filepath('output.mid')
        'mid'
        >>> resolve_format_from_filepath('output.wav')
        'wav'
    """
    return os.path.splitext(filepath)[1][1:]


def filter_parts(
    part_filter: PartFilterSpec,
    score_input: ScoreSpec,
    *,
    save_to_filepath: Filepath = None,
) -> Score:
    """
    Filter parts from a score based on the provided filter function or part indices.

    Parameters:
        part_filter: PartFilterSpec
            A function that takes a music21 Part object and returns a boolean value.
            If an integer or list of integers is provided, the function will filter in
            parts based on the indices.
        score_input: Union[str, Score]
            The input score, either as a file path or a music21 Score instance.
        save_to_filepath: str
            The file path to save the modified score. Default is None.

    Returns:
        Score: The score with the subset of parts that were filtered in.

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
    """
    filter_func = ensure_part_filter(part_filter)

    # Load the score if a file path is provided
    if isinstance(score_input, str):
        score = converter.parse(score_input)
    else:
        score = score_input

    # Create a new score and add the remaining parts
    new_score = Score()
    for i, part in enumerate(score.parts):
        if filter_func(i, part):
            new_score.append(part)

    # Save the modified score if a file path is provided
    if save_to_filepath:
        # resolve the fmt from the file extension
        fmt = resolve_format_from_filepath(save_to_filepath)
        new_score.write(fmt=fmt, fp=save_to_filepath)

    return new_score


def delete_parts(
    part_idx: PartIdx, score_input: ScoreSpec, *, save_to_filepath: Filepath = None
) -> Score:
    """
    Delete parts from a score based on the provided part indices.

    Parameters:
        part_idx: Union[int, List[int]]
            An integer or a list of integers representing the indices of parts to be deleted.
        score_input: Union[str, Score]
            The input score, either as a file path or a music21 Score instance.
        save_to_filepath: str
            The file path to save the modified score. Default is None.

    Returns:
        Score: The score with specified parts deleted.

    Examples:
        >>> score = mk_score([['C4'], ['D4'], ['E4']])
        >>> modified_score = delete_parts([1], score)
        >>> note_names(modified_score)
        [['C4'], ['E4']]
        >>> modified_score = delete_parts([0, 2], score)
        >>> note_names(modified_score)
        [['D4']]
    """
    if isinstance(part_idx, int):
        part_idx = [part_idx]

    if isinstance(part_idx, str) or not isinstance(part_idx, (Container, Callable)):
        raise ValueError(
            f"part_idx must be an integer or a list of integers. Was: {part_idx}"
        )

    part_filter = lambda i, part: i not in part_idx

    return filter_parts(part_filter, score_input, save_to_filepath=save_to_filepath)
