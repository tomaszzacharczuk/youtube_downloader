import pafy
from pydub import AudioSegment
import os
import sys
import argparse
import re


def get_arguments():
    parser = argparse.ArgumentParser(prog='python3 ' + __file__, 
                                     usage='%(prog)s --url URL [options]')
    parser.add_argument('--url', required=True, help='URL for You Tube video.')
    parser.add_argument('--download_path',
                        help='Path to where the file should be saved.')
    parser.add_argument('--t_start', type=int,
                        help='Number of second that should be cut at the beggining of video.')
    parser.add_argument('--t_end', 
                        type=int, 
                        help='Number of second that should be cut at the end of video.')
    args = parser.parse_args()
    args_dict = {'url': args.url, 't_start': args.t_start, 't_end': args.t_end}
    if args.download_path:
        args_dict['download_path'] = args.download_path
    return args_dict

def xstr(str):
    if str is None:
        return '0'
    return str


class YouTubeDownload(object):

    def __init__(self, url, download_path="/Users/tom/Music", t_start=None, t_end=None):
        self.url = url
        if not os.path.isdir(download_path) or not os.path.exists(download_path):
            raise NotADirectory('Download path is not a directory.')
        self.download_path = download_path
        self.t_start = t_start
        self.t_end = t_end

    def __call__(self):
        self.video_name = self.download_audio()
        name = self.convert_to_mp3()
        self.cleanup()
        print('Your file is at ' + name)

    def download_audio(self):
        video = pafy.new(self.url)
        bestaudio = video.getbestaudio()
        self.file_extension = bestaudio.extension
        self.filepath = bestaudio.download(filepath=self.download_path)
        return video.title

    def convert_to_mp3(self):
        default_version = AudioSegment.from_file(self.filepath, self.file_extension)
        print("""Leave empty to use default values.""")
        t_start = input('Cut beggining [' + xstr(self.t_start) + ']: ')
        self.t_start = int(t_start) if t_start else self.t_start
        if self.t_start:
            self.t_start *= 1000
            default_version = default_version[self.t_start:]

        t_end = input('Cut ending [' + xstr(self.t_end) + ']: ')
        self.t_end = int(t_end) if t_end else self.t_end
        if self.t_end:
            self.t_end *= 1000
            self.t_end = -self.t_end
            default_version = default_version[:self.t_end]

        new_filepath = self.filepath.replace(self.file_extension, "mp3")
        self.video_name = re.sub('(\(.*\))', '', self.video_name)
        tags2 = re.findall('(.*)[-|–](.*)', self.video_name)
        try:
            tags = {'artist': tags2[0][0].strip(), 'title': tags2[0][
                1].strip(), 'album': self.video_name}
        except IndexError:
            tags = {'artist': input("Type artist:"), 'title': input(
                "Type title:"), 'album': input("Type album:")}
        for tag_name, tag_value in tags.items():
            value = input(tag_name.upper() + ' [' + tag_value + ']: ')
            tags[tag_name] = value or tag_value
        new_file = default_version.export(
            new_filepath, format="mp3", tags=tags)
        return new_file.name

    def cleanup(self):
        os.remove(self.filepath)


class NotADirectory(ValueError):
    pass

if __name__ == "__main__":
    args = get_arguments()

    try:
        youtube_downloader = YouTubeDownload(**args)
    except (NotADirectory, TypeError) as e:
        sys.exit(e)

    try:
        youtube_downloader()
    except ValueError as e:
        print(e)
