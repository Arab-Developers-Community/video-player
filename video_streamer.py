import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import customtkinter as ctk
from detect_nude import detect_nude
import numpy as np 
from PIL import Image, ImageTk
import os
from video_manager import video_manager
import time
import cv2    


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class video_streamer:

    def __init__(self, path, should_render_frame_callback):
        self.root = ctk.CTk()
        self.vm = video_manager(path)
        self.should_render_frame_callback = should_render_frame_callback
        self.window_height = self.root.winfo_screenheight()
        self.window_width = self.root.winfo_screenwidth()
        self.root.geometry("1080x800")
        self.root.title("Video Player")
        self.image_label = None
        self.video_file_path = None
        self.frame = None
        self.has_ended = False
        self.current_image = ctk.CTkImage(light_image=Image.open('assets/black.jpg'),
                                          dark_image=Image.open('assets/black.jpg'),
                                          size=(self.window_height, self.window_width))
        self.lastTimeStamp = time.time() * 1000
        self.frames_displayed = 0
        self.initialize_gui()

    def initialize_gui(self):
        self.frame = ctk.CTkFrame(master=self.root, corner_radius=15)
        self.frame.pack(pady=20, padx=40, fill='both', expand=True)
        button_browse = ctk.CTkButton(master=self.frame, text="Open Video", corner_radius=8, command=self.browse)
        button_browse.pack(pady=10, padx=10)
        self.image_label = ctk.CTkLabel(self.frame, text="", image=self.current_image)
        self.image_label.pack(pady=0, padx=0, fill='both', expand=True)

    def start(self):
        self.update()
        self.root.mainloop()

    def browse(self):
        f_path = askopenfilename(initialdir="/", title="Select File",
                                 filetypes=(("Video files", "*.mp4"), ("All Files", "*.*")))
        self.video_file_path = 'None' if f_path == '' else f_path

    def update(self):
        if self.has_ended:
            self.vm.stop_stream()
            quit(0)
        timePerFrame = self.vm.get_frame_time()
        currentTimeStamp = time.time() * 1000
        if (currentTimeStamp - self.lastTimeStamp) <= timePerFrame:
            self.root.after(1, self.update)
            return
        self.lastTimeStamp = currentTimeStamp
        should_render_results = self.should_render_frame_callback(self.vm.get_current_second())
        if should_render_results is None:
            #should show wait
            pass
        stream_frames = self.vm.stream_frames()
        if stream_frames is None:
            self.has_ended = True
            return
        if should_render_results:# remove this true
            self.display_frame(stream_frames)
        
        self.frames_displayed = self.frames_displayed + 1
        self.root.after(1, self.update)


    def black_frame(self, dim):
        return np.zeros(dim)
    
    def display_frame(self, frame):

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo
