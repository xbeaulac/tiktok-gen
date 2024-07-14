import json
import random


def get_random_voice():
    random_gender = random.choice(['male', 'female'])
    with open(f"data/{random_gender}_voices.json", "r") as f:
        data = json.load(f)
        voices_count = data['data']['CategoryEffects']['Cursor']
        random_voice = data['data']['CategoryEffects']['Effects'][random.randint(0, voices_count - 1)]
        return json.loads(json.loads(random_voice['Extra'])['tonetype'])['voice_type']
