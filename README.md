# YouTube Downloader GUI

A modern, simple, and fast desktop app to download YouTube videos with a single click. Built with Python, Tkinter, and [yt-dlp](https://github.com/yt-dlp/yt-dlp) for maximum reliability and speed.

---

## Features
- Clean, modern graphical interface
- Paste a YouTube URL and download with one click
- Progress bar and futuristic loading animation
- "Clear" button to reset input quickly
- Downloads best available single-file video or audio (no ffmpeg required)
- Works on Windows (Python 3.8+ recommended)

---

## Installation

1. **Clone this repository:**
   ```sh
   git clone https://github.com/yourusername/youtube-downloader.git
   cd youtube-downloader
   ```

2. **Install Python dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
   This will install `yt-dlp` and other required packages.

3. **(Optional, but recommended) Install FFmpeg:**
   - For best quality downloads, install [FFmpeg](https://ffmpeg.org/download.html) and add it to your PATH.
   - Without FFmpeg, the app will still work but may not download the highest possible quality.

---

## Usage

1. **Run the app:**
   ```sh
   python youtube_downloader.py
   ```

2. **Download a video:**
   - Paste a YouTube video URL into the input field.
   - Click `Download`.
   - Watch the progress bar and animation. The file will appear in the `downloads` folder.
   - Use the `Clear` button to reset the input.

---

## Troubleshooting
- **FFmpeg not found:**
  - You may see a warning about FFmpeg. For most single-file downloads, you can ignore it. For best quality, [install FFmpeg](https://ffmpeg.org/download.html).
- **"No suitable stream found" or download fails:**
  - Some videos may not have a single-file stream. Install FFmpeg for full support.
- **App does not launch:**
  - Make sure you have Python 3.8+ and all dependencies installed.

---

## Credits
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for reliable YouTube downloading
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI
- Inspired by open-source video tools and the Python community

---

## License
MIT