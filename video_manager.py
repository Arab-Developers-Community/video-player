import cv2

class video_manager:
    def __init__(self, path):
        self.path = path
        self.video = cv2.VideoCapture(path)
        self.frame_count = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.video.get(cv2.CAP_PROP_FPS))
        self.stream_mode = False


    def read_frames(self, second):
        if self.stream_mode:
            raise Exception("Cannot read frames while in stream mode")
        self.video.set(cv2.CAP_PROP_POS_FRAMES, second * self.fps)
        return self._read_sec()[1]
    
    def _read_sec(self):
        frames = []
        for i in range(self.fps):
            ret, frame = self.video.read()
            if ret:
                frames.append(frame)
            else:
                break
        return 1, frames
    
    def stream(self):
        self.stream_mode = True
        return self._read_sec()
    
    def stream_frames(self):
        ret, frame = self.video.read()
        if ret:
            return frame

    def stop_stream(self):
        self.stream_mode = False
        self.video.release()

    def get_frame_time(self):
        return 1000 / self.fps
    
    def get_current_second(self):
        return int(self.video.get(cv2.CAP_PROP_POS_FRAMES) / self.fps)