"""
chordspace.py

A small, opinionated module to generate *theoretical* chord data and to link
chords (or chord voicings) into a graph according to several criteria.

The design follows the conversation:
- level 1: raw pitch-class combinations (choose k from 12)
- level 2: voicings in a bounded range above a fixed root
- level 3: graph edges based on similarity / voice-leading / subset relations

It is **not** tied to any specific music theory naming system. It just produces
structured data you can then map to names.

Conventions
-----------
- Pitch classes are 0..11 (0 = C, 1 = C#, ..., 11 = B).
- Pitches (not just pitch classes) are integers too: 60 = C4, etc., but here we
  mostly use small integers as semitone offsets from a root.
- A "pc-set" is a frozenset of pitch classes.
- A "voicing" is a tuple of *pitches* (ordered), e.g. (0, 4, 7), (0, 7, 12).
- A "chord node" in the graph is usually an int-indexed entry referring to a
  voicing or a pc-set.

The module ends with doctests so you can quickly verify that things work.

Author: (your name)
"""

from __future__ import annotations

from itertools import combinations, product
from typing import (
    Iterable,
    Iterator,
    List,
    Tuple,
    Callable,
    Dict,
    Any,
    Sequence,
    Set,
    FrozenSet,
    Optional,
)


# ---------------------------------------------------------------------------
# 1. PITCH-CLASS COMBINATIONS (THEORETICAL, ORDERLESS)
# ---------------------------------------------------------------------------


def pc_combinations(
    k: int,
    pcs: Sequence[int] = tuple(range(12)),
) -> List[FrozenSet[int]]:
    """
    Enumerate all k-element pitch-class combinations from given pitch classes.

    This corresponds to the "dumb upper bound" level:
    choose k from 12, ignore order and octave.

    Args:
        k: number of pitch classes to choose (e.g. 3, 4, 5).
        pcs: iterable of pitch classes to choose from (default 0..11).

    Returns:
        List of frozensets, each a k-element pc-set.

    >>> len(pc_combinations(3, range(12)))
    220
    >>> frozenset({0, 4, 7}) in pc_combinations(3)
    True
    """
    return [frozenset(c) for c in combinations(pcs, k)]


def all_pc_combinations(
    sizes: Iterable[int] = (3, 4, 5),
    pcs: Sequence[int] = tuple(range(12)),
) -> List[FrozenSet[int]]:
    """
    Enumerate all pitch-class combinations for the given sizes.

    >>> combos = all_pc_combinations((3, 4))
    >>> len(combos)  # 220 + 495 = 715
    715
    >>> frozenset({0, 3, 7}) in combos
    True
    """
    out: List[FrozenSet[int]] = []
    for k in sizes:
        out.extend(pc_combinations(k, pcs))
    return out


# ---------------------------------------------------------------------------
# 2. VOICING ENUMERATION IN A BOUNDED RANGE
# ---------------------------------------------------------------------------


def interval_stack_voicings(
    root: int = 0,
    max_semitones: int = 24,
    allowed_intervals: Sequence[int] = (1, 2, 3, 4, 5, 7, 8, 9, 12),
    max_notes: int = 5,
    min_notes: int = 2,
) -> List[Tuple[int, ...]]:
    """
    Enumerate voicings by *stacking intervals* above a root, staying within
    `max_semitones`.

    The algorithm:
        - start with [root]
        - at each step add one of allowed_intervals to the *last* pitch
        - stop when adding any allowed interval would go past max_semitones
        - keep sequences whose length is between min_notes and max_notes

    This is *exactly* the "fixed root, bounded range, interval stacking"
    approach you described.

    Args:
        root: base pitch (0 means 'C' abstractly).
        max_semitones: highest allowed pitch = root + max_semitones.
        allowed_intervals: intervals (in semitones) you can stack.
        max_notes: maximum size of the voicing.
        min_notes: minimum size of the voicing.

    Returns:
        List of tuples, each a voicing like (0, 4, 7) or (0, 5, 9, 12).

    >>> v = interval_stack_voicings(
    ...     root=0,
    ...     max_semitones=12,
    ...     allowed_intervals=(3, 4, 5),
    ...     max_notes=4,
    ...     min_notes=3,
    ... )
    >>> (0, 4, 7) in v or (0, 3, 7) in v
    True
    """
    results: List[Tuple[int, ...]] = []

    def _recur(current: List[int]) -> None:
        if min_notes <= len(current) <= max_notes:
            results.append(tuple(current))
        if len(current) >= max_notes:
            return
        last = current[-1]
        for iv in allowed_intervals:
            nxt = last + iv
            if nxt - root > max_semitones:
                continue
            current.append(nxt)
            _recur(current)
            current.pop()

    _recur([root])
    return results


def expand_with_duplicates(
    base_voicing: Tuple[int, ...],
    max_duplicates: int = 1,
    within: Tuple[int, int] = (0, 24),
) -> List[Tuple[int, ...]]:
    """
    Given a voicing like (0, 4, 7), add (at most) `max_duplicates` extra notes
    that duplicate existing pitch classes in nearby octaves.

    This models the real-life situation where pianists double the root or the
    fifth.

    Args:
        base_voicing: base tuple of pitches (sorted, ascending).
        max_duplicates: how many extra notes to add at most.
        within: (lo, hi) absolute pitch bounds.

    Returns:
        List of voicings, including the original one.

    >>> expand_with_duplicates((0, 4, 7), max_duplicates=1, within=(0, 12))
    [(0, 4, 7), (0, 4, 7, 12)]
    """
    base = tuple(sorted(base_voicing))
    out = [base]

    # Find candidate duplicates: transpose existing notes by octaves
    candidates: List[int] = []
    for p in base:
        for octv in range(-2, 5):  # generous
            cand = p + 12 * octv
            if within[0] <= cand <= within[1] and cand not in base:
                candidates.append(cand)

    # pick up to max_duplicates from candidates
    for r in range(1, max_duplicates + 1):
        for extra in combinations(candidates, r):
            new_v = tuple(sorted(base + extra))
            out.append(new_v)

    return out


# ---------------------------------------------------------------------------
# 3. LINKING / GRAPH CONSTRUCTION
# ---------------------------------------------------------------------------


def shared_pcs(a: Tuple[int, ...], b: Tuple[int, ...]) -> int:
    """
    Number of shared pitch classes between two voicings.

    >>> shared_pcs((0, 4, 7), (0, 7, 11))
    2
    """
    return len({x % 12 for x in a}.intersection({y % 12 for y in b}))


def voice_leading_distance(a: Tuple[int, ...], b: Tuple[int, ...]) -> int:
    """
    A dumb voice-leading distance: compare two voicings of (possibly) the same
    length, and sum absolute differences between *best-matched* notes.

    For simplicity, if lengths differ, we match up to the min length.

    This is *not* Tymoczko's metric, but good enough for building edges.

    >>> voice_leading_distance((0, 4, 7), (0, 5, 7))
    1
    """
    la, lb = len(a), len(b)
    m = min(la, lb)
    # naive: sort and zip
    sa = sorted(a)[:m]
    sb = sorted(b)[:m]
    return sum(abs(x - y) for x, y in zip(sa, sb))


def is_subset_pcs(a: Tuple[int, ...], b: Tuple[int, ...]) -> bool:
    """
    True if pc(a) is subset of pc(b).

    >>> is_subset_pcs((0, 4, 7), (0, 2, 4, 7, 9))
    True
    >>> is_subset_pcs((0, 4, 7), (1, 4, 7))
    False
    """
    return {x % 12 for x in a}.issubset({y % 12 for y in b})


def is_codiatonic(
    a: Tuple[int, ...],
    b: Tuple[int, ...],
    scale_quality: Sequence[int] = (0, 2, 4, 5, 7, 9, 11),
    *,
    tonic: Optional[int] = None,
) -> bool:
    """
    Return True if the union of the pitch classes of chords `a` and `b`
    can be embedded in a single scale derived from the given `scale_quality`.

    If `tonic` is provided (0–11), only test that transposition of the scale;
    otherwise, test all 12 possible transpositions.

    Args:
        a: chord as a tuple of pitches (any integers)
        b: chord as a tuple of pitches (any integers)
        scale_quality: sequence of pitch-class intervals for the scale (default: major)
        tonic: if not None, only use this tonic (0-11), else try all 12 transpositions

    Returns:
        True if union of a and b's pitch classes is a subset of any transposition of the scale.

    >>> is_codiatonic((0, 4, 7), (2, 5, 9))  # e.g. C major triad + D minor triad, both in C major
    True
    >>> is_codiatonic((0, 4, 7), (1, 5, 8))  # No two major triads a semitone apart in major scales...
    False
    >>> is_codiatonic((0, 4, 7), (1, 5, 8), scale_quality=(0,2,3,5,7,8,11))  # ... but in a harmonic minor, there are
    True
    >>> is_codiatonic((0, 4, 7), (1, 4, 8), tonic=0)  # Only test C major scale
    False
    >>> is_codiatonic((0, 4, 7), (1, 4, 8), tonic=1)  # Only test C# major scale
    False
    >>> is_codiatonic((0, 4, 7), (2, 5, 9), tonic=0)  # C major scale, C and Dm triads
    True
    """
    pcs_union = {x % 12 for x in a} | {y % 12 for y in b}
    scale_quality_set = set(x % 12 for x in scale_quality)
    # Precompute all 12 transpositions of the scale as sets
    if tonic is not None:
        tonics = [tonic % 12]
    else:
        tonics = list(range(12))
    for t in tonics:
        scale_pcs = {(p + t) % 12 for p in scale_quality_set}
        if pcs_union.issubset(scale_pcs):
            return True
    return False


def build_graph(
    voicings: List[Tuple[int, ...]],
    *,
    min_shared_pcs: int = 2,
    max_vl_distance: Optional[int] = None,
    include_subset_edges: bool = True,
) -> Dict[int, List[int]]:
    """
    Build an adjacency list over voicings using several criteria.

    A directed edge i -> j is created if ANY of the following are true:
      - shared PCs >= min_shared_pcs
      - voice-leading distance <= max_vl_distance (if given)
      - i is pc-subset of j (if include_subset_edges)

    Args:
        voicings: list of voicings (each is a tuple of ints)
        min_shared_pcs: minimum shared pitch classes to create an edge
        max_vl_distance: max voice-leading distance, or None to ignore
        include_subset_edges: whether to link subset -> superset

    Returns:
        Dict[node_index, List[node_index]]

    >>> V = [(0, 4, 7), (0, 5, 7), (0, 4, 7, 11)]
    >>> G = build_graph(V, min_shared_pcs=2)
    >>> sorted(G[0])
    [1, 2]
    """
    n = len(voicings)
    adj: Dict[int, List[int]] = {i: [] for i in range(n)}

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            a = voicings[i]
            b = voicings[j]
            add_edge = False

            if shared_pcs(a, b) >= min_shared_pcs:
                add_edge = True

            if (max_vl_distance is not None) and voice_leading_distance(
                a, b
            ) <= max_vl_distance:
                add_edge = True

            if include_subset_edges and is_subset_pcs(a, b):
                add_edge = True

            if add_edge:
                adj[i].append(j)

    return adj


# ---------------------------------------------------------------------------
# 4. HIGHER-LEVEL GENERATORS
# ---------------------------------------------------------------------------


def generate_default_voicing_space() -> List[Tuple[int, ...]]:
    """
    Generate a reasonably rich but still small voicing space:

    - root = 0 (C)
    - range = 24 semitones (two octaves)
    - allowed intervals = 2, 3, 4, 5, 7
    - 3 to 5 notes
    - plus optional duplications

    >>> V = generate_default_voicing_space()
    >>> isinstance(V, list) and len(V) > 50
    True
    """
    base = interval_stack_voicings(
        root=0,
        max_semitones=24,
        allowed_intervals=(2, 3, 4, 5, 7),
        max_notes=5,
        min_notes=3,
    )
    # optionally expand some of them with duplicates
    expanded: List[Tuple[int, ...]] = []
    for v in base:
        expanded.extend(expand_with_duplicates(v, max_duplicates=1, within=(0, 24)))
    # deduplicate
    uniq = sorted(set(expanded))
    return uniq


def generate_graph_default() -> Dict[int, List[int]]:
    """
    Convenience: generate a default voicing space and link it.

    >>> G = generate_graph_default()  # doctest: +SKIP
    >>> len(G) > 50  # doctest: +SKIP
    True
    """
    V = generate_default_voicing_space()
    G = build_graph(
        V,
        min_shared_pcs=2,
        max_vl_distance=3,
        include_subset_edges=True,
    )
    return G


# ---------------------------------------------------------------------------
# 5. NOTES ON EXTENSIONS (not code, but pointers)
# ---------------------------------------------------------------------------
# - To include *all 12 transpositions*, just add 0..11 to every pitch.
# - To include *different roots*, call interval_stack_voicings with root=0..11
#   and merge the results.
# - To restrict to "actual" tonal chord qualities, prefilter voicings whose
#   pitch classes match {0,4,7}, {0,3,7}, {0,4,7,11}, etc.
# - To get Forte-style pc-set categories, you’d add a normalization function
#   that maps pitch-class sets to prime form and use that as node label.


# ---------------------------------------------------------------------------
# CHORD TABLES AND LINK COMPUTATION
# ---------------------------------------------------------------------------

# Global configuration for computation warnings
DEFAULT_WARNING_THRESHOLD = 10000  # warn if processing more than this many combinations


def _warn_if_large_computation(
    n: int, threshold: int = DEFAULT_WARNING_THRESHOLD
) -> None:
    """Warn user if computation might take a while."""
    if n > threshold:
        print(f"⚠️  Processing {n:,} items. This may take a while...", flush=True)


def chord_table(
    *,
    voicings: Optional[List[Tuple[int, ...]]] = None,
    id_col: str = "id_",
    index_by: str = "int",
    include_links: bool = False,
    link_kinds: Optional[List[str]] = None,
    use_pandas: bool = True,
    warning_threshold: int = DEFAULT_WARNING_THRESHOLD,
    **link_kwargs,
):
    """
    Build a chord table with one row per chord.

    By default, generates the default voicing space from chordspace.
    Each row describes the chord's internal features: voicing, number of notes,
    span, pitch-class set, and interval vector.

    If `include_links` is True, link columns are added listing linked chord IDs
    according to the specified link kinds.

    Args:
        voicings: list of chord tuples (if None, use generate_default_voicing_space()).
        id_col: name of the unique ID column.
        index_by: how to compute chord IDs ("int", "hash", or "repr").
        include_links: whether to add link columns.
        link_kinds: types of links to compute if include_links is True
            (e.g., ["shared", "subset", "voiceleading"]).
        use_pandas: return DataFrame if True, otherwise yield dicts.
        warning_threshold: threshold for warning about large computations.
        **link_kwargs: passed to compute_links for each link kind.

    Returns:
        pandas.DataFrame if use_pandas else generator of dicts

    >>> table = list(chord_table(
    ...     voicings=[(0, 4, 7), (0, 3, 7), (0, 4, 7, 11)],
    ...     use_pandas=False
    ... ))
    >>> len(table)
    3
    >>> table[0]['n_notes']
    3
    >>> table[0]['span']
    7
    """
    # 1. Get voicings
    if voicings is None:
        voicings = generate_default_voicing_space()

    _warn_if_large_computation(len(voicings), warning_threshold)

    # 2. Assign IDs based on index_by strategy
    ids = _generate_ids(voicings, index_by)

    # 3. Generate chord feature rows
    rows = list(_chord_feature_rows(voicings, ids, id_col))

    # 4. Add links if requested
    if include_links:
        if link_kinds is None:
            link_kinds = ["shared"]  # default to shared PC links

        for kind in link_kinds:
            _warn_if_large_computation(
                len(rows) * len(rows),
                warning_threshold * 100,  # pairwise is more expensive
            )
            links = compute_links(rows, id_col=id_col, kind=kind, **link_kwargs)
            for row, link_list in zip(rows, links):
                row[f"{kind}_links"] = link_list

    # 5. Produce output
    if use_pandas:
        import pandas as pd

        return pd.DataFrame(rows)
    else:
        return (row for row in rows)


def _generate_ids(voicings: List[Tuple[int, ...]], index_by: str) -> List:
    """Generate IDs for voicings based on indexing strategy."""
    if index_by == "int":
        return list(range(len(voicings)))
    elif index_by == "hash":
        import hashlib

        return [
            int(hashlib.sha1(str(v).encode()).hexdigest(), 16) % (10**12)
            for v in voicings
        ]
    elif index_by == "repr":
        return [repr(v) for v in voicings]
    else:
        raise ValueError(
            f"Unknown index_by mode: {index_by}. " "Must be 'int', 'hash', or 'repr'."
        )


def _chord_feature_rows(
    voicings: List[Tuple[int, ...]], ids: List, id_col: str
) -> Iterator[Dict[str, Any]]:
    """Generate chord feature dicts for each voicing."""
    for chord_id, voicing in zip(ids, voicings):
        yield _chord_features(chord_id, voicing, id_col)


def _chord_features(chord_id, voicing: Tuple[int, ...], id_col: str) -> Dict[str, Any]:
    """Extract features from a single chord voicing."""
    pcs = sorted({p % 12 for p in voicing})
    n_notes = len(voicing)

    # Interval vector: count each interval class (1-6) in the pc-set
    interval_vector = _compute_interval_vector(pcs)

    return {
        id_col: chord_id,
        "voicing": voicing,
        "n_notes": n_notes,
        "span": max(voicing) - min(voicing) if n_notes > 1 else 0,
        "pitch_classes": pcs,
        "n_pcs": len(pcs),
        "interval_vector": interval_vector,
    }


def _compute_interval_vector(pcs: List[int]) -> List[int]:
    """
    Compute the interval vector for a pitch-class set.

    The interval vector counts occurrences of each interval class (1-6).
    """
    return [
        sum(1 for x in pcs for y in pcs if 0 < (y - x) % 12 == ic) for ic in range(1, 7)
    ]


def compute_links(
    chord_table,
    *,
    id_col: str = "id_",
    kind: str = "shared",
    min_shared_pcs: int = 2,
    max_vl_distance: int = 3,
    warning_threshold: int = DEFAULT_WARNING_THRESHOLD,
) -> List[List]:
    """
    Compute links between chords based on chosen criteria.

    Args:
        chord_table: list of dicts or DataFrame describing chords.
        id_col: name of chord ID column.
        kind: link definition - either a string or callable:
            String options:
            - "shared": share >= min_shared_pcs pitch classes
            - "subset": subset relation in pitch-class space
            - "voiceleading": voice-leading distance <= max_vl_distance
            - "codiatonic": both chords fit in same major scale

            Callable: custom function with signature:
                (i: int, j: int, voicings: List, pc_sets: List, **kwargs) -> bool
                where i, j are chord indices, voicings is list of tuples,
                pc_sets is list of pitch-class sets, and kwargs includes
                min_shared_pcs and max_vl_distance
        min_shared_pcs: threshold for 'shared' links
        max_vl_distance: max distance for 'voiceleading' links
        warning_threshold: threshold for warning about large computations

    Returns:
        List of lists of chord IDs (parallel to input rows)

    >>> rows = [
    ...     {'id_': 0, 'voicing': (0, 4, 7), 'pitch_classes': [0, 4, 7]},
    ...     {'id_': 1, 'voicing': (0, 5, 7), 'pitch_classes': [0, 5, 7]},
    ...     {'id_': 2, 'voicing': (0, 4, 7, 11), 'pitch_classes': [0, 4, 7, 11]},
    ... ]
    >>> links = compute_links(rows, kind="shared", min_shared_pcs=2)
    >>> len(links[0]) >= 1  # first chord should link to others
    True
    """
    # Normalize to list of dicts
    if hasattr(chord_table, "to_dict"):
        rows = chord_table.to_dict("records")
    else:
        rows = list(chord_table)

    n = len(rows)
    _warn_if_large_computation(n * n, warning_threshold * 100)

    # Extract relevant data
    voicings = [tuple(r["voicing"]) for r in rows]
    ids = [r[id_col] for r in rows]

    # Precompute pitch-class sets for efficiency
    pc_sets = [{p % 12 for p in v} for v in voicings]

    # Build link function based on kind
    link_func = _get_link_function(
        kind,
        pc_sets=pc_sets,
        min_shared_pcs=min_shared_pcs,
        max_vl_distance=max_vl_distance,
    )

    # Compute links
    all_links = [
        [ids[j] for j in range(n) if i != j and link_func(i, j, voicings)]
        for i in range(n)
    ]

    return all_links


def _get_link_function(
    kind,
    *,
    pc_sets: List[Set[int]],
    min_shared_pcs: int,
    max_vl_distance: int,
) -> Callable[[int, int, List[Tuple[int, ...]]], bool]:
    """
    Create a link function based on the specified kind.

    Args:
        kind: Either a string name ("shared", "subset", "voiceleading", "codiatonic")
              or a callable with signature (i: int, j: int, voicings, pc_sets, **kwargs) -> bool
        pc_sets: Precomputed pitch-class sets for efficiency
        min_shared_pcs: Threshold for 'shared' links
        max_vl_distance: Max distance for 'voiceleading' links

    Returns:
        A link function with signature (i: int, j: int, voicings: List[Tuple]) -> bool
    """
    # If it's already a callable, wrap it to provide pc_sets
    if callable(kind):

        def link_func(i: int, j: int, voicings: List[Tuple[int, ...]]) -> bool:
            return kind(
                i,
                j,
                voicings,
                pc_sets,
                min_shared_pcs=min_shared_pcs,
                max_vl_distance=max_vl_distance,
            )

        return link_func

    # Otherwise, look up by name
    if kind == "shared":

        def link_func(i: int, j: int, voicings: List[Tuple[int, ...]]) -> bool:
            return len(pc_sets[i] & pc_sets[j]) >= min_shared_pcs

    elif kind == "subset":

        def link_func(i: int, j: int, voicings: List[Tuple[int, ...]]) -> bool:
            return pc_sets[i].issubset(pc_sets[j])

    elif kind == "voiceleading":

        def link_func(i: int, j: int, voicings: List[Tuple[int, ...]]) -> bool:
            return voice_leading_distance(voicings[i], voicings[j]) <= max_vl_distance

    elif kind == "codiatonic":

        def link_func(i: int, j: int, voicings: List[Tuple[int, ...]]) -> bool:
            return is_codiatonic(voicings[i], voicings[j])

    else:
        raise ValueError(
            f"Unknown link kind: {kind}. "
            "Must be 'shared', 'subset', 'voiceleading', 'codiatonic', or a custom callable."
        )

    return link_func


# if __name__ == "__main__":
#     import doctest

#     doctest.testmod()
