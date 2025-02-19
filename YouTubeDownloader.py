from threading import Thread
import uuid
from ui_lib.YouTubeTerminalUI import YouTubeTerminalUI
from youtube_download_lib.YouTubeDownloadManager import YouTubeDownloadManager
from pytubefix import StreamQuery


class YouTubeDownloader:
    def __init__(self):
        self._downloads: list = []  # filepath
        self._ongoing_downloads: dict = {}  # Itag: filepath

        self._ui: YouTubeTerminalUI = YouTubeTerminalUI()
        self._ui.add_listener("get_yt_options", self._on_get_yt_options)
        self._ui.add_listener("download", self._on_download)
        self._ui.add_listener("download_mp3", self._on_download_mp3)
        self._ui.add_listener("list_downloads", self._on_list_downloads)

    def _on_get_yt_options(self, url: str):
        streams: StreamQuery = YouTubeDownloadManager.get_video_options(url)

        if streams is None:
            self._ui._print_error("Invalid URL")
            return

        self._ui.show_yt_options(streams)

    def _on_download_mp3(self, url: str):
        streams: StreamQuery = YouTubeDownloadManager.get_video_options(url)

        if streams is None:
            self._ui._print_error("Invalid URL")
            return

        highest_bitrate_audio_stream = streams.filter(only_audio=True).order_by("abr").last()

        if highest_bitrate_audio_stream:
            itag = highest_bitrate_audio_stream.itag
            target_format = "mp3"
            self._on_download(url, itag, target_format)

    def _on_download(self, url: str, itag: str, target_format: str):
        def download_thread():
            random_uuid = uuid.uuid4().hex[:4]
            self._ongoing_downloads[random_uuid] = url
            file_path = YouTubeDownloadManager.download_and_convert(url, itag, target_format)
            self._downloads.append(file_path)
            self._ongoing_downloads.pop(random_uuid)

        Thread(target=download_thread).start()

    def _on_list_downloads(self):
        self._ui.show_downloads(self._downloads, self._ongoing_downloads.values())

    def start(self):
        self._ui.start()
