# youtube_downloader
Simple script for downloading high quality audio from youtube videos.

# Useage
In terminal (being in project's dir) run: <br>
python3 youtube_downloader --url 'youtube url to video' --download_path 'path to download directory' --t_start 0 --t_end 0

# Available options
optional arguments:
  -h, --help            show this help message and exit
  --url URL             URL for You Tube video.
  --download_path DOWNLOAD_PATH
                        Path to where the file should be saved.
  --t_start T_START     Number of second that should be cut at the beggining
                        of video.
  --t_end T_END         Number of second that should be cut at the end of
                        video.
