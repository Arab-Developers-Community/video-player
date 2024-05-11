class video_manager:
    def __init__(self, path):
        self.path = path
        self.video = cv2.VideoCapture(path)
        self.frame_count = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.video.get(cv2.CAP_PROP_FPS))


    def read_frames(self, second):
        self.video.set(cv2.CAP_PROP_POS_FRAMES, second * self.fps)
        frames = []
        for i in range(self.fps):
            ret, frame = self.video.read()
            if ret:
                frames.append(frame)
            else:
                break
        return frames
    
    
