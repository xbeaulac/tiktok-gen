import json

import requests

response = requests.get("https://api.elevenlabs.io/v1/voices")
data = response.json()

with open('data/voices.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)
