from django.core.management.base import BaseCommand
from django.conf import settings

import requests

from people.models import Person
from people.helpers import get_wikipedia_extract




class Command(BaseCommand):
    def handle(self, **options):
        for person in Person.objects.exclude(wikipedia_url=None).exclude(wikipedia_url=''):
            person.wikipedia_bio = get_wikipedia_extract(person)
            person.save()
