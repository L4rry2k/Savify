import os
from pathlib import Path
from shutil import move, rmtree
from sys import platform


class FFmpegDL:
    def __init__(self):
        from uuid import uuid1
        home = Path.home()

        if platform == 'win32':
            self.temp = home / 'AppData/Roaming/Savify/ffmpeg' / str(uuid1())
            self.download_link = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
            self.final_location = self.temp.parent / 'bin' / 'ffmpeg.exe'
            self.platform_task = self._download_win
        elif platform == 'linux':
            self.temp = home / '.local/share/Savify/ffmpeg' / str(uuid1())
            self.download_link = 'https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz'
            self.final_location = self.temp.parent / 'ffmpeg'
            self.platform_task = self._download_linux
        elif platform == 'darwin':
            self.temp = home / 'Library/Application Support/Savify/ffmpeg' / str(uuid1())
            self.download_link = 'https://evermeet.cx/ffmpeg/getrelease/zip'
            self.final_location = self.temp.parent / 'ffmpeg'
            self.platform_task = self._download_mac
        else:
            raise RuntimeError(f'Platform not supported! [{platform}]')

        self.file = self.temp / self.download_link.split('/')[-1]

    def check(self):
        return self.final_location.is_file()

    def download(self, force=False):
        downloaded = self.check()
        if not downloaded or force:
            rmtree(self.temp.parent)
            self._download()
            self.platform_task()

        return self.final_location

    def _download(self):
        from urllib.request import urlretrieve
        self.temp.mkdir(parents=True, exist_ok=True)
        urlretrieve(self.download_link, self.file)

    def _download_win(self):
        self._unzip()
        bin_path = self.temp / os.listdir(self.temp)[0] / 'bin'
        self._cleanup(bin_path)

    def _download_mac(self):
        self._unzip()
        bin_file = self.temp / 'ffmpeg'
        self._cleanup(bin_file)

    def _download_linux(self):
        self._untar()
        bin_file = self.temp / os.listdir(self.temp)[0] / 'ffmpeg'
        self._cleanup(bin_file)

    def _unzip(self):
        from zipfile import ZipFile
        with ZipFile(self.file, 'r') as zip_ref:
            zip_ref.extractall(self.temp)

    def _untar(self):
        import tarfile
        with tarfile.open(self.file) as tf:
            tf.extractall(self.temp)

    def _cleanup(self, ffmpeg_files):
        move(ffmpeg_files, self.temp.parent)
        rmtree(self.temp)
