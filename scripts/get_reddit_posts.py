import json

import requests


def get_reddit_posts(subreddit: str, count: int):
    if count < 0:
        raise ValueError("Count cannot be negative")

    posts = []
    url = f"https://www.reddit.com/r/{subreddit}.json"
    remaining_posts = count
    while remaining_posts > 0:
        response = requests.get(url)
        data = response.json()

        try:
            after = data["data"]["after"]
        except KeyError:
            open('error_file.json', 'w').close()
            with open('error.json', 'w') as error_file:
                error_file.write(json.dumps(data))
                print("Wrote error file to error.json")

        for post in data['data']['children']:
            thumbnail: str = post['data']['thumbnail']
            if thumbnail != 'self' and thumbnail != 'nsfw':
                title: str = post['data']['title']
                image: str = post['data']['url_overridden_by_dest']
                post_json = {
                    'title': title.replace(".", "").replace(",", "").replace('"', '').strip(),
                    'image': image
                }
                posts.append(post_json)
                remaining_posts -= 1

                if remaining_posts == 0:
                    break

        url = f"https://www.reddit.com/r/{subreddit}.json?after={after}"

    return posts
