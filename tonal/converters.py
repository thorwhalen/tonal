"""Convert music into various formats."""

import os
import io
import tempfile
from typing import Union, Optional, Callable, Any, Dict
from tonal.util import (
    DFLT_MIDI_OUTPUT,
    DFLT_SOUNDFONT,
    DFLT_WAV_OUTPUT,
)

# Type aliases
FilePath = str
BytesData = bytes

dflt_format_for_extension = {
    ".midi": "midi",
    ".mid": "midi",
    ".xml": "musicxml",
    ".musicxml": "musicxml",
    ".wav": "wav",
    ".png": "image",
    ".jpg": "image",
    ".jpeg": "image",
    # '.ipy_audio': 'audio',  # TODO: Handle IPython.display.Audio objects
    # '.ipy_audio': 'ipython',
}

dflt_extension_for_format = {v: k for k, v in dflt_format_for_extension.items()}

# Define magic number signatures for common file formats
FORMAT_SIGNATURES: Dict[bytes, str] = {
    b"MThd": "midi",  # MIDI files start with MThd
    b"RIFF": "wav",  # WAV files start with RIFF
    b"<?xml": "musicxml",  # XML files often start with <?xml
    b"<score-partwise": "musicxml",  # MusicXML specific identifier
    b"\xff\xd8": "image",  # JPEG files start with FF D8
    b"\x89PNG": "image",  # PNG files start with 89 PNG
}


def format_of_filepath(
    filepath: str, *, format_for_extension=dflt_format_for_extension
) -> str:
    """Return the format of a file."""
    ext = os.path.splitext(filepath)[-1].lower()
    return format_for_extension.get(ext, ext)


def replace_extension(src: str, dest_extension: str) -> str:
    """Replace the extension of a filepath with a new one."""
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


# Use dol.written_bytes to use file functions as bytes functions
def convert(
    src: Union[FilePath, BytesData],
    dest: Optional[Union[FilePath, str]] = None,
    *,
    src_format: Optional[str] = None,
    dest_format: Optional[str] = None,
    format_for_extension=dflt_format_for_extension,
) -> Union[FilePath, BytesData]:
    """
    Convert between different music formats.

    Args:
        src: Source as a filepath or bytes data
        dest: Destination filepath, format string, or None to return bytes
        src_format: Source format, inferred from filepath extension if None
        dest_format: Destination format, inferred from dest if None
        format_for_extension: Mapping of file extensions to format names

    Returns:
        If dest is a filepath: returns the destination filepath
        If dest is None or a format string or src is bytes: returns the converted bytes

    Examples:
        # File to file conversion
        convert('my_score.musicxml', 'my_score.mid')

        # File to bytes with specified format
        midi_bytes = convert('my_score.musicxml', dest_format='midi')

        # File to bytes using format string shorthand
        midi_bytes = convert('my_score.musicxml', 'midi')

        # Bytes to file
        convert(midi_bytes, 'output.wav', src_format='midi')

        # Bytes to bytes
        wav_bytes = convert(midi_bytes, src_format='midi', dest_format='wav')

        # Bytes to bytes with format string shorthand
        wav_bytes = convert(midi_bytes, 'wav', src_format='midi')
    """
    is_src_bytes = isinstance(src, bytes)

    # If dest is a format string in our known formats, use it as dest_format and set dest to None
    format_values = set(dflt_format_for_extension.values())
    if isinstance(dest, str) and dest in format_values:
        dest_format = dest
        dest = None

    return_bytes = dest is None

    # Determine source format
    if src_format is None:
        if not is_src_bytes:
            # If src is a filepath, infer format from extension
            src_format = format_of_filepath(
                src, format_for_extension=format_for_extension
            )
        else:
            # Try to guess format from bytes magic numbers/headers
            src_format = guess_format_from_bytes(src)

    # If dest is just an extension, add it to the source filename to make the actual filepath
    if not is_src_bytes and isinstance(dest, str) and dest in format_for_extension:
        dest_extension = dest
        dest = replace_extension(src, dest_extension)

    # Determine destination format
    if dest_format is None and dest is not None:
        dest_format = format_of_filepath(
            dest, format_for_extension=format_for_extension
        )

    if not src_format or not dest_format:
        raise ValueError(
            f"Could not determine formats: src_format={src_format}, dest_format={dest_format}. "
            f"Please specify src_format and dest_format explicitly."
        )

    # Handle bytes conversion path
    if is_src_bytes:
        return _convert_from_bytes(
            src, dest, src_format=src_format, dest_format=dest_format
        )

    # Handle file conversion path
    conversion_func = _get_conversion_func(src_format, dest_format)

    if return_bytes:
        # Convert file to bytes
        return _convert_file_to_bytes(src, conversion_func, dest_format)
    else:
        # Regular file to file conversion
        return conversion_func(src, dest)


def guess_format_from_bytes(data: bytes) -> Optional[str]:
    """
    Attempt to guess the format of a file from its bytes content.

    Args:
        data: The bytes data to analyze

    Returns:
        The format string or None if the format couldn't be determined
    """
    if not data:
        return None

    # Check for known file signatures
    for signature, format_name in FORMAT_SIGNATURES.items():
        if data.startswith(signature):
            return format_name

    # Check for MusicXML by looking for common tags if it's likely XML
    if data.startswith(b"<") or b"<?xml" in data[:100]:
        if b"<score-partwise" in data[:1000] or b"<score-timewise" in data[:1000]:
            return "musicxml"

    # Check for MIDI by looking for track chunks if the file starts with MThd
    if len(data) > 14 and data[:4] == b"MThd" and b"MTrk" in data[:1000]:
        return "midi"

    return None


def _get_conversion_func(src_format: str, dest_format: str) -> Callable:
    """Get the appropriate conversion function based on formats."""
    if src_format == "musicxml" and dest_format == "midi":
        return musicxml_to_midi
    elif src_format == "midi" and dest_format == "wav":
        return midi_to_wav
    elif src_format == "image" and dest_format == "musicxml":
        return image_to_musicxml
    else:
        raise ValueError(f"Unsupported conversion: {src_format} -> {dest_format}")


def _convert_from_bytes(
    src_bytes: bytes, dest: Optional[str] = None, *, src_format: str, dest_format: str
) -> Union[FilePath, bytes]:
    """Handle conversions where the source is bytes."""
    # Write bytes to a temporary file with the correct extension
    with tempfile.NamedTemporaryFile(
        suffix=dflt_extension_for_format.get(src_format, f".{src_format}"), delete=False
    ) as temp_file:
        temp_src = temp_file.name
        temp_file.write(src_bytes)

    try:
        conversion_func = _get_conversion_func(src_format, dest_format)

        if dest is None:
            # Return bytes
            temp_dest = temp_src.replace(
                os.path.splitext(temp_src)[1],
                dflt_extension_for_format.get(dest_format, f".{dest_format}"),
            )
            conversion_func(temp_src, temp_dest)

            with open(temp_dest, "rb") as f:
                result = f.read()

            try:
                os.remove(temp_dest)
            except:
                pass

            return result
        else:
            # Write to the specified destination
            return conversion_func(temp_src, dest)
    finally:
        try:
            os.remove(temp_src)
        except:
            pass


def _convert_file_to_bytes(
    src_file: str, conversion_func: Callable, dest_format: str
) -> bytes:
    """Convert a file to bytes using the specified conversion function."""
    # Create a temporary output file
    ext = dflt_extension_for_format.get(dest_format, f".{dest_format}")
    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as temp_file:
        temp_dest = temp_file.name

    try:
        conversion_func(src_file, temp_dest)
        with open(temp_dest, "rb") as f:
            return f.read()
    finally:
        try:
            os.remove(temp_dest)
        except:
            pass


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
    """Convert a MusicXML file to MIDI."""
    from music21 import converter

    if midi_path is None:
        midi_path = musicxml_path.replace(".musicxml", ".mid")
    score = converter.parse(musicxml_path)
    score.write("midi", fp=midi_path)
    return midi_path


def midi_to_wav(
    midi_file: str,
    output_wav: str = None,
    *,
    soundfont: str = DFLT_SOUNDFONT,
):
    """
    Synthesize audio from a MIDI file using FluidSynth.

    Args:
        midi_file: Name of the input MIDI file.
        output_wav: Name of the output WAV file.
        soundfont: Path to the SoundFont file.
    """
    import subprocess

    output_wav = ensure_dest_filepath(midi_file, output_wav, dest_format="wav")

    subprocess.run(
        ["fluidsynth", "-ni", soundfont, midi_file, "-F", output_wav, "-r", "44100"]
    )

    return output_wav
