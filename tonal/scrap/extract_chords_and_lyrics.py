import os
import subprocess
from pathlib import Path
from music21 import converter, harmony, note, stream

# TODO: Write a tool that will find the mscore executable automatically
# Path to your MuseScore CLI executable
MSCORE_CMD = "/Applications/MuseScore 4.app/Contents/MacOS/mscore"

import subprocess
from pathlib import Path
from music21 import converter, harmony, note, stream

MSCORE_CMD = "/Applications/MuseScore 4.app/Contents/MacOS/mscore"


# How extract_chord_and_lyrics works
# 	1.	Convert .mscz to MusicXML via the MuseScore CLI.
# 	2.	Parse and flatten into a single time‐aligned stream.
# 	3.	Extract all ChordSymbol objects (using their .offset and .figure).
# 	4.	For each Note.lyrics, read .offset, .text and .number (verse index).
# 	5.	Compute a total width in characters = max_offset*resolution + longest_text +1.
# 	6.	Build one character‐array of length width for chords and one per verse.
# 	7.	Scatter each chord and lyric text at the column = int(offset*resolution).
# 	8.	Right‐trim each line and concatenate: chord–verse1–verse2–…–blank.
def extract_chord_and_lyrics(input_path: str, resolution: int = 8) -> str:
    """
    Converts an MSCZ to MusicXML if needed, then extracts one chord line
    and N lyric lines (one per verse), aligning everything in fixed-width ASCII.

    Returns a single multiline string:
      chord_line
      lyric_line (verse 1)
      lyric_line (verse 2)
      …
      (blank separator)
    """
    p = Path(input_path)
    # 1. Convert .mscz → .musicxml if necessary
    if p.suffix.lower() == ".mscz":
        xml_path = p.with_suffix(".musicxml")
        subprocess.run([MSCORE_CMD, "-o", str(xml_path), str(p)], check=True)
    else:
        assert p.suffix.lower() in (
            ".xml",
            ".mxl",
            ".musicxml",
        ), "Input must be .mscz, .xml, or .mxl"
        xml_path = p

    # 2. Parse and flatten
    score: stream.Score = converter.parse(str(xml_path))
    flat_score = score.flatten()

    # 3. Collect chord events (offset, text)
    chords = [
        (cs.offset, cs.figure)
        for cs in flat_score.getElementsByClass(harmony.ChordSymbol)
    ]

    # 4. Collect lyric events, grouped by verse number
    lyric_events = {}
    for nt in flat_score.getElementsByClass(note.Note):
        for lyr in nt.lyrics:
            verse = lyr.number or "1"  # default verse "1"
            lyric_events.setdefault(verse, []).append((nt.offset, lyr.text))

    # 5. Determine total width
    all_texts = [text for _, text in chords]
    for evs in lyric_events.values():
        all_texts += [text for _, text in evs]
    if not all_texts:
        return ""
    max_offset = max(
        [off for off, _ in chords]
        + [off for evs in lyric_events.values() for off, _ in evs]
    )
    max_len = max(len(t) for t in all_texts)
    width = int(max_offset * resolution) + max_len + 1

    # 6. Initialize lines
    chord_line = [" "] * width
    lyric_lines = {verse: [" "] * width for verse in sorted(lyric_events, key=int)}

    # 7. Place chords
    for offset, text in chords:
        col = int(offset * resolution)
        for i, ch in enumerate(text):
            if col + i < width:
                chord_line[col + i] = ch

    # 8. Place each verse’s lyrics
    for verse, evs in lyric_events.items():
        line = lyric_lines[verse]
        for offset, text in evs:
            col = int(offset * resolution)
            for i, ch in enumerate(text):
                if col + i < width:
                    line[col + i] = ch

    # 9. Assemble output
    out_lines = ["".join(chord_line).rstrip()]
    for verse in sorted(lyric_lines, key=int):
        out_lines.append("".join(lyric_lines[verse]).rstrip())
    out_lines.append("")  # final blank separator

    return "\n".join(out_lines)


def wrap_aligned_ascii(ascii_block: str, max_width: int) -> str:
    """
    Wrap a two-line ASCII block of chords over lyrics into multiple pages/lines,
    without splitting words, and preferring line breaks before capitalized words.

    Parameters:
        ascii_block (str): Two-line string with chords on the first line and lyrics on the second.
        max_width (int): Maximum characters per line.

    Returns:
        str: Wrapped ASCII, with each chunk consisting of:
             chord_line
             lyric_line
             (blank line)
    """
    # Split into the chord line and the lyric line
    lines = ascii_block.splitlines()
    if len(lines) < 2:
        return ascii_block  # nothing to wrap

    chord_line, lyric_line = lines[0], lines[1]
    length = len(lyric_line)
    wrapped_lines = []
    start = 0

    while start < length:
        # Determine the furthest we could go
        end = min(start + max_width, length)

        # Collect all candidate break positions (spaces)
        uppercase_breaks = []
        general_breaks = []
        for i in range(start + 1, end):
            if lyric_line[i] == " ":
                # space followed by uppercase => preferred
                if i + 1 < length and lyric_line[i + 1].isupper():
                    uppercase_breaks.append(i)
                else:
                    general_breaks.append(i)

        # Pick break position
        if uppercase_breaks:
            breakpos = uppercase_breaks[-1]
        elif general_breaks:
            breakpos = general_breaks[-1]
        else:
            # no space found => hard break at max width
            breakpos = end

        # Slice out the segment
        chord_seg = chord_line[start:breakpos].rstrip()
        lyric_seg = lyric_line[start:breakpos].rstrip()

        # Append to result
        wrapped_lines.append(chord_seg)
        wrapped_lines.append(lyric_seg)
        wrapped_lines.append("")  # blank separator

        # Move past the break; skip the space if we broke on one
        start = breakpos + (
            1 if breakpos < length and lyric_line[breakpos] == " " else 0
        )

    return "\n".join(wrapped_lines)


def example_usage():
    """
    Example usage of the extract_chord_lyrics function.
    """
    musicxml_file = "/Users/thorwhalen/Dropbox/Media/music/musescore/Over The Rainbow/Over_The_Rainbow__lead_sheet_-_A_modified.mscz"
    output_string = extract_chord_lyrics(musicxml_file, resolution=8)
    print(wrap_aligned_ascii(output_string, max_width=80))


# example_usage()
