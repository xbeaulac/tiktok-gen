import ffmpeg
import sys


def print_error_and_exit(error_string: str) -> None:
    print(error_string, file=sys.stderr)
    sys.exit(1)


AUDIO_FORMATS = ["MP3", "WAV", "AAC", "FLAC", "OGG", "WMA", "ALAC", "AIFF", "M4A", "PCM"]
VIDEO_FORMATS = ["MP4", "AVI", "MKV", "MOV", "WMV", "FLV", "MPEG", "WEBM", "3GP", "MTS"]
IMAGE_FORMATS = ["JPEG", "PNG", "GIF", "BMP", "TIFF", "SVG", "RAW", "WEBP", "HEIF", "PSD"]


def get_info(pathname: str, file_type="") -> dict:
    extension = pathname.split(".")[-1].upper()

    if file_type != "audio" and file_type != "video":
        if extension in AUDIO_FORMATS:
            file_type = 'audio'
        elif extension in VIDEO_FORMATS or extension in IMAGE_FORMATS:
            file_type = 'video'
        else:
            print_error_and_exit("Unknown file type, specify either \"audio\" or \"video\", images are \"video\"")

    try:
        probe = ffmpeg.probe(pathname)
    except ffmpeg.Error as e:
        print_error_and_exit(e.stderr.decode())

    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == file_type), None)
    if video_stream is None:
        print_error_and_exit("Could not find video stream.")

    return video_stream
