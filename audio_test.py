from pydub.utils import make_chunks
from pydub import AudioSegment
import os
import threading
import time
import pyaudio

def setup_audo_lib():
    AudioSegment.converter = "{}\\ffmpeg\\bin\\ffmpeg.exe".format(os.getcwd())
    AudioSegment.ffmpeg = "{}\\ffmpeg\\bin\\ffmpeg.exe".format(os.getcwd())
    AudioSegment.ffprobe ="{}\\ffmpeg\\bin\\ffprobe.exe".format(os.getcwd())
    print(AudioSegment.converter, AudioSegment.ffmpeg, AudioSegment.ffprobe)
    return AudioSegment

audio = setup_audo_lib().from_file("C:\\Users\\ibrah\\Downloads\\xx.mp4", "mp4")
empty = setup_audo_lib().from_file("C:\\Users\\ibrah\\Desktop\\video-player\\empty-track.wav", "wav")

five_seconds = 5 * 1000
ten_seconds = 10 * 1000
five_seconds_audio = audio[:five_seconds]
ten_seconds_audio = audio[five_seconds:ten_seconds]

def play_audio(seg, empty):
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(seg.sample_width),
                    channels=seg.channels,
                    rate=seg.frame_rate,
                    output=True)
    empty_chunk = make_chunks(empty, 500)[0]
    alt = False
    # Just in case there were any exceptions/interrupts, we release the resource
    # So as not to raise OSError: Device Unavailable should play() be used again
    try:
        # break audio into half-second chunks (to allows keyboard interrupts)
        for chunk in make_chunks(seg, 500):
            if alt:
                stream.write(chunk._data)
            else:
                stream.write(empty_chunk._data)
            alt = not alt
    finally:
        stream.stop_stream()
        stream.close()

        p.terminate()

play_audio(five_seconds_audio, empty)