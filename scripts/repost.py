import json

from get_reddit_posts import get_reddit_posts
from speak import speak
from get_info import get_info


def create_content(subreddit: str, num_posts=1, min_duration=60):
    posts_json = []
    post_duration = 0
    i = 0
    posts, after = get_reddit_posts(subreddit)
    for num_post in range(num_posts):
        while post_duration < min_duration:
            if i == len(posts):
                posts, after = get_reddit_posts(subreddit, after)
                i = 0
            post = posts[i]
            audio_path = f'public/audio/{post["id"]}.mp3'
            speak(pathname=audio_path, text=post['title'])
            print(f"Saved {audio_path}")
            audio_duration = float(get_info(audio_path)['duration'])
            post['audio_path'] = audio_path
            post['audio_duration'] = audio_duration
            posts_json.append(post)
            post_duration += post['duration'] + audio_duration
            i += 1
        post_duration = 0

    open('public/info.json', 'w').close()
    with open('public/info.json', 'w') as outfile:
        json.dump({"data": posts_json}, outfile, indent=4)
        print('Saved public/info.json')

    return posts_json


if __name__ == '__main__':
    create_content('Damnthatsinteresting', num_posts=3)
