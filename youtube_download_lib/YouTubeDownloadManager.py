import os
from pytubefix import YouTube, StreamQuery
from moviepy import AudioFileClip, VideoFileClip
import uuid


class YouTubeDownloadManager:
    @staticmethod
    def get_video_options(url: str) -> StreamQuery:
        try:
            youtube: YouTube = YouTube(url)
        except Exception as e:
            return None

        return youtube.streams

    @staticmethod
    def download_and_convert(url: str, itag: str, target_format: str, download_folder_path: str = "./yt_downloads") -> str:
        donwload_file_path: str = YouTubeDownloadManager.download(url, itag, download_folder_path)

        if target_format == "original":
            return donwload_file_path

        convert_file_path = YouTubeDownloadManager.convert_to_format(donwload_file_path, target_format)

        # Delete original file
        while os.path.exists(donwload_file_path):
            try:
                os.remove(donwload_file_path)
            except PermissionError:
                pass
            except FileNotFoundError:
                break

        return convert_file_path

    @staticmethod
    def download(url: str, itag: str, download_folder_path: str = "./yt_downloads") -> str | None:
        try:
            youtube: YouTube = YouTube(url)
        except Exception as e:
            return None

        stream = youtube.streams.get_by_itag(itag)
        downloaded_file_path: str = stream.download(output_path=download_folder_path)

        return downloaded_file_path

    @staticmethod
    def convert_to_format(input_file_path: str, target_format: str) -> str:
        base_filepath: str = input_file_path.split(".")[0]
        unique_suffix: str = uuid.uuid4().hex[:4]
        output_filepath: str = f"{base_filepath}_{unique_suffix}.{target_format}"

        current_format = input_file_path.split(".")[-1]

        audio_formats = ["mp3", "wav", "flac", "ogg", "m4a"]
        is_audio = current_format in audio_formats

        audio: AudioFileClip = None

        if is_audio:
            audio = AudioFileClip(input_file_path)
        else:
            audio = VideoFileClip(input_file_path).audio

        audio.write_audiofile(output_filepath, logger=None)

        return output_filepath
