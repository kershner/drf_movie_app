from django.conf import settings
import requests
import random
import json
import os


def get_parameters():
    # Load params from JSON file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    params_path = '{}\parameters.json'.format(base_dir)
    with open(params_path) as f:
        params = json.load(f)
        return params


def tmdb_request(endpoint, extra_params=''):
    params = get_parameters()
    full_api_url = '{}{}?api_key={}{}'.format(settings.BASE_TMDB_API_URL, endpoint, params['tmdb_api_key'], extra_params)
    r = requests.get(full_api_url)
    return r


def get_random_pks(pks, limit=20):
    random_pks = []
    for num in range(limit):
        random_pks.append(random.choice(pks))
    return random_pks
