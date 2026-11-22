"""Tests for ``tonal.converters``: format detection, path helpers and the dispatch logic.

The real converters (music21, homr, fluidsynth) are replaced by tiny fakes, so these run anywhere.
"""

import pytest

from tonal import converters as cv


# --- format detection -------------------------------------------------------------------


@pytest.mark.parametrize(
    "path, fmt",
    [
        ("a.MID", "midi"),
        ("a.midi", "midi"),
        ("a.musicxml", "musicxml"),
        ("a.XML", "musicxml"),
        ("a.wav", "wav"),
        ("a.jpeg", "image"),
        ("a.unknown", ".unknown"),
    ],
)
def test_format_of_filepath(path, fmt):
    assert cv.format_of_filepath(path) == fmt


@pytest.mark.parametrize(
    "data, fmt",
    [
        (b"", None),
        (b"MThd\x00\x00\x00\x06", "midi"),
        (b"RIFF....WAVE", "wav"),
        (b"\x89PNG\r\n", "image"),
        (b"\xff\xd8\xff", "image"),
        (b"<?xml version='1.0'?><score-partwise/>", "musicxml"),
        (b"  <?xml ?><score-timewise>", "musicxml"),
        (b"<html></html>", None),
        (b"random bytes", None),
    ],
)
def test_guess_format_from_bytes(data, fmt):
    assert cv.guess_format_from_bytes(data) == fmt


# --- path helpers -----------------------------------------------------------------------


def test_replace_extension_and_ensure_dest_filepath():
    assert cv.replace_extension("a/b.mid", ".wav") == "a/b.wav"
    assert cv.ensure_dest_filepath("a.musicxml", None, dest_format="midi") == "a.mid"
    assert cv.ensure_dest_filepath("a.musicxml", "keep.mid") == "keep.mid"
    assert cv.ensure_dest_filepath("a.x", None, dest_format="zzz") == "a.zzz"


@pytest.mark.xfail(
    strict=True,
    reason="https://github.com/thorwhalen/tonal/issues/13: str.replace hits every occurrence",
)
def test_replace_extension_only_touches_the_suffix():
    assert cv.replace_extension("/t/x.mid/foo.mid", ".wav") == "/t/x.mid/foo.wav"


@pytest.mark.xfail(
    strict=True,
    reason="https://github.com/thorwhalen/tonal/issues/13: an empty extension matches everywhere",
)
def test_replace_extension_of_an_extensionless_path_appends():
    assert cv.replace_extension("noext", ".wav") == "noext.wav"


# --- dispatch ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "src, dest, name",
    [
        ("musicxml", "midi", "musicxml_to_midi"),
        ("midi", "wav", "midi_to_wav"),
        ("image", "musicxml", "image_to_musicxml"),
    ],
)
def test_get_conversion_func_picks_the_registered_converter(src, dest, name):
    assert cv._get_conversion_func(src, dest) is getattr(cv, name)


def test_unsupported_conversions_are_rejected():
    with pytest.raises(ValueError, match="Unsupported conversion: wav -> midi"):
        cv._get_conversion_func("wav", "midi")


@pytest.fixture
def fake_converters(monkeypatch):
    calls = []

    def fake(src, dest=None):
        calls.append((src, dest))
        with open(dest, "wb") as f:
            f.write(b"converted:" + open(src, "rb").read())
        return dest

    monkeypatch.setattr(cv, "musicxml_to_midi", fake)
    return calls


def test_convert_file_to_file(tmp_path, fake_converters):
    src = tmp_path / "s.musicxml"
    src.write_bytes(b"xml")
    dest = tmp_path / "d.mid"
    assert cv.convert(str(src), str(dest)) == str(dest)
    assert dest.read_bytes() == b"converted:xml"


def test_convert_file_to_bytes_with_a_format_shorthand(tmp_path, fake_converters):
    src = tmp_path / "s.musicxml"
    src.write_bytes(b"xml")
    assert cv.convert(str(src), "midi") == b"converted:xml"


def test_convert_bytes_to_bytes_guesses_the_source_format(fake_converters):
    out = cv.convert(b"<?xml ?><score-partwise/>", "midi")
    assert out.startswith(b"converted:")


def test_convert_bytes_to_a_file(tmp_path, fake_converters):
    dest = tmp_path / "out.mid"
    cv.convert(b"xml", str(dest), src_format="musicxml")
    assert dest.read_bytes() == b"converted:xml"


def test_convert_with_undeterminable_formats_names_both(tmp_path):
    with pytest.raises(ValueError, match="Could not determine formats"):
        cv.convert(b"random bytes", "midi")
    with pytest.raises(ValueError, match="dest_format=None"):
        cv.convert(b"xml", src_format="musicxml")


def test_temp_files_are_cleaned_up_even_when_the_converter_fails(monkeypatch):
    seen = []

    def boom(src, dest=None):
        seen.append(src)
        raise RuntimeError("engine down")

    monkeypatch.setattr(cv, "musicxml_to_midi", boom)
    import os

    with pytest.raises(RuntimeError, match="engine down"):
        cv.convert(b"xml", "midi", src_format="musicxml")
    assert seen and not os.path.exists(seen[0])
