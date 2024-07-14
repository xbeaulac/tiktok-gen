import json

import requests

pathname = "data/female_voices.json"

data = {
    "panel": "tone",
    "appVersion": "14.1.0",
    "sdkVersion": "16.9.0",
    "lang": "en",
    "category": "female_voice",
    "hasCategoryEffects": "false",
    "cc_web_version": "0",
    "only_commercial": "false",
    "offset": "0",
    "sortingPosition": "0"
}

response = requests.post("https://edit-api-va.capcut.com/lv/v1/effect/get_category_effects", json=data)
data = response.json()
open(pathname, 'w').close()  # empty file contents
with open(pathname, 'w') as outfile:
    json.dump(data, outfile, indent=4)
print(f"Saved {pathname}")
