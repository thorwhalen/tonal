"""Convert music into various formats."""

import os
from tonal.util import DFLT_MIDI_OUTPUT, DFLT_SOUNDFONT, DFLT_WAV_OUTPUT

dflt_format_for_extension = {
    '.midi': 'midi',
    '.mid': 'midi',
    '.xml': 'musicxml',
    '.musicxml': 'musicxml',
    '.wav': 'wav',
    '.png': 'image',
    '.jpg': 'image',
    '.jpeg': 'image',
}

dflt_extension_for_format = {v: k for k, v in dflt_format_for_extension.items()}


def format_of_filepath(
    filepath: str, *, format_for_extension=dflt_format_for_extension
) -> str:
    """Return the format of a file."""
    ext = os.path.splitext(filepath)[-1].lower()
    return format_for_extension.get(ext, ext)


def replace_extension(src: str, dest_extension: str) -> str:
    return src.replace(os.path.splitext(src)[-1], dest_extension)


def ensure_dest_filepath(
    src: str,
    dest: str,
    *,
    dest_format: str = None,
    extension_for_format=dflt_extension_for_format,
) -> str:
    """Ensure that a destination filepath is given."""
    if dest is None:
        src_ext = os.path.splitext(src)[-1]
        dest_ext = extension_for_format.get(dest_format, f".{dest_format}")
        dest = src.replace(src_ext, dest_ext)
    return dest


def convert(
    src: str,
    dest: str,
    *,
    src_format: str = None,
    dest_format: str = None,
    format_for_extension=dflt_format_for_extension,
) -> str:
    src_format = format_of_filepath(src)

    # if dest is just an extension, add it to the source filename to make the actual filepath
    if dest in format_for_extension:
        dest_extension = dest
        dest = replace_extension(src, dest_extension)

    dest_format = format_of_filepath(dest)

    # print(locals())
    if src_format == 'musicxml' and dest_format == 'midi':
        return musicxml_to_midi(src, dest)
    if src_format == 'midi' and dest_format == 'wav':
        return midi_to_wav(src, dest)
    if src_format == 'image' and dest_format == 'musicxml':
        return image_to_musicxml(src)
    raise ValueError(f"Unsupported conversion: {src_format} -> {dest_format}")


def image_to_musicxml(
    image: str, *, enable_debug=False, enable_cache=False, remove_teaser_file=True
):
    """Convert and image of a music score into a musicxml file."""
    from homr.main import process_image

    musicxml_filepath, _, teaser_filepath = process_image(
        image, enable_debug=enable_debug, enable_cache=enable_cache
    )

    if remove_teaser_file:
        os.remove(teaser_filepath)

    return musicxml_filepath


def musicxml_to_midi(musicxml_path, midi_path=None):
    from music21 import converter

    if midi_path is None:
        midi_path = musicxml_path.replace('.musicxml', '.mid')
    score = converter.parse(musicxml_path)
    score.write('midi', fp=midi_path)
    return midi_path


def midi_to_wav(
    midi_file: str,
    output_wav: str = None,
    *,
    soundfont: str = DFLT_SOUNDFONT,
):
    """
    Synthesize audio from a MIDI file using FluidSynth.

    :param midi_file: Name of the input MIDI file.
    :param output_wav: Name of the output WAV file.
    :param soundfont: Path to the SoundFont file.

    """
    import subprocess

    output_wav = ensure_dest_filepath(midi_file, output_wav, dest_format='wav')

    subprocess.run(
        ['fluidsynth', '-ni', soundfont, midi_file, '-F', output_wav, '-r', '44100']
    )

    return output_wav
