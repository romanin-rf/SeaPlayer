try:
    from .MP3 import MP3Codec
    from .OGG import OGGCodec
    from .WAV import WAVECodec
    from .MIDI import MIDICodec
    from .FLAC import FLACCodec

    codecs = [ MP3Codec, OGGCodec, WAVECodec, MIDICodec, FLACCodec ]
except:
    codecs = []
