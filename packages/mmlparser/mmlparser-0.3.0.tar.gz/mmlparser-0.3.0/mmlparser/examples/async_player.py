from mmlparser import MMLParser
from .songs import HAPPY_BIRTHDAY
import asyncio

try:
    import rtmidi
    midi = rtmidi.RtMidiOut()
    midi.openPort(0)
    midiMsg = rtmidi.MidiMessage()
except:
    print("Cannot open MIDI OUT; perform dry run")
    midi = None

def callback(channel,evt,note,vel):
    if evt == "on":
        if midi:
            midi.sendMessage(midiMsg.noteOn(channel+1,note,vel))
        print("CH{}: plays note {} with vel={}"
                .format(channel,note,vel))
    elif evt == "off":
        if midi:
            midi.sendMessage(midiMsg.noteOff(channel+1,note))
        print("CH{}: stops".format(channel))

parser = MMLParser(2,callback)
loop = asyncio.get_event_loop()
loop.run_until_complete(parser.aplay(*HAPPY_BIRTHDAY))

if midi:
    del midi

