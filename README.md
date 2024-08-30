
# tonal
Tools for music analysis and generation


To install:	```pip install tonal```


# Examples

## chords


```python
from tonal import chords_to_wav

chord_sequence = [
    ('Bdim', 120),
    ('Em11', 120),
    ('Amin9', 120),
    ('Dm7', 120),
    'G7',
    'Cmaj7',
]

wav_filepath = chords_to_wav(chord_sequence)

```

If you have [hum](https://pypi.org/project/hum/) you can use it to diplay (and hear) 
the sound:

```python
from hum import Sound
Sound.from_file(wav_filepath).display()
```

![image](https://github.com/thorwhalen/sonification/assets/1906276/49e1002c-fbb6-47d8-b642-aaf46b218e0b)


Change the way the chords are played, and what the name (really, filepath) of the 
midi and wav files produce are.

```python
from tonal.chords import play_arpeggio

Sound.from_file(
    chords_to_wav(chord_sequence, name='test_arpeggio', render_chord=play_arpeggio)
).display()
```

![image](https://github.com/thorwhalen/sonification/assets/1906276/0f046317-3965-4544-ae4b-288a0762ec4d)


## counterpoint

```python
The `translate_in_scale` allows you to translate a sequence of notes, or multiple 
tracks of notes by the given number of steps within the given scale.

>>> stream = translate_in_scale(['C4', 'E4', 'B3', 'C4'], -2, 'C')
>>> stream  # doctest: +ELLIPSIS
<music21.stream.Stream ...>
>>> note_names(stream)
['A3', 'C4', 'G3', 'A3']

For multiple tracks:

>>> tracks = [['C4', 'E4', 'G4'], ['A4', 'C5', 'E5']]
>>> translated_tracks = translate_in_scale(tracks, -2, 'C')
>>> multi_note_names(translated_tracks)
[['A3', 'C4', 'E4'], ['F4', 'A4', 'C5']]

Using some other scales:

With a E major scale:

>>> tracks = [['E4', 'G#4', 'B4'], ['C#5', 'E5', 'G#5']]
>>> translated_tracks = translate_in_scale(tracks, 1, 'E')
>>> multi_note_names(translated_tracks)
[['F#4', 'A4', 'C#5'], ['D#5', 'F#5', 'A5']]

With a D flat major scale:

>>> tracks = [['Db4', 'F4', 'Ab4'], ['Bb4', 'Db5', 'F5']]
>>> translated_tracks = translate_in_scale(tracks, -3, 'Db')
>>> multi_note_names(translated_tracks)
[['A-3', 'C4', 'E-4'], ['F4', 'A-4', 'C5']]

Now let's use a different, "custom" scale, as well as demonstrate the use
of a partial function to get a translator with a fixed input scale:

>>> from functools import partial
>>> from music21.scale import HarmonicMinorScale
>>> translate = partial(
...     translate_in_scale, input_scale='A', scale_creator=HarmonicMinorScale
... )
>>> tracks = [['A4', 'C5', 'E5'], ['G#5', 'A5', 'C6']]
>>> translated_tracks = translate(tracks, 2)
>>> multi_note_names(translated_tracks)
[['C5', 'E5', 'G#5'], ['B5', 'C6', 'E6']]
```

Let's make a four part cycling V-I progression.

```python
from tonal.counterpoint import translate_in_scale, create_score_from_tracks
from tonal.util import play_music21_object

motif = [
    "C4 C4".split(),
    "E4 E4".split(),
    "G4 F4".split(),
    "B4 A4".split(),
]

tracks = translate_in_scale(motif, range(7, -14, -1), 'C')
score = create_score_from_tracks(tracks)
score.show()
play_music21_object(score)
```

<img width="653" alt="image" src="https://github.com/thorwhalen/tonal/assets/1906276/95f14372-e711-4fb5-8024-4692cd25956a">
