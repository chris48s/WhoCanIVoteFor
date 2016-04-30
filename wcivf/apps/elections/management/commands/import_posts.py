from django.core.management.base import BaseCommand
from django.conf import settings

import requests

from elections.models import Election, Post

class Command(BaseCommand):
    def handle(self, **options):
        next_page = settings.YNR_BASE + '/api/v0.9/posts/?page_size=200'
        while next_page:
            print(next_page)
            req = requests.get(next_page)
            if req.status_code != 200:
                print(req.url)
                print(req.content)
            results = req.json()
            self.add_posts(results)
            next_page = results.get('next')

    def add_posts(self, results):
        for post in results['results']:
            post_obj, created = Post.objects.update_or_create_from_ynr(
                post)
            if created:
                print("Added new post: {0}".format(post['label']))
