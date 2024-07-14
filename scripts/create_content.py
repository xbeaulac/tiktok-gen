import json
import os
import shutil
from pathlib import Path
from get_image import get_image
from get_reddit_posts import get_reddit_posts
from get_info import get_info
from get_song_url import get_song_url
from speak import speak


def remove_dir_if_exists(path: str):
    audio_dir = Path(path)
    if audio_dir.exists() and audio_dir.is_dir():
        shutil.rmtree(audio_dir)


def create_content():
    remove_dir_if_exists('public/audio')
    remove_dir_if_exists('public/image')
    os.makedirs('public', exist_ok=True)
    os.makedirs('public/audio', exist_ok=True)
    os.makedirs('public/image', exist_ok=True)

    # get audio and images
    audio_paths = []
    image_paths = []
    durations = []
    total_duration = 0
    i = 0
    posts, after = get_reddit_posts('mildlyinteresting')
    while total_duration < 60:
        if i == len(posts):
            posts, after = get_reddit_posts('mildlyinteresting', after)
            i = 0
        post = posts[i]
        # create image from reddit data
        file_format = post['url'].split('.')[-1]
        image_path = f"public/image/{i}.{file_format}"
        get_image(post['url'], image_path)
        image_paths.append(image_path)
        print(f"Saved {image_path}")

        # use text-to-speech to create audio
        audio_path = f"public/audio/{i}.mp3"
        speak(audio_path, post['title'])
        audio_paths.append(audio_path)
        print(f"Saved {audio_path}")

        duration = float(get_info(audio_path)['duration'])
        durations.append(round(duration, 3))
        total_duration += duration
        print(f"Total duration: {total_duration:.3f}s")
        i += 1

    print("successfully scraped and generated content")

    song_url = get_song_url()

    open("public/info.json", "w").close()  # empties file
    with open('public/info.json', 'w') as f:
        json.dump({'duration_in_seconds': total_duration, 'durations': durations, 'audio_paths': audio_paths,
                   'image_paths': image_paths, "song_url": song_url}, f, indent=4)

    print("saved info.json")


if __name__ == '__main__':
    create_content()
