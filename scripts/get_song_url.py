import requests
from playwright.sync_api import sync_playwright


def get_headers(playwright):
    browser = playwright.chromium.launch(headless=True, timeout=(10 * 1000))
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    context = browser.new_context(user_agent=user_agent)
    page = context.new_page()

    request_sent = False
    headers = {}

    # Intercept and log network request
    def log_request(route, request):
        if request.url.startswith("https://ads.tiktok.com/creative_radar_api/v1/popular_trend/sound/rank_list"):
            print(f"Request: {request.headers}")
            nonlocal request_sent
            nonlocal headers
            request_sent = True
            headers.update(request.headers)
        route.continue_()

    page.route("**/*", log_request)

    # Navigate to a page
    page.goto("https://ads.tiktok.com/business/creativecenter/inspiration/popular/music/pad/en")

    # Perform actions on the page if needed
    page.reload()
    page.click('div[role="button"] >> span:has-text("Please Select")')
    page.click('div.byted-select-popover-panel-inner >> div:has-text("United States")')

    if request_sent:
        browser.close()

    while not request_sent:
        pass

    return headers


def get_song_url():
    with sync_playwright() as playwright:
        headers = get_headers(playwright)

    url = "https://ads.tiktok.com/creative_radar_api/v1/popular_trend/sound/rank_list?period=7&page=1&limit=10&rank_type=popular&new_on_board=false&commercial_music=false&country_code=US"
    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)
    song_id = data['data']['sound_list'][0]['clip_id']

    url = f"https://www.tiktok.com/api/music/item_list/?aid=1988&count=2&cursor=0&musicID={song_id}"
    response = requests.get(url)
    data = response.json()
    song_url = data["itemList"][0]["music"]["playUrl"]

    return song_url


if __name__ == '__main__':
    print(get_song_url())
