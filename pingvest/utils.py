import requests
import json
import os
import logging

logger = logging.getLogger('app.utils')


def make_get_request_to_json(url, params):
    logger.debug('requesting json from alpha vantage api.')
    r = requests.get(url, params)
    logger.debug(F'request status code: {r.status_code}')
    if r.status_code == 200:
        response_dict = r.json()
        if 'Error Message' in response_dict:
            logger.exception('error message in response. : ' + response_dict['Error Message'])
            raise Exception(response_dict['Error Message'] + F' URL: {url}, params: {params}')
        else:
            return response_dict
    else:
        logger.error(r.text)
        r.raise_for_status()


def make_request_to_csv(url, params):
    logger.debug('requesting csv from alpha vantage api.')
    r = requests.get(url, params)
    logger.debug(F'request status code: {r.status_code}')
    if r.status_code == 200:
        return r.content.decode('utf-8')
    else:
        logger.error(r.text)
        r.raise_for_status()


def get_api_key():
    logger.debug('fetching api key for alpha vantage api.')
    with open('./alphavantage_apikey.txt') as f:
        key = f.read()
    return key


def read_json(path):
    with open(path) as f:
        data = json.load(f)
    return data


def save_json(d, path):
    with open(path, "w") as f:
        json.dump(d, f)


def notify(title, text):
    os.system(
        """
        osascript -e 'display notification "{}" with title "{}"'
        """.format(text, title))
