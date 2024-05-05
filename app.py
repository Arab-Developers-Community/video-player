from tkinter.filedialog import askopenfilename
import customtkinter as ctk
import video_player as vp
import tkinter as tk
import tkinter.messagebox as tk_mb

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App:

    def __init__(self):
        self.app = ctk.CTk()
        self.app.geometry("500x600")
        self.app.title("Censored Video Player Powered with AI")
        self.video_file_path = 'None'
        self.f_name_label = None
        self.initialize_gui()
        self.app.mainloop()

    def browse(self):
        f_path = askopenfilename(initialdir="/", title="Select File",
                                 filetypes=(("Video files", "*.mp4"), ("All Files", "*.*")))
        self.video_file_path = 'None' if f_path == '' else f_path
        self.f_name_label.configure(text='file selected: ' + self.video_file_path)

    def start(self):
        if self.video_file_path == 'None':
            tk_mb.showwarning(title='No File Selected',
                              message='Please make sure that you have selected a file!')
        else:
            self.app.destroy()
            video = vp.VideoPlayer(self.video_file_path)

    def initialize_gui(self):
        frame = ctk.CTkFrame(master=self.app)
        frame.pack(pady=20, padx=40, fill='both', expand=True)

        label = ctk.CTkLabel(master=frame, text='Select a video\n'
                                                'NOTE: This video player only supports mp4 files')
        label.pack(pady=12, padx=10)

        button = ctk.CTkButton(master=frame, text='Browse', command=self.browse)
        button.pack(pady=12, padx=10)

        self.f_name_label = ctk.CTkLabel(master=frame, text='file selected: ' + self.video_file_path)
        self.f_name_label.pack(pady=12, padx=10)

        label = ctk.CTkLabel(master=frame, text='Select filters:')
        label.pack(pady=12, padx=10)
        checkbox = ctk.CTkCheckBox(master=frame, text='Nudity', )
        checkbox.pack(pady=12, padx=10)

        checkbox = ctk.CTkCheckBox(master=frame, text='Kissing')
        checkbox.pack(pady=12, padx=10)

        button = ctk.CTkButton(master=frame, text='Start Video', command=self.start)
        button.pack(pady=12, padx=10)


