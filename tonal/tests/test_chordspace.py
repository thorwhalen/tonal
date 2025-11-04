"""
Tests for chordspace module, focusing on chord table and link computation.

Note: Tests use small inputs to ensure efficiency.
"""

import sys
from pathlib import Path

# Add parent directory to path to allow direct import of chordspace
# This avoids triggering tonal.__init__ which has heavy dependencies
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from tonal.chordspace import (
    chord_table,
    compute_links,
    shared_pcs,
    voice_leading_distance,
    is_subset_pcs,
    is_codiatonic,
    _generate_ids,
    _chord_features,
    _compute_interval_vector,
)


# ---------------------------------------------------------------------------
# Test basic utility functions
# ---------------------------------------------------------------------------


def test_shared_pcs():
    """Test shared pitch class counting."""
    assert shared_pcs((0, 4, 7), (0, 7, 11)) == 2
    assert shared_pcs((0, 4, 7), (2, 5, 9)) == 0
    assert shared_pcs((0, 4, 7), (0, 4, 7)) == 3


def test_voice_leading_distance():
    """Test voice leading distance calculation."""
    assert voice_leading_distance((0, 4, 7), (0, 5, 7)) == 1
    assert voice_leading_distance((0, 4, 7), (0, 4, 7)) == 0
    assert voice_leading_distance((0, 4, 7), (1, 5, 8)) == 3


def test_is_subset_pcs():
    """Test pitch-class subset relation."""
    assert is_subset_pcs((0, 4, 7), (0, 2, 4, 7, 9)) is True
    assert is_subset_pcs((0, 4, 7), (1, 4, 7)) is False
    assert is_subset_pcs((0, 4, 7), (0, 4, 7)) is True


# ---------------------------------------------------------------------------
# Test ID generation strategies
# ---------------------------------------------------------------------------


def test_generate_ids_int():
    """Test integer-based ID generation."""
    voicings = [(0, 4, 7), (0, 3, 7), (0, 5, 9)]
    ids = _generate_ids(voicings, "int")
    assert ids == [0, 1, 2]


def test_generate_ids_repr():
    """Test repr-based ID generation."""
    voicings = [(0, 4, 7), (0, 3, 7)]
    ids = _generate_ids(voicings, "repr")
    assert ids == ["(0, 4, 7)", "(0, 3, 7)"]


def test_generate_ids_hash():
    """Test hash-based ID generation."""
    voicings = [(0, 4, 7), (0, 3, 7)]
    ids = _generate_ids(voicings, "hash")
    assert len(ids) == 2
    assert all(isinstance(i, int) for i in ids)
    assert ids[0] != ids[1]  # Should be different


def test_generate_ids_invalid():
    """Test invalid index_by raises error."""
    voicings = [(0, 4, 7)]
    with pytest.raises(ValueError, match="Unknown index_by mode"):
        _generate_ids(voicings, "invalid")


# ---------------------------------------------------------------------------
# Test chord feature extraction
# ---------------------------------------------------------------------------


def test_chord_features():
    """Test extraction of chord features."""
    features = _chord_features(0, (0, 4, 7), "id_")

    assert features["id_"] == 0
    assert features["voicing"] == (0, 4, 7)
    assert features["n_notes"] == 3
    assert features["span"] == 7
    assert features["pitch_classes"] == [0, 4, 7]
    assert features["n_pcs"] == 3
    assert len(features["interval_vector"]) == 6


def test_chord_features_single_note():
    """Test chord features for single note."""
    features = _chord_features(0, (60,), "id_")
    assert features["span"] == 0
    assert features["n_notes"] == 1


def test_interval_vector():
    """Test interval vector computation."""
    # Major triad: C E G (0, 4, 7)
    pcs = [0, 4, 7]
    iv = _compute_interval_vector(pcs)
    assert len(iv) == 6
    assert all(isinstance(x, int) for x in iv)


# ---------------------------------------------------------------------------
# Test chord_table function
# ---------------------------------------------------------------------------


def test_chord_table_basic():
    """Test basic chord table generation without pandas."""
    voicings = [(0, 4, 7), (0, 3, 7), (0, 5, 9)]
    table = list(chord_table(voicings=voicings, use_pandas=False))

    assert len(table) == 3
    assert all("id_" in row for row in table)
    assert all("voicing" in row for row in table)
    assert all("n_notes" in row for row in table)


def test_chord_table_custom_id_col():
    """Test chord table with custom ID column name."""
    voicings = [(0, 4, 7), (0, 3, 7)]
    table = list(chord_table(voicings=voicings, id_col="chord_id", use_pandas=False))

    assert all("chord_id" in row for row in table)
    assert all("id_" not in row for row in table)


def test_chord_table_different_index_strategies():
    """Test different indexing strategies."""
    voicings = [(0, 4, 7), (0, 3, 7)]

    # Int indexing
    table_int = list(chord_table(voicings=voicings, index_by="int", use_pandas=False))
    assert table_int[0]["id_"] == 0
    assert table_int[1]["id_"] == 1

    # Repr indexing
    table_repr = list(chord_table(voicings=voicings, index_by="repr", use_pandas=False))
    assert isinstance(table_repr[0]["id_"], str)


def test_chord_table_with_links():
    """Test chord table with link computation."""
    voicings = [(0, 4, 7), (0, 5, 7), (0, 4, 7, 11)]
    table = list(
        chord_table(
            voicings=voicings,
            include_links=True,
            link_kinds=["shared"],
            min_shared_pcs=2,
            use_pandas=False,
        )
    )

    assert len(table) == 3
    assert all("shared_links" in row for row in table)
    assert all(isinstance(row["shared_links"], list) for row in table)


def test_chord_table_multiple_link_kinds():
    """Test chord table with multiple link kinds."""
    voicings = [(0, 4, 7), (0, 5, 7), (0, 4, 7, 11)]
    table = list(
        chord_table(
            voicings=voicings,
            include_links=True,
            link_kinds=["shared", "subset"],
            use_pandas=False,
        )
    )

    assert all("shared_links" in row for row in table)
    assert all("subset_links" in row for row in table)


def test_chord_table_with_pandas():
    """Test chord table returns DataFrame when use_pandas=True."""
    pd = pytest.importorskip("pandas")

    voicings = [(0, 4, 7), (0, 3, 7)]
    table = chord_table(voicings=voicings, use_pandas=True)

    assert isinstance(table, pd.DataFrame)
    assert len(table) == 2
    assert "id_" in table.columns
    assert "voicing" in table.columns


# ---------------------------------------------------------------------------
# Test compute_links function
# ---------------------------------------------------------------------------


def test_compute_links_shared():
    """Test shared pitch-class links."""
    rows = [
        {'id_': 0, 'voicing': (0, 4, 7), 'pitch_classes': [0, 4, 7]},
        {'id_': 1, 'voicing': (0, 5, 7), 'pitch_classes': [0, 5, 7]},
        {'id_': 2, 'voicing': (0, 4, 7, 11), 'pitch_classes': [0, 4, 7, 11]},
    ]

    links = compute_links(rows, kind="shared", min_shared_pcs=2)

    assert len(links) == 3
    assert 1 in links[0]  # first chord shares 2 PCs with second
    assert 2 in links[0]  # first chord shares 3 PCs with third
    assert 0 in links[1]  # second chord shares 2 PCs with first


def test_compute_links_subset():
    """Test subset links."""
    rows = [
        {'id_': 0, 'voicing': (0, 4, 7), 'pitch_classes': [0, 4, 7]},
        {'id_': 1, 'voicing': (0, 4, 7, 11), 'pitch_classes': [0, 4, 7, 11]},
    ]

    links = compute_links(rows, kind="subset")

    assert len(links) == 2
    assert 1 in links[0]  # first is subset of second
    assert 1 not in links[1]  # second is not subset of first


def test_compute_links_voiceleading():
    """Test voice-leading links."""
    rows = [
        {'id_': 0, 'voicing': (0, 4, 7), 'pitch_classes': [0, 4, 7]},
        {'id_': 1, 'voicing': (0, 5, 7), 'pitch_classes': [0, 5, 7]},
        {'id_': 2, 'voicing': (5, 9, 12), 'pitch_classes': [0, 5, 9]},
    ]

    links = compute_links(rows, kind="voiceleading", max_vl_distance=2)

    assert len(links) == 3
    assert 1 in links[0]  # distance of 1


def test_compute_links_invalid_kind():
    """Test invalid link kind raises error."""
    rows = [{'id_': 0, 'voicing': (0, 4, 7), 'pitch_classes': [0, 4, 7]}]

    with pytest.raises(ValueError, match="Unknown link kind"):
        compute_links(rows, kind="invalid")


def test_compute_links_with_dataframe():
    """Test compute_links works with pandas DataFrame."""
    pd = pytest.importorskip("pandas")

    df = pd.DataFrame(
        [
            {'id_': 0, 'voicing': (0, 4, 7), 'pitch_classes': [0, 4, 7]},
            {'id_': 1, 'voicing': (0, 5, 7), 'pitch_classes': [0, 5, 7]},
        ]
    )

    links = compute_links(df, kind="shared", min_shared_pcs=2)

    assert len(links) == 2
    assert isinstance(links[0], list)


def test_compute_links_custom_id_col():
    """Test compute_links with custom ID column."""
    rows = [
        {'my_id': 100, 'voicing': (0, 4, 7), 'pitch_classes': [0, 4, 7]},
        {'my_id': 200, 'voicing': (0, 5, 7), 'pitch_classes': [0, 5, 7]},
    ]

    links = compute_links(rows, id_col="my_id", kind="shared", min_shared_pcs=2)

    assert 200 in links[0]
    assert 100 in links[1]


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------


def test_full_workflow_without_pandas():
    """Test complete workflow: create table and compute separate links."""
    # Create table without links
    voicings = [(0, 4, 7), (0, 3, 7), (0, 4, 7, 11)]
    table = list(chord_table(voicings=voicings, use_pandas=False))

    # Compute links separately
    shared_links = compute_links(table, kind="shared", min_shared_pcs=2)
    subset_links = compute_links(table, kind="subset")

    assert len(shared_links) == 3
    assert len(subset_links) == 3


def test_full_workflow_with_pandas():
    """Test complete workflow with pandas."""
    pd = pytest.importorskip("pandas")

    voicings = [(0, 4, 7), (0, 3, 7), (0, 4, 7, 11)]

    # Create table with links included
    table = chord_table(
        voicings=voicings,
        include_links=True,
        link_kinds=["shared", "voiceleading"],
        use_pandas=True,
    )

    assert isinstance(table, pd.DataFrame)
    assert "shared_links" in table.columns
    assert "voiceleading_links" in table.columns


def test_empty_voicings():
    """Test handling of empty voicing list."""
    table = list(chord_table(voicings=[], use_pandas=False))
    assert len(table) == 0


def test_compute_links_codiatonic():
    """Test codiatonic link computation."""
    rows = [
        {"id_": 0, "voicing": (0, 4, 7), "pitch_classes": [0, 4, 7]},  # C major
        {"id_": 1, "voicing": (2, 5, 9), "pitch_classes": [2, 5, 9]},  # D minor
        {
            "id_": 2,
            "voicing": (1, 5, 8),
            "pitch_classes": [1, 5, 8],
        },  # C# major (not in C major scale)
    ]

    links = compute_links(rows, kind="codiatonic")

    # C major and D minor should be codiatonic (both in C major scale)
    assert 1 in links[0]
    assert 0 in links[1]

    # C# major should not be codiatonic with C major or D minor
    assert 2 not in links[0]
    assert 2 not in links[1]


def test_custom_link_function():
    """Test using a custom link function."""
    rows = [
        {"id_": 0, "voicing": (0, 4, 7), "pitch_classes": [0, 4, 7]},
        {"id_": 1, "voicing": (1, 5, 8), "pitch_classes": [1, 5, 8]},
        {"id_": 2, "voicing": (0, 3, 7), "pitch_classes": [0, 3, 7]},
    ]

    # Custom function: link if root notes (first pitch) are same
    def same_root(i, j, voicings, pc_sets, **kwargs):
        return voicings[i][0] % 12 == voicings[j][0] % 12

    links = compute_links(rows, kind=same_root)

    # Chords 0 and 2 both start with 0 (C)
    assert 2 in links[0]
    assert 0 in links[2]

    # Chord 1 starts with 1 (C#), so no matches
    assert len(links[1]) == 0


if __name__ == "__main__":
    # Run a quick test when executed directly
    print("Running basic smoke tests...")

    # Test basic functionality
    test_shared_pcs()
    print("✓ shared_pcs works")

    test_voice_leading_distance()
    print("✓ voice_leading_distance works")

    test_is_subset_pcs()
    print("✓ is_subset_pcs works")

    test_generate_ids_int()
    print("✓ ID generation works")

    test_chord_features()
    print("✓ Chord features extraction works")

    test_chord_table_basic()
    print("✓ Basic chord table works")

    test_chord_table_with_links()
    print("✓ Chord table with links works")

    test_compute_links_shared()
    print("✓ Compute links (shared) works")

    test_compute_links_subset()
    print("✓ Compute links (subset) works")

    test_compute_links_codiatonic()
    print("✓ Compute links (codiatonic) works")

    test_custom_link_function()
    print("✓ Custom link functions work")

    test_compute_links_voiceleading()
    print("✓ Compute links (voiceleading) works")

    print("\n✅ All basic tests passed!")
