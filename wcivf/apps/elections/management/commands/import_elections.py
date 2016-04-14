from django.core.management.base import BaseCommand
from django.conf import settings

import requests

from elections.models import Election


class Command(BaseCommand):
    def handle(self, **options):
        next_page = settings.YNR_BASE + '/api/v0.9/elections/'
        while next_page:
            req = requests.get(next_page)
            results = req.json()
            self.add_elections(results)
            next_page = results.get('next')

    def add_elections(self, results):
        for election in results['results']:
            election_obj, created = Election.objects.update_or_create_from_ynr(
                election)
            if created:
                print("Added new election: {0}".format(election['name']))
