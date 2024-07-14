import requests  # Used for making HTTP requests

# Define constants for the script
CHUNK_SIZE = 1024  # Size of chunks to read/write at a time
XI_API_KEY = "6c4c375d4e1b1cf3bbb7585bbfa9ae17"  # Your API key for authentication
VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # ID of the voice model to use (Adam)
VOICE_SETTINGS = {  # Voice settings for voice model's articulation
    "stability": 0.5,
    "similarity_boost": 0.8,
    "style": 0.0,
    "use_speaker_boost": True
}


def speak(text: str, output: str):
    # Construct the URL for the Text-to-Speech API request
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"

    # Set up headers for the API request, including the API key for authentication
    headers = {
        "Accept": "application/json",
        "xi-api-key": XI_API_KEY
    }

    # Set up the data payload for the API request, including the text and voice settings
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": VOICE_SETTINGS
    }

    # Make the POST request to the TTS API with headers and data, enabling streaming response
    response = requests.post(tts_url, headers=headers, json=data, stream=True)

    # Check if the request was successful
    try:
        if not response.ok:
            raise Exception(response.text)
        # Open the output file in write-binary mode
        with open(output, "wb") as f:
            # Read the response in chunks and write to the file
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
    except Exception as e:
        # Print the error message if the request was not successful
        print(e)
