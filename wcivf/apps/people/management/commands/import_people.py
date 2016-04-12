from django.core.management.base import BaseCommand
from django.conf import settings

import requests

from people.models import Person


class Command(BaseCommand):
    def handle(self, **options):
        self.existing_people = set(Person.objects.values_list('pk', flat=True))
        self.seen_people = set()

        next_page = settings.YNR_BASE + '/api/v0.9/persons/?page_size=200'
        while next_page:
            req = requests.get(next_page)
            results = req.json()
            self.add_people(results)
            next_page = results.get('next')

        deleted_ids = self.existing_people.difference(self.seen_people)
        Person.objects.filter(ynr_id__in=deleted_ids).delete()

    def add_people(self, results):
        for person in results['results']:
            person_obj, created = Person.objects.get_or_create_from_ynr(
                person)
            self.seen_people.add(person['id'])
            if created:
                print("Added new person: {0}".format(person['name']))
