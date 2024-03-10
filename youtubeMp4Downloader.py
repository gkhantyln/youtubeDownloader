import os
import yt_dlp
import re

class YouTubeDownloader:
    def __init__(self, video_id):
        self.video_id = video_id
        self.url = f"https://www.youtube.com/watch?v={video_id}"
        self.target_folder = os.path.join(os.getcwd(), "videos")

        if not os.path.exists(self.target_folder):
            os.makedirs(self.target_folder)

    def get_video_title(self):
        try:
            with yt_dlp.YoutubeDL() as ydl:
                info = ydl.extract_info(self.url, download=False)
                return info.get('title', 'video')

        except Exception as e:
            print(f"Hata oluştu: {e}")
            return 'video'

    def clean_filename(self, filename):
        cleaned_filename = re.sub(r'[^\w\s]', '', filename)
        cleaned_filename = re.sub(r'\s+', '_', cleaned_filename)
        return cleaned_filename

    def download_video(self):
        try:
            video_title = self.get_video_title()
            cleaned_title = self.clean_filename(video_title)

            video_filename = f"{cleaned_title}_{self.video_id}.mp4"

            options = {
                'format': 'best',
                'outtmpl': os.path.join(self.target_folder, video_filename),
            }

            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([self.url])

            print("İndirme tamamlandı!")
        except Exception as e:
            print(f"Hata oluştu: {e}")

if __name__ == "__main__":

    video_id = input("Please enter the YouTube video ID: ")
    
    downloader = YouTubeDownloader(video_id)
    downloader.download_video()
