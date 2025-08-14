"""Test notes module"""

import pytest

from tonal.notes import (
    list_root_notes,
    list_scale_qualities,
    scale_midi_notes,
    scale_params,
    list_scales_string,
    IncorrectScaleSpecification,
)


def test_list_scales_string_has_expected_sections():
    s = list_scales_string()
    sl = s.lower()
    assert "anatomy" in sl
    assert "valid roots" in sl
    assert "valid qualities" in sl


def test_all_root_quality_combinations_parse_with_scale_midi_notes():
    roots = sorted(list_root_notes().keys())
    qualities = sorted(list_scale_qualities(include_aliases=True).keys())

    for root in roots:
        for quality in qualities:
            spec = f"{root} {quality}".strip()
            try:
                notes = scale_midi_notes(spec)
            except IncorrectScaleSpecification as e:
                pytest.fail(f"Spec '{spec}' raised IncorrectScaleSpecification: {e}")
            # Should be a tuple of ints (can be empty depending on range, but default range is full MIDI)
            assert isinstance(notes, tuple)
            assert all(isinstance(n, int) for n in notes)


def test_scale_params_raises_helpful_error_on_invalid_spec():
    with pytest.raises(IncorrectScaleSpecification) as excinfo:
        scale_params("H hypermix")
    msg = str(excinfo.value).lower()
    assert "incorrect scale specification" in msg
    assert "valid roots" in msg
    assert "valid qualities" in msg
