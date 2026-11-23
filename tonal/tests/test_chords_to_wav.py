"""`chords_to_wav` renders through this package's own converter, not the separate `sonification` package."""

import sys

import pytest

pytest.importorskip("mido")


def test_chords_to_wav_needs_no_sonification(tmp_path, monkeypatch):
    import tonal.converters
    from tonal.chords import chords_to_wav

    calls = []

    def fake_midi_to_wav(midi_file, output_wav=None, *, soundfont=None):
        calls.append((midi_file, output_wav))

    monkeypatch.setitem(sys.modules, "sonification", None)  # makes `import sonification` fail
    monkeypatch.setattr(tonal.converters, "midi_to_wav", fake_midi_to_wav)
    name = str(tmp_path / "out")
    assert chords_to_wav([("C", 1)], name) == f"{name}.wav"
    assert calls == [(f"{name}.mid", f"{name}.wav")]
