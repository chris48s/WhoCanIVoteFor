import os
import csv

from django.core.management.base import BaseCommand
from django.conf import settings

from people.models import PersonPost
from profiles.models import Profile

class Command(BaseCommand):
    def handle(self, **options):
        election_id = "pcc.2016-05-05"
        data = open(
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    '../../data/pcc.2016.profiles.csv'
                )
            )
        )
        for line in csv.DictReader(data):
            try:
                person_post = PersonPost.objects.get(
                    election__slug=election_id, person__ynr_id=line['ynr_id'])
                self.add_profile(person_post, line)
            except PersonPost.DoesNotExist:
                print(line['ynr_id'])

    def add_profile(self, person_post, line):
        text = line['chat']
        # text = text.replace('\n', '\n\n')

        profile = Profile.objects.update_or_create(
            person_post=person_post,
            defaults={
                'text': text,
                'url': line['url'],
            }
        )
