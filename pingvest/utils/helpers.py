import requests
import json
import os


def make_request(url, params):
    r = requests.get(url, params)
    if r.status_code == 200:
        return r.json()
    else:
        r.raise_for_status()


def get_api_key():
    with open('./apikey.txt') as f:
        key = f.read()
    return key


def load_sample():
    with open('./data.json') as f:
        data = json.load(f)
    return data


def notify(title, text):
    os.system(
        """
        osascript -e 'display notification "{}" with title "{}"'
        """.format(text, title))