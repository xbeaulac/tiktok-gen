import subprocess

from overlay import create_content
from shift_captions import shift_captions


def run_command(command: str):
    subprocess.run(command.split(' '))


# scrape Reddit for post's images and titles, use text-to-speech for narration
create_content()

# combine background video, images, and audio
run_command("yarn remotion render LayeredVideo public/temp.mp4")

# generate captions with whisper
run_command("rm public/temp.json")
run_command("node sub.mjs public/temp.mp4")

# shift captions backward to be more flashy
shift_captions("public/temp.json")

# combine temporary video and captions
run_command("yarn remotion render CaptionedVideo out/final.mp4")
