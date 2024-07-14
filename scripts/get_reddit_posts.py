import requests


def get_reddit_posts(subreddit: str, after: str = ""):
    posts = []
    url = f"https://www.reddit.com/r/{subreddit}.json"
    if after:
        url = f"{url}?after={after}"
    response = requests.get(url)
    data = response.json()
    try:
        data['data']
    except KeyError as e:
        print(e)
        print(data)
    for post in data['data']['children']:
        thumbnail: str = post['data']['thumbnail']
        if thumbnail != 'self' and thumbnail != 'nsfw':
            is_video = True if post['data']['secure_media'] else False
            title: str = post['data']['title'].replace(".", "").replace(",", "").replace('"', '').strip()
            if is_video:
                media_url: str = post['data']['secure_media']['reddit_video']['fallback_url']
            else:
                media_url: str = post['data']['url_overridden_by_dest']
            post_json = {
                'title': title,
                'url': media_url,
                'type': 'video' if is_video else 'image'
            }

            posts.append(post_json)

    return posts, data['data']['after']
