import tkinter as tk
from tkinter import filedialog, messagebox
import cv2

# Function to select a video file
def select_video():
    video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.mkv")])
    if video_path:
        entry_video.delete(0, tk.END)
        entry_video.insert(0, video_path)

# Function to select a subtitle file
def select_subtitle():
    subtitle_path = filedialog.askopenfilename(filetypes=[("Subtitle files", "*.srt;*.txt")])
    if subtitle_path:
        entry_subtitle.delete(0, tk.END)
        entry_subtitle.insert(0, subtitle_path)

# Toggle the subtitle file input based on checkbox status
def toggle_subtitle_input():
    if subtitle_var.get():
        entry_subtitle.config(state='normal')
        button_subtitle.config(state='normal')
    else:
        entry_subtitle.config(state='disabled')
        button_subtitle.config(state='disabled')
        entry_subtitle.delete(0, tk.END)  # Clear any existing path

# Function to handle the final submission and play video
def submit():
    video_path = entry_video.get()
    subtitle_path = entry_subtitle.get() if subtitle_var.get() else None
    
    if not video_path:
        messagebox.showerror("Input Error", "Please select a video file.")
        return
    
    # Play the video
    play_video(video_path)

# Function to play the selected video
def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not open video file.")
        return
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Display the video frame by frame
        cv2.imshow("Video Playback", frame)

        # Press 'q' to exit the video playback
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Main GUI setup
window = tk.Tk()
window.title("Video and Subtitle Selector")
window.geometry("500x300")

# Video file selection
label_video = tk.Label(window, text="Select a video file:")
label_video.pack(pady=5)

entry_video = tk.Entry(window, width=50)
entry_video.pack(pady=5)

button_video = tk.Button(window, text="Browse", command=select_video)
button_video.pack(pady=5)

# Checkbox for subtitle file
subtitle_var = tk.BooleanVar()
checkbox_subtitle = tk.Checkbutton(window, text="I have a subtitle file (SRT/TXT)", variable=subtitle_var, command=toggle_subtitle_input)
checkbox_subtitle.pack(pady=10)

# Subtitle file selection (initially disabled)
label_subtitle = tk.Label(window, text="Select a subtitle file:")
label_subtitle.pack(pady=5)

entry_subtitle = tk.Entry(window, width=50, state='disabled')
entry_subtitle.pack(pady=5)

button_subtitle = tk.Button(window, text="Browse", command=select_subtitle, state='disabled')
button_subtitle.pack(pady=5)

# Submit button
button_submit = tk.Button(window, text="Submit", command=submit)
button_submit.pack(pady=20)

# Run the main event loop
window.mainloop()
