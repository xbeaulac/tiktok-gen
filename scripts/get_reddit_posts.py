import requests
from requests.exceptions import HTTPError, Timeout, RequestException
import time
import m3u8


def fetch_url(url, retries=3, delay=5):
    """Created by chatGPT, function that will fetch again if there's an error"""
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url)
            if response.status_code == 500:
                print(f"Server error (500). Retrying in {delay} seconds...")
                attempt += 1
                time.sleep(delay)
            elif response.status_code == 408:
                print(f"Request timeout (408). Retrying in {delay} seconds...")
                attempt += 1
                time.sleep(delay)
            else:
                response.raise_for_status()  # Raise an HTTPError for other bad responses (4xx and 5xx)
                return response
        except (HTTPError, Timeout) as e:
            print(f"Error occurred: {e}. Retrying in {delay} seconds...")
            attempt += 1
            time.sleep(delay)
        except RequestException as e:
            print(f"RequestException occurred: {e}. Aborting...")
            raise e
    print("Max retries exceeded. Aborting...")
    return None


def get_reddit_posts(subreddit: str, after: str = ""):
    posts = []
    url = f"https://www.reddit.com/r/{subreddit}.json"
    if after:
        url = f"{url}?after={after}"
    response = fetch_url(url)
    data = response.json()
    for post in data['data']['children']:
        thumbnail: str = post['data']['thumbnail']
        if thumbnail != 'self' and thumbnail != 'nsfw':
            is_video = True if post['data']['secure_media'] else False
            title: str = post['data']['title'].replace(".", "").replace(",", "").replace('"', '').strip()
            if is_video:
                video_url: str = post['data']['secure_media']['reddit_video']['fallback_url'].split('?')[0]

                height = post['data']['secure_media']['reddit_video']['height']
                width = post['data']['secure_media']['reddit_video']['width']

                m3u8_url = post['data']['secure_media']['reddit_video']['hls_url']
                m3u8_obj = m3u8.load(m3u8_url)
                stream_info = str(m3u8_obj.playlists[0].stream_info).split(',')
                fps = int([info.split('=')[1] for info in stream_info if "FRAME-RATE" in info][0])

                audio_url = video_url.split('/')[:-1]
                audio_url.append('DASH_AUDIO_128.mp4')
                audio_url = '/'.join(audio_url)
                media_url = {'video': video_url, 'audio': audio_url}

                duration = int(post['data']['secure_media']['reddit_video']['duration'])
            else:
                height = post['data']['preview']['images'][0]['source']['height']
                width = post['data']['preview']['images'][0]['source']['width']
                media_url = post['data']['url_overridden_by_dest']
                duration = 0
                fps = 0
            post_json = {
                'title': title,
                'url': media_url,
                'type': 'video' if is_video else 'image',
                'duration': duration,
                'fps': fps,
                'height': height,
                'width': width
            }

            posts.append(post_json)

    return posts, data['data']['after']
