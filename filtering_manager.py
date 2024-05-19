from video_manager import video_manager
from  detect_nude import detect_nude
import threading
import cv2
class filtering_manager:

    def __init__(self, vm: video_manager, sample_rate=10):
        self.video = vm
        self.detector = detect_nude(sample_rate)
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
    
    def return_filtered_frames(self, mask, path):
        all_frames = []
        print((self.video.width,self.video.height))
        video = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'mp4v'), self.video.fps, (1920, 1080))
        for i in mask:
            sec, frames = self.video.stream()
            if frames is None or len(frames) == 0:
                return all_frames
            framesToApped = frames if i == True else self.make_blured_frames(frames)
            for frame in framesToApped:
                video.write(frame)
        video.release()

    def make_blured_frames(self, frames):
        for i in range(len(frames)):
            if frames[i] is not None:
                # make max blur
                frames[i] = cv2.GaussianBlur(frames[i], (185, 185), 0)
        return frames

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
        return thread

        