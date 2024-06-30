"""Utils for sonify."""

from importlib.resources import files
from config2py import (
    process_path,
    simple_config_getter,
)

pkg_name = 'tonal'

data_files = files(pkg_name) / 'data'

get_config = simple_config_getter(pkg_name)


DFLT_OUTPUT_NAME = 'audio_output'
DFLT_MIDI_OUTPUT = f"{DFLT_OUTPUT_NAME}.mid"
DFLT_WAV_OUTPUT = f"{DFLT_OUTPUT_NAME}.wav"
DFLT_SOUNDFONT = process_path(
    get_config('TONAL_DFLT_SOUNDFONT_PATH'),
)

from typing import Callable, Iterable, List, Union, Generator
from operator import attrgetter

from music21.stream import Score, Stream, Part
from music21.midi.realtime import StreamPlayer
from music21.scale import Scale, MajorScale
from music21.note import Note


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
Streams = Iterable[Stream]


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
