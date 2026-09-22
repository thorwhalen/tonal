# tonal.converters

Convert music into various formats.

### Functions

| [`convert`](#tonal.converters.convert)(src[, dest, src_format, ...])             | Convert between different music formats.                      |
|----------------------------------------------------------------------------------------------------|---------------------------------------------------------------|
| [`ensure_dest_filepath`](#tonal.converters.ensure_dest_filepath)(src, dest, \*[, ...])        | Ensure that a destination filepath is given.                  |
| [`format_of_filepath`](#tonal.converters.format_of_filepath)(filepath, \*[, ...])           | Return the format of a file.                                  |
| [`guess_format_from_bytes`](#tonal.converters.guess_format_from_bytes)(data)                     | Attempt to guess the format of a file from its bytes content. |
| [`image_to_musicxml`](#tonal.converters.image_to_musicxml)(image, \*[, enable_debug, ...]) | Convert and image of a music score into a musicxml file.      |
| [`midi_to_wav`](#tonal.converters.midi_to_wav)(midi_file[, output_wav, soundfont])   | Synthesize audio from a MIDI file using FluidSynth.           |
| [`musicxml_to_midi`](#tonal.converters.musicxml_to_midi)(musicxml_path[, midi_path])      | Convert a MusicXML file to MIDI.                              |
| [`replace_extension`](#tonal.converters.replace_extension)(src, dest_extension)            | Replace the extension of a filepath with a new one.           |

### tonal.converters.convert(src, dest=None, , src_format=None, dest_format=None, format_for_extension={'.jpeg': 'image', '.jpg': 'image', '.mid': 'midi', '.midi': 'midi', '.musicxml': 'musicxml', '.png': 'image', '.wav': 'wav', '.xml': 'musicxml'})

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

### tonal.converters.ensure_dest_filepath(src, dest, , dest_format=None, extension_for_format={'image': '.jpeg', 'midi': '.mid', 'musicxml': '.musicxml', 'wav': '.wav'})

Ensure that a destination filepath is given.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

### tonal.converters.format_of_filepath(filepath, , format_for_extension={'.jpeg': 'image', '.jpg': 'image', '.mid': 'midi', '.midi': 'midi', '.musicxml': 'musicxml', '.png': 'image', '.wav': 'wav', '.xml': 'musicxml'})

Return the format of a file.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

### tonal.converters.guess_format_from_bytes(data)

Attempt to guess the format of a file from its bytes content.

* **Parameters:**
  **data** ([`bytes`](https://docs.python.org/3/builtins/stdtypes.html#bytes)) – The bytes data to analyze
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str) | [`None`](https://docs.python.org/3/builtins/constants.html#None)
* **Returns:**
  The format string or None if the format couldn’t be determined

### tonal.converters.image_to_musicxml(image, , enable_debug=False, enable_cache=False, remove_teaser_file=True)

Convert and image of a music score into a musicxml file.

### tonal.converters.midi_to_wav(midi_file, output_wav=None, , soundfont='/home/runner/work/tonal/tonal/tonal/data/Caeds Small Trash GM v1.06.sf2')

Synthesize audio from a MIDI file using FluidSynth.

* **Parameters:**
  * **midi_file** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of the input MIDI file.
  * **output_wav** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of the output WAV file.
  * **soundfont** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to the SoundFont file.

### tonal.converters.musicxml_to_midi(musicxml_path, midi_path=None)

Convert a MusicXML file to MIDI.

### tonal.converters.replace_extension(src, dest_extension)

Replace the extension of a filepath with a new one.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
