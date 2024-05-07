import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import customtkinter as ctk
import cv2
import threading
import queue
from detect_nude import detect_nude
import numpy as np 
from PIL import Image, ImageTk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class VideoPlayer:
    def __init__(self, video):
        self.root = ctk.CTk()
        self.window_height = self.root.winfo_screenheight()
        self.window_width = self.root.winfo_screenwidth()
        self.root.geometry("1080x800")
        self.root.title("Video Player")
        self.detector = detect_nude({'filter_nudes': True, 'filter_kissing': True})
        self.image_label = None
        self.video_file_path = None
        self.frame = None

        self.current_image = ctk.CTkImage(light_image=Image.open('assets/black.jpg'),
                                          dark_image=Image.open('assets/black.jpg'),
                                          size=(self.window_height, self.window_width))

        self.video_capture = cv2.VideoCapture(video)
        self.frame_count = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.video_capture.get(cv2.CAP_PROP_FPS))
        self.buffer = queue.Queue()
        self.frames_displayed = 0
        self.initialize_gui()
        self.create_threads()
        self.update()
        self.root.mainloop()

    def initialize_gui(self):
        self.frame = ctk.CTkFrame(master=self.root, corner_radius=15)
        self.frame.pack(pady=20, padx=40, fill='both', expand=True)
        button_browse = ctk.CTkButton(master=self.frame, text="Open Video", corner_radius=8, command=self.browse)
        button_browse.pack(pady=10, padx=10)
        self.image_label = ctk.CTkLabel(self.frame, text="", image=self.current_image)
        self.image_label.pack(pady=0, padx=0, fill='both', expand=True)

    def browse(self):
        f_path = askopenfilename(initialdir="/", title="Select File",
                                 filetypes=(("Video files", "*.mp4"), ("All Files", "*.*")))
        self.video_file_path = 'None' if f_path == '' else f_path

    def update(self):

        if self.frames_displayed == self.frame_count:
            # If the video ends, you can add logic to handle this event
            self.video_capture.release()
            quit(0)

        self.display_frame(cv2.cvtColor(self.buffer.get(), cv2.COLOR_BGR2RGB))
        self.frames_displayed = self.frames_displayed + 1

        self.root.after(1, self.update)

    def start_checking(self, lock):
        while True:
            lock.acquire()

            ret, frame = self.video_capture.read()
            image = Image.fromarray(frame)
            if ret:
                # this code to detect nudity **NEED TO BE UPDATED
                if self.detector.detect(image):
                    self.buffer.put(frame)
                ##################################################
            else:
                # If the video ends, you can add logic to handle this event
                threading.current_thread().join()

            lock.release()

    def create_threads(self, threads_num=1):
        lock = threading.Lock()
        for i in range(0, threads_num):
            thread = threading.Thread(target=VideoPlayer.start_checking, args=(self, lock,))
            thread.start()

    def black_frame(self, dim):
        return np.zeros(dim)
    
    def display_frame(self, frame):
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo
