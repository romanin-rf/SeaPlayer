import os
import pytest
import asyncio
try:
    from seaplayer.codecs import (
        MP3Codec,
        OGGCodec,
        WAVECodec,
        MIDICodec,
        FLACCodec
    )
    CODECS_IMPORTED = True
except:
    CODECS_IMPORTED = False

# ! Vars
LOCAL_DIRPATH = os.path.dirname(__file__)

# ! Getting
def get_clibration_filepath(filename: str) -> str:
    return os.path.join(LOCAL_DIRPATH, "calibration_data", filename)

# ! Test Vars
mp3_file = get_clibration_filepath("test.mp3")
midi_file = get_clibration_filepath("test.mid")

# ! Tests
if CODECS_IMPORTED:
    # * MP3Codec Test
    def test_mp3_codec_is_this_codec():
        assert MP3Codec.is_this_codec(mp3_file)
        assert not MP3Codec.is_this_codec(midi_file)
    
    def test_mp3_codec_aio_is_this_codec():
        async def aio_test_mp3_codec_aio_is_this_codec():
            assert await MP3Codec.aio_is_this_codec(mp3_file)
            assert not await MP3Codec.aio_is_this_codec(midi_file)
        asyncio.run(aio_test_mp3_codec_aio_is_this_codec())
    
    def test_mp3_codec_sha1():
        mp3_sha1_t1 = MP3Codec(mp3_file).__sha1__(65536)
        mp3_sha1_t2 = MP3Codec(mp3_file).__sha1__(65536)
        assert mp3_sha1_t1 == mp3_sha1_t2
    
    def test_mp3_codec_aio_sha1():
        async def aio_test_mp3_codec_aio_sha1():
            return await MP3Codec(mp3_file).__aio_sha1__(65536), await MP3Codec(mp3_file).__aio_sha1__(65536)
        mp3_sha1_t1, mp3_sha1_t2 = asyncio.run(aio_test_mp3_codec_aio_sha1())
        assert mp3_sha1_t1 == mp3_sha1_t2
    
    # * MIDI Test
    def test_midi_codec_is_this_codec():
        assert not MIDICodec.is_this_codec(mp3_file)
        assert MIDICodec.is_this_codec(midi_file)
    
    def test_midi_codec_aio_is_this_codec():
        async def aio_test_midi_codec_aio_is_this_codec():
            assert not await MIDICodec.aio_is_this_codec(mp3_file)
            assert await MIDICodec.aio_is_this_codec(midi_file)
        asyncio.run(aio_test_midi_codec_aio_is_this_codec())
    
    def test_midi_codec_sha1():
        midi_sha1_t1 = MIDICodec(midi_file).__sha1__(65536)
        midi_sha1_t2 = MIDICodec(midi_file).__sha1__(65536)
        assert midi_sha1_t1 == midi_sha1_t2
    
    def test_midi_codec_aio_sha1():
        async def aio_test_midi_codec_aio_sha1():
            return \
                (await (await MIDICodec.__aio_init__(midi_file)).__aio_sha1__(65536)), \
                (await (await MIDICodec.__aio_init__(midi_file)).__aio_sha1__(65536))
        midi_sha1_t1, midi_sha1_t2 = asyncio.run(aio_test_midi_codec_aio_sha1())
        assert midi_sha1_t1 == midi_sha1_t2
