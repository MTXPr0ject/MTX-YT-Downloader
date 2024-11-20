import os
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import subprocess
import json
import speech_recognition as sr
import pyttsx3
from datetime import datetime
import logging
import sys

# Initialize TTS engine
tts_engine = pyttsx3.init()
tts_engine.setProperty("rate", 150)

# Set up logging
logging.basicConfig(filename="download_log.txt", level=logging.DEBUG, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Global constants
MEMORY_FILE = "user_preferences.json"
DOWNLOAD_HISTORY_FILE = "download_history.json"

# Dynamic paths for executables
BASE_DIR = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
YTDLP_PATH = os.path.join(BASE_DIR, "yt-dlp.exe")
FFMPEG_PATH = os.path.join(BASE_DIR, "ffmpeg.exe")

# Check for executables
def check_dependencies():
    missing = []
    if not os.path.exists(YTDLP_PATH):
        missing.append("yt-dlp.exe")
    if not os.path.exists(FFMPEG_PATH):
        missing.append("ffmpeg.exe")

    if missing:
        error_msg = f"The following dependencies are missing: {', '.join(missing)}\nPlease ensure they are in the same directory as this program."
        logging.error(error_msg)
        messagebox.showerror("Missing Dependencies", error_msg)
        tts_engine.say(error_msg)
        tts_engine.runAndWait()
        sys.exit(1)

# Load or initialize user preferences
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {"output_folder": "", "thumbnail": True, "metadata": True, "audio_quality": "128", "video_resolution": "best"}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

memory = load_memory()

# Load or initialize download history
def load_download_history():
    if os.path.exists(DOWNLOAD_HISTORY_FILE):
        with open(DOWNLOAD_HISTORY_FILE, "r") as f:
            return json.load(f)
    return {"downloads": []}

def save_download_history(history):
    with open(DOWNLOAD_HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

download_history = load_download_history()

# Function to prevent duplicate downloads
def is_duplicate(url):
    return url in download_history["downloads"]

def add_to_history(url):
    download_history["downloads"].append(url)
    save_download_history(download_history)

# Function for TTS
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to log errors
def log_error(message):
    logging.error(message)

# Function to run yt-dlp commands
def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
        messagebox.showinfo("Success", "Download completed successfully!")
        speak("Download completed successfully.")
    except subprocess.CalledProcessError as e:
        error_message = f"An error occurred: {e}"
        log_error(error_message)
        messagebox.showerror("Error", error_message)
        speak("An error occurred during the download. Please check the logs.")

# Handle video download
def download_video(url):
    if not url:
        messagebox.showwarning("Input Error", "Please enter a valid URL.")
        speak("Please enter a valid URL.")
        return

    if is_duplicate(url):
        messagebox.showinfo("Duplicate File", "This URL has already been downloaded.")
        speak("This file has already been downloaded.")
        return

    resolution = video_res_dropdown.get()
    output_dir = memory["output_folder"]

    if not output_dir:
        messagebox.showwarning("Input Error", "Please select an output folder.")
        speak("Please select an output folder.")
        return

    command = f'"{YTDLP_PATH}" -f "bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]" --merge-output-format mp4 -o "{output_dir}/%(title)s.%(ext)s" {url}'
    run_command(command)
    add_to_history(url)

# Handle audio download
def download_audio(url):
    if not url:
        messagebox.showwarning("Input Error", "Please enter a valid URL.")
        speak("Please enter a valid URL.")
        return

    if is_duplicate(url):
        messagebox.showinfo("Duplicate File", "This URL has already been downloaded.")
        speak("This file has already been downloaded.")
        return

    bitrate = audio_bitrate_dropdown.get()
    output_dir = memory["output_folder"]

    if not output_dir:
        messagebox.showwarning("Input Error", "Please select an output folder.")
        speak("Please select an output folder.")
        return

    command = f'"{YTDLP_PATH}" -x --audio-format mp3 --audio-quality {bitrate} --embed-metadata --embed-thumbnail -o "{output_dir}/%(title)s.%(ext)s" {url}'
    run_command(command)
    add_to_history(url)

# Output folder selection
def select_output_folder():
    folder = filedialog.askdirectory(title="Select Output Folder")
    if folder:
        memory["output_folder"] = folder
        save_memory(memory)
        speak("Output folder updated.")

# Create main GUI
root = tk.Tk()
root.title("MTX YT Downloader")
root.geometry("700x600")
root.config(bg="#0A0A0A")

# Title Label
title_label = tk.Label(root, text="MTX YT Downloader", font=("Helvetica", 16, "bold"), fg="#00FFFF", bg="#0A0A0A")
title_label.pack(pady=20)

# URL Entry Section
url_label = tk.Label(root, text="Enter YouTube URL:", font=("Helvetica", 12), fg="#FFFFFF", bg="#0A0A0A")
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=50, font=("Helvetica", 12))
url_entry.pack(pady=10)

# Video Resolution Dropdown
video_res_label = tk.Label(root, text="Select Video Resolution:", font=("Helvetica", 12), fg="#FFFFFF", bg="#0A0A0A")
video_res_label.pack(pady=5)
video_res_dropdown = ttk.Combobox(root, values=["144", "360", "480", "720", "1080"], font=("Helvetica", 12))
video_res_dropdown.set("1080")
video_res_dropdown.pack(pady=5)

# Audio Bitrate Dropdown
audio_bitrate_label = tk.Label(root, text="Select Audio Bitrate (kbps):", font=("Helvetica", 12), fg="#FFFFFF", bg="#0A0A0A")
audio_bitrate_label.pack(pady=5)
audio_bitrate_dropdown = ttk.Combobox(root, values=["64", "128", "192", "256", "320"], font=("Helvetica", 12))
audio_bitrate_dropdown.set("128")
audio_bitrate_dropdown.pack(pady=5)

# Buttons
output_folder_button = tk.Button(root, text="Select Output Folder", font=("Helvetica", 12), command=select_output_folder, bg="#00FF00", fg="#000000")
output_folder_button.pack(pady=10)

video_button = tk.Button(root, text="Download Video", font=("Helvetica", 12), command=lambda: download_video(url_entry.get()), bg="#FF5733", fg="#FFFFFF")
video_button.pack(pady=10)

audio_button = tk.Button(root, text="Download Audio", font=("Helvetica", 12), command=lambda: download_audio(url_entry.get()), bg="#3498DB", fg="#FFFFFF")
audio_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", font=("Helvetica", 12), command=root.quit, bg="#FF0000", fg="#FFFFFF")
exit_button.pack(pady=10)

# Dependency Check
check_dependencies()

root.mainloop()
