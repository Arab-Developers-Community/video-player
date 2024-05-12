from pydub.utils import make_chunks
from pydub import AudioSegment
import os
import pyaudio

import threading
class audio_manager:

    def __init__(self, path, shouldCensorCallback):
        self.path = path
        self.shouldCensorCallback = shouldCensorCallback

        self.audio = self.setup_audo_lib().from_file(path, "mp4")
        empty_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "empty-track.wav")
        self.empty = self.setup_audo_lib().from_file(empty_path, "wav")

    def setup_audo_lib(self):
        AudioSegment.converter = "{}\\ffmpeg\\bin\\ffmpeg.exe".format(os.getcwd())
        AudioSegment.ffmpeg = "{}\\ffmpeg\\bin\\ffmpeg.exe".format(os.getcwd())
        AudioSegment.ffprobe ="{}\\ffmpeg\\bin\\ffprobe.exe".format(os.getcwd())
        print(AudioSegment.converter, AudioSegment.ffmpeg, AudioSegment.ffprobe)
        return AudioSegment

    def play(self):
        self._play_audio(self.audio, self.empty)


    def startSyncThread(self):
        thread = threading.Thread(target=self.play)
        thread.start()

    def _play_audio(self, seg, empty):
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(seg.sample_width),
                        channels=seg.channels,
                        rate=seg.frame_rate,
                        output=True)
        empty_chunk = make_chunks(empty, 1000)[0]
        try:
            for index, chunk in enumerate(make_chunks(seg, 1000)):
                    if self.shouldCensorCallback(index):
                        stream.write(chunk._data)
                    else:
                        stream.write(empty_chunk._data)
        finally:
            stream.stop_stream()
            stream.close()

            p.terminate()