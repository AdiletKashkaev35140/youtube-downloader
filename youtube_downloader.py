import tkinter as tk
from tkinter import ttk, messagebox
import yt_dlp
import os
import threading
import re
from urllib.parse import urlparse, parse_qs
import time


class YouTubeDownloader:
    def __init__(self, root):
        self.loading_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.loading_index = 0
        self.is_downloading = False
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")

        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # URL Entry with Clear Button
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(url_frame, text="YouTube URL:", font=("Segoe UI", 12, "bold"), background="#ffffff").pack(side=tk.LEFT, padx=(0, 10))
        self.url_entry = ttk.Entry(url_frame, width=45, font=("Segoe UI", 12))
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.clear_button = ttk.Button(url_frame, text="Clear", command=self.clear_input, style="Accent.TButton")
        self.clear_button.pack(side=tk.LEFT, padx=(10, 0))


        # Download Button
        self.download_button = ttk.Button(main_frame, text="Download", command=self.start_download, style="Accent.TButton")
        self.download_button.pack(pady=18, ipadx=12, ipady=6)

        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100, style="Modern.Horizontal.TProgressbar")
        self.progress_bar.pack(fill=tk.X, pady=(0, 16))

        # Status & Futuristic Loading Animation
        self.status_frame = ttk.Frame(main_frame)
        self.status_frame.pack(fill=tk.X, pady=(0, 5))
        self.loading_wave = ttk.Label(self.status_frame, text="", font=("Segoe UI", 18, "bold"), background="#f0f4fa", foreground="#0078d7")
        self.loading_wave.pack(side=tk.LEFT, padx=(0, 10))
        self.status_label = ttk.Label(self.status_frame, text="", font=("Segoe UI", 12), background="#f0f4fa")
        self.status_label.pack(side=tk.LEFT)

    def update_loading_animation(self):
        # Futuristic animated wave of colored dots
        if not hasattr(self, 'wave_phase'):
            self.wave_phase = 0
        if self.is_downloading:
            wave = ''
            colors = ['#0078d7', '#00bcf2', '#00b294', '#bad80a', '#ffb900']
            for i in range(5):
                phase = (self.wave_phase + i) % 5
                dot = '●'
                color = colors[phase]
                wave += f'\u200a' + f'\u001b[38;2;{int(color[1:3],16)};{int(color[3:5],16)};{int(color[5:7],16)}m{dot}\u001b[0m'
            # Tkinter doesn't support ANSI, so use simple color cycling
            dot_wave = ''
            for i in range(5):
                phase = (self.wave_phase + i) % 5
                color = colors[phase]
                dot_wave += f'\u2022 '
            self.loading_wave.config(text=dot_wave, foreground=colors[self.wave_phase])
            self.wave_phase = (self.wave_phase + 1) % 5
            self.root.after(120, self.update_loading_animation)
        else:
            self.loading_wave.config(text="")

    def update_progress(self, d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes', 0)
            if total_bytes:
                percentage = (downloaded_bytes / total_bytes) * 100
                self.progress_var.set(percentage)
                speed = d.get('speed', 0)
                status_text = f"Downloading... {percentage:.1f}%"
                if speed:
                    status_text += f" ({speed/1024/1024:.1f} MB/s)"
                self.status_label.config(text=status_text)
                self.root.update()

    def download_complete(self):
        self.is_downloading = False
        self.loading_wave.config(text="")
        self.status_label.config(text="Download Complete!")
        self.download_button.config(state=tk.NORMAL)
        messagebox.showinfo("Success", "Download completed successfully!")

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return

        self.download_button.config(state=tk.DISABLED)
        self.status_label.config(text="Starting download...")
        self.progress_var.set(0)
        self.is_downloading = True
        self.update_loading_animation()
        threading.Thread(target=self.download, daemon=True).start()

    def clear_input(self):
        self.url_entry.delete(0, tk.END)

    def is_valid_youtube_url(self, url):
        # Check if URL is a valid YouTube URL
        youtube_regex = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/'
        if not re.match(youtube_regex, url):
            return False
        
        try:
            parsed_url = urlparse(url)
            if 'youtube.com' in parsed_url.netloc:
                if 'watch' in parsed_url.path and parse_qs(parsed_url.query).get('v'):
                    return True
                if 'shorts' in parsed_url.path:
                    return True
            elif 'youtu.be' in parsed_url.netloc:
                return True
        except:
            return False
        return False

    def download(self):
        try:
            url = self.url_entry.get().strip()
            if not self.is_valid_youtube_url(url):
                raise ValueError("Invalid YouTube URL. Please enter a valid YouTube video URL.")

            # Update status
            self.status_label.config(text="Fetching video information...")
            self.root.update()

            # Setup yt-dlp options for default format
            ydl_opts = {
                'progress_hooks': [self.update_progress],
                'outtmpl': os.path.join(os.path.dirname(__file__) if '__file__' in globals() else os.getcwd(), 'downloads', '%(title)s.%(ext)s'),
                'quiet': True,
                'noprogress': False,
            }

            # Ensure downloads dir exists
            downloads_dir = os.path.join(os.path.dirname(__file__) if '__file__' in globals() else os.getcwd(), 'downloads')
            os.makedirs(downloads_dir, exist_ok=True)

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.root.after(0, self.download_complete)
            self.root.after(0, lambda: self.download_button.config(state=tk.NORMAL))
            self.is_downloading = False

        except Exception as e:
            error_message = str(e)
            print(f"Debug - Full error: {error_message}")
            self.root.after(0, lambda: messagebox.showerror("Error", error_message))
            self.root.after(0, lambda: self.download_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.status_label.config(text="Error occurred"))
            self.root.after(0, lambda: self.loading_wave.config(text=""))
            self.is_downloading = False

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#f0f4fa")
    style.configure("TLabel", background="#f0f4fa", font=("Segoe UI", 12))
    style.configure("Accent.TButton", font=("Segoe UI", 12, "bold"), foreground="#fff", background="#0078d7", borderwidth=0, focusthickness=3, focuscolor="#00bcf2", padding=8)
    style.map("Accent.TButton",
              foreground=[('active', '#fff')],
              background=[('active', '#005a9e')])
    style.configure("Modern.Horizontal.TProgressbar", troughcolor="#e6eaf0", bordercolor="#e6eaf0", background="#0078d7", lightcolor="#00bcf2", darkcolor="#0078d7", thickness=18)
    app = YouTubeDownloader(root)
    root.mainloop()
