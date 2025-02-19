from typing import List
from events_lib.EventObject import EventObject


class YouTubeTerminalUI(EventObject):
    def __init__(self) -> None:
        super().__init__()
        self._seperator = "-" * 10

    def start(self) -> None:
        while True:
            command = input("Enter a command (or help): ")
            params = command.split(" ")

            if command == "exit" or command == "quit" or command == "q" or command == "e":
                break

            self._handle_command(params[0], params[1:])

    def _handle_command(self, command: str, params: List[str]) -> None:
        if command == "help" or command == "":
            self.help_command()
        elif command == "options" and len(params) > 0:
            self.yt_options_command(params[0])
        elif command == "download" and len(params) > 2:
            self.download_command(params[0], params[1], params[2])
        elif command == "download_mp3" and len(params) > 0:
            self.download_mp3_command(params[0])
        elif command == "downloads":
            self.show_downloads_command()
        else:
            self._print_error("Invalid command. Type 'help' to see available commands")

    def _print_seperator(self) -> None:
        print(self._seperator)

    def _print_section(self, section_name: str) -> None:
        print("")
        print(f"[{section_name}]")
        print("")

    def _print_command(self, command: str, description: str, params: list = []) -> None:
        if params:
            print(f"{command} [{', '.join(params)}] - {description}")
        else:
            print(f"{command} - {description}")

    def _print_error(self, message: str) -> None:
        self._print_section("Error")
        print(message)
        self._print_seperator()

    def help_command(self) -> None:
        print("Available commands:")
        self._print_seperator()

        self._print_section("General")
        self._print_command("help", "Show this message")
        self._print_command("exit/quit/q/e", "Exit the program")

        self._print_section("Download commands")
        self._print_command("options", "Lists info of video", ["url"])
        self._print_command("download", "Downloads video", ["url", "itag", "target_format (mp3, original)"])
        self._print_command("download_mp3", "Downloads video audio of highest audio quality", ["url"])
        self._print_command("downloads", "Lists ongoing downloads")

        self._print_seperator()

    def yt_options_command(self, url: str) -> None:
        self.emit("get_yt_options", url)

    def download_command(self, url: str, itag: str, target_format: str) -> None:
        allowed_formats = ["mp3", "original"]
        if target_format not in allowed_formats:
            self._print_error(f"Invalid target format. Allowed formats: {', '.join(allowed_formats)}")
            return

        self.emit("download", url, itag, target_format)

    def download_mp3_command(self, url: str) -> None:
        self.emit("download_mp3", url)

    def show_downloads_command(self) -> None:
        self.emit("list_downloads")

    def show_yt_options(self, options: list) -> None:
        self._print_section("YouTube Video Options")

        for i, option in enumerate(options):
            print(f"({i}) [{option.itag}]: {option}")

        self._print_seperator()

    def show_downloads(self, downloads: list, ongoing_downloads: list) -> None:
        self._print_section("Ongoing Downloads")

        for i, download in enumerate(ongoing_downloads):
            print(f"[{i}] {download}")

        self._print_section("Downloads")
        for i, download in enumerate(downloads):
            print(f"[{i}] {download}")

        self._print_seperator()
