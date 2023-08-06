MML Parser and Player for Python
================================

Python-based MML ([Music Macro Language](https://en.wikipedia.org/wiki/Music_Macro_Language)) parser and player.


Installation
------------

    pip install mmlparser
    

Examples
--------

Examples, as well as simple songs written in MML, can be found in the
directory `mmlparser/examples`, which can be played directly from a command
line.

    python -m mmlparser.examples.simple_player

To actually play the song, install `pyrtmidi` and make sure at least one MIDI
output is available.  The notes will be sent to the MIDI out device.

    pip install rtmidi
    python -m mmlparser.examples.simple_player

The code in `examples/simple_player.py` plays musical notes with
`MMLParser.play()` method, which relies on the blocking `time.sleep()`
function.  The async version, `MMLParser.aplay()`, may be used to play music
concurrently with other asyncio tasks.  See `examples/async_player.py` for
some examples.

    python -m mmlparser.examples.async_player

Limitations
-----------

* Triplets are not yet supported.
* User event and repeat commands are not supported.