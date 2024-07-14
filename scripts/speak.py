import json
import requests
from websocket import create_connection


def use_web_socket(pathname: str, url: str, message: dict):
    ws = create_connection(url)
    ws.send(json.dumps(message))  # send message to use text-to-speech
    ws.recv()  # start
    open(pathname, 'w').close()  # empty contents of file
    response = ws.recv()
    while isinstance(response, bytes):
        with open(pathname, 'wb') as f:
            f.write(response)
        response = ws.recv()
    ws.close()


def get_tts_token():
    res = requests.post("https://edit-api-va.capcut.com/lv/v1/common/tts/token",
                        headers={
                            "Appvr": "5.8.0",
                            "Device-Time": "1720624021",
                            "Pf": "7",
                            "Sign": "c60b925d979c30d793fc11245c48548f",
                            "Sign-Ver": "1"
                        })

    return res.json()['data']['token']


def speak(pathname: str, text: str):
    token = get_tts_token()

    message = {
        "token": token,
        "appkey": "OXZXHOnduo",
        "namespace": "TTS",
        "event": "StartTask",
        "payload": '{\"pitch_rate\":10,\"speech_rate\":10,\"sample_rate\":24000,\"ssml\":\"\",\"speaker\":\"'
                   + 'en_us_006' + '\",\"text\":\"' + text + '\",\"audio_config\":{}}'
    }

    url = 'wss://sami-maliva.byteintlapi.com/internal/api/v1/ws'

    use_web_socket(pathname, url, message)


if __name__ == '__main__':
    print("Token: " + get_tts_token())
