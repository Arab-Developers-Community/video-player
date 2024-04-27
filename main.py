import tkinter as tk
from tkinter import ttk
import cv2
import threading
import queue
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
import customtkinter as ctk
import tkinter.messagebox as tkmb
# Selecting GUI theme - dark, light , system (for system default)
ctk.set_appearance_mode("dark")

# Selecting color theme - blue, green, dark-blue
ctk.set_default_color_theme("blue")

app = ctk.CTk()
window_width = app.winfo_screenwidth()
window_height = app.winfo_screenheight()
app.geometry("%dx%d" % (window_width, window_height))
app.title("Modern Login UI using Customtkinter")

f_path = None

# def login():
#     username = "Geeks"
#     password = "12345"
#     new_window = ctk.CTkToplevel(app)
#
#     new_window.title("New Window")
#
#     new_window.geometry("350x150")
#
#     if user_entry.get() == username and user_pass.get() == password:
#         tkmb.showinfo(title="Login Successful", message="You have logged in Successfully")
#         ctk.CTkLabel(new_window, text="GeeksforGeeks is best for learning ANYTHING !!").pack()
#     elif user_entry.get() == username and user_pass.get() != password:
#         tkmb.showwarning(title='Wrong password', message='Please check your password')
#     elif user_entry.get() != username and user_pass.get() == password:
#         tkmb.showwarning(title='Wrong username', message='Please check your username')
#     else:
#         tkmb.showerror(title="Login Failed", message="Invalid Username and password")
def browse():
    f_path = askopenfilename(initialdir="/", title="Select File",
                             filetypes=(("Video files", "*.mp4"), ("All Files", "*.*")))
    f_name_label.configure(text='file selected: ' + f_path)
def start():
    return
frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=40, fill='both', expand=True)

label = ctk.CTkLabel(master=frame, text='Select a video')
label.pack(pady=12, padx=10)
label = ctk.CTkLabel(master=frame, text='NOTE: This video player only supports mp4 files')
label.pack(pady=12, padx=10)

button = ctk.CTkButton(master=frame, text='Browse', command=browse)
button.pack(pady=12, padx=10)

f_name_label = ctk.CTkLabel(master=frame, text='file selected: None')
f_name_label.pack(pady=12, padx=10)

label = ctk.CTkLabel(master=frame, text='Select filters:')
label.pack(pady=12, padx=10)
checkbox = ctk.CTkCheckBox(master=frame, text='Nudity')
checkbox.pack(pady=12, padx=10)

checkbox = ctk.CTkCheckBox(master=frame, text='Kissing')
checkbox.pack(pady=12, padx=10)

button = ctk.CTkButton(master=frame, text='Start Video', command=start)
button.pack(pady=12, padx=10)


app.mainloop()
