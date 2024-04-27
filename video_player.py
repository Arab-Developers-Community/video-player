import tkinter as tk
from tkinter import ttk
import cv2
import threading
import queue
from PIL import Image, ImageTk


class VideoPlayer:
    def __init__(self, root, video):
        self.root = root
        self.root.title("Video Player")
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.video_label = ttk.Label(self.frame)
        self.video_label.pack()
        self.video_capture = cv2.VideoCapture(video)
        self.frame_count = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.buffer = queue.Queue()
        self.frames_displayed = 0

        self.create_threads()
        self.update()

    def update(self):

        if self.frames_displayed == self.frame_count:
            # If the video ends, you can add logic to handle this event
            self.video_capture.release()

        self.display_frame(cv2.cvtColor(self.buffer.get(), cv2.COLOR_BGR2RGB))
        self.frames_displayed = self.frames_displayed + 1

        self.root.after(33, self.update)

    def start_checking(self, lock):
        while True:
            lock.acquire()

            ret, frame = self.video_capture.read()

            if ret:
                # this code to detect nudity **NEED TO BE UPDATED
                self.buffer.put(frame)
                ##################################################
            else:
                # If the video ends, you can add logic to handle this event
                threading.current_thread().join()

            lock.release()

    def create_threads(self, threads_num=4):
        lock = threading.Lock()
        for i in range(0, threads_num):
            thread = threading.Thread(target=VideoPlayer.start_checking , args=(self,lock,))
            thread.start()

    def display_frame(self, frame):
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=image)
        self.video_label.config(image=photo)
        self.video_label.image = photo


if __name__ == "__main__":
    root = tk.Tk()
    player = VideoPlayer(root, "video.mp4")
    root.mainloop()