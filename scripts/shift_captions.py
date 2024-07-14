import json


def shift_captions(pathname: str, shift: float = 0.0):
    with open(pathname, "r") as f:
        data = json.load(f)

    first_caption_time = data['transcription'][0]['startInSeconds']

    if shift == 0.0:
        shift_value = first_caption_time - 0.01
    else:
        shift_value = shift

    if shift_value > first_caption_time:
        raise ValueError(f'shift too high, must be less than or equal to {first_caption_time}')
    for caption in data['transcription']:
        caption['startInSeconds'] -= shift_value
        round(caption['startInSeconds'], 2)

    with open(pathname, "w") as f:
        json.dump(data, f, indent=4)
        print(f"Shifted captions by {shift_value} seconds")

if __name__ == "__main__":
    shift_captions("public/temp.json")
