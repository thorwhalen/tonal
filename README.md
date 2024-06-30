
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

![image](https://github.com/thorwhalen/sonify/assets/1906276/49e1002c-fbb6-47d8-b642-aaf46b218e0b)


Change the way the chords are played, and what the name (really, filepath) of the 
midi and wav files produce are.

```python
from tonal.chords import play_arpeggio

Sound.from_file(
    chords_to_wav(chord_sequence, name='test_arpeggio', render_chord=play_arpeggio)
).display()
```

![image](https://github.com/thorwhalen/sonify/assets/1906276/0f046317-3965-4544-ae4b-288a0762ec4d)

