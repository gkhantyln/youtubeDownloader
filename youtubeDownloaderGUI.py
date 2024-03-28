import os
import yt_dlp
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")

        self.video_id_label = ttk.Label(root, text="YouTube Video URL:")
        self.video_id_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.video_id_entry = ttk.Entry(root)
        self.video_id_entry.grid(row=0, column=1, padx=5, pady=5)

        self.format_label = ttk.Label(root, text="Select Format:")
        self.format_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.format_var = tk.StringVar(root, "MP3")
        self.format_combobox = ttk.Combobox(root, textvariable=self.format_var, values=["MP3", "MP4"])
        self.format_combobox.grid(row=1, column=1, padx=5, pady=5)

        self.download_button = ttk.Button(root, text="Download", command=self.start_download)
        self.download_button.grid(row=1, column=2, padx=5, pady=5)

    def start_download(self):
        video_url = self.video_id_entry.get()
        if not video_url:
            messagebox.showerror("Error", "Please enter the YouTube video URL")
            return

        download_format = self.format_var.get()

        downloader_thread = threading.Thread(target=self.download_video, args=(video_url, download_format))
        downloader_thread.start()

    def download_video(self, video_url, download_format):
        try:
            def progress_hook(d):
                if d['status'] == 'downloading':
                    print(f"\rİndiriliyor... {d['_percent_str']} tamamlandı.", end='', flush=True)
                if d['status'] == 'finished':
                    print("\rİndirme tamamlandı.                          ")
                    messagebox.showinfo("Success", "Download completed!")

            ydl_opts = {
                'format': 'best' if download_format == 'MP4' else 'bestaudio/best',
                'outtmpl': f'{"audios" if download_format == "MP3" else "videos"}/%(title)s.{"mp3" if download_format == "MP3" else "mp4"}',
                'postprocessors': [],
                'progress_hooks': [progress_hook]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()
