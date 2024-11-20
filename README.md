
# MTX YT Downloader

![Banner](images/banner.png)

**MTX YT Downloader** is a feature-rich application for downloading YouTube videos and audio in various resolutions and bitrates. Built with Python and `yt-dlp`, it offers a futuristic UI and a seamless experience.

---

## **Features**
- Download YouTube **Videos** in custom resolutions (144p, 360p, 720p, 1080p).
- Download YouTube **Audio** with custom bitrates (64kbps, 128kbps, 320kbps).
- Prevent duplicate downloads with built-in history management.
- Save user preferences like output folder and quality settings.
- Voice commands for hands-free operations.

---

## **Preview**

### Application UI
![Application Screenshot](images/screenshot1.png)

---

## **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/MTX-YT-Downloader.git
   cd MTX-YT-Downloader
   ```

2. Install the required dependencies:
   ```bash
   pip install yt-dlp SpeechRecognition pyttsx3 pyaudio
   ```

3. Run the application:
   ```bash
   python MTXYTDOWNLOADER.py
   ```

---

## **How to Use**
1. Enter a valid YouTube URL.
2. Select the output folder.
3. Choose video resolution or audio bitrate.
4. Click **Download Video** or **Download Audio**.

---

## **Project Structure**
```
MTX-YT-Downloader/
│
├── download_log.txt           # Log file for download activities
├── user_preferences.json      # File to store user preferences
├── download_history.json      # File to track downloaded URLs
├── MTXYTDOWNLOADER.py         # Main Python script
├── images/
│   ├── banner.png             # Banner for README.md
│   └── screenshot1.png        # Screenshot of the application
└── README.md                  # Project documentation
```

---

## **Contributing**
Contributions are welcome! Feel free to submit a pull request or raise issues.

---

## **License**
This project is licensed under the MIT License.
