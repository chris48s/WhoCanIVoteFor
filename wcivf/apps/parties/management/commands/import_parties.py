from django.core.management.base import BaseCommand
from django.conf import settings

import requests

from parties.models import Party


class Command(BaseCommand):
    def handle(self, **options):

        next_page = settings.YNR_BASE + '/api/v0.9/organizations/?page_size=200'
        while next_page:
            req = requests.get(next_page)
            results = req.json()
            self.add_people(results)
            next_page = results.get('next')

    def add_people(self, results):
        for party in results['results']:
            if not party['classification'] == "Party":
                continue

            party_obj, created = Party.objects.update_or_create_from_ynr(
                party)
            if created:
                print("Added new party: {0}".format(party['name']))
