from urllib.parse import urlencode

import requests

from .models import PersonPost


def get_wikipedia_extract(person):
    """
    Adapted from code written by @andylolz:
    https://github.com/DemocracyClub/YourNextMP-Read/blob/master/_scripts/get_wikipedia_extracts.py
    """
    base_url = "http://en.wikipedia.org/w/api.php"
    wiki_title = person.wikipedia_url.strip('/').split('/')[-1]
    params = {
        'titles': wiki_title,
        'format': 'json',
        'action': 'query',
        'prop': 'extracts',
        'exintro': '',
        'explaintext': '',
        'redirects': '',
    }
    url = "{}?{}".format(base_url, urlencode(params))

    api_url = url.format(wiki_title)

    resp = requests.get(api_url).json()
    page_id = list(resp['query']['pages'].keys())[0]
    full = resp['query']['pages'][page_id]

    if 'extract' in full:
        first_para = full['extract'].split('\n')[0]
    else:
        first_para = None

    return first_para


def peopleposts_for_election_post(election, post):
    return PersonPost.objects.filter(election=election, post=post)
