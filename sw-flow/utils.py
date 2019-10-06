# -*- coding: utf-8 -*-
from __future__ import print_function

import os

import requests
import ujson as json
import exceptions

SWAPI_URL = 'https://swapi.co/api'

PEOPLE = 'people'
PLANETS = 'planets'
STARSHIPS = 'starships'
VEHICLES = 'vehicles'
FILMS = 'films'
SPECIES = 'species'

RESOURCES = (FILMS, PEOPLE, PLANETS, STARSHIPS, VEHICLES, SPECIES)


DATASET_PATH = 'dataset'

def query(query_url):
    headers = {'User-Agent': 'swapi-python'}
    response = requests.get(query_url, headers=headers)
    if response.status_code != 200:
        raise exceptions.ValueError('Resource does not exist')

    return response.content


def all_resource_urls(query_url):
    ''' Get all the URLs for every resource '''
    urls = []
    next_page = True
    while next_page:
        response = query(query_url)
        json_data = json.loads(response)

        for resource in json_data['results']:
            urls.append(resource['url'])
        if bool(json_data['next']):
            query_url = json_data['next']
        else:
            next_page = False

    return urls


if not os.path.exists(DATASET_PATH):
    os.makedirs(DATASET_PATH)

for resource in RESOURCES:

    resource_urls = (all_resource_urls('{0}/{1}'.format(SWAPI_URL, resource)))
    print(resource_urls)
    with open('{0}/{1}.json'.format(DATASET_PATH, resource), 'w') as json_file:
        json_file.write('\n'.join(map(query, resource_urls)))
