from video_manager import video_manager
from  detect_nude import detect_nude
import threading

class filtering_manager:

    def __init__(self, vm: video_manager):
        self.video = vm
        self.detector = detect_nude({})
        self.lock = threading.Lock()
        self.state = []
        self.is_done = False
        self.secondsToSkip = 10

    def startfiltering(self: video_manager):
        while not self.is_done:
            self.filter()

    def filter(self):
        sec, frames = self.video.stream()
        if frames is None or len(frames) == 0:
            self.is_done = True
            return None
        results = self.detector.detect(frames)
        if results:
            self.update_state(self.state+[True])
        else:
            self.skip_seconds(self.secondsToSkip)

        return self.detector.detect(frames)
    
    def skip_seconds(self, seconds):
        new_state = [False] * seconds
        self.update_state(self.state+new_state)
        # seek to the next 10 seconds
        for i in range(seconds):
            self.video.stream()

    def update_state(self, state):
        self.lock.acquire()
        self.state = state
        self.lock.release()

    def read_state(self):
        self.lock.acquire()
        state = self.state
        self.lock.release()
        return state
    
    def startSyncThread(self):
        thread = threading.Thread(target=self.startfiltering)
        thread.start()

        