import urllib.request


def get_image(image_url: str, filename: str):
    urllib.request.urlretrieve(image_url, filename)
