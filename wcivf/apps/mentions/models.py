from django.db import models

from people.models import Person
from elections.models import Post

class MentionsManager(models.Manager):
    def get_or_create_from_em(self, mention):
        defaults = {
            'date_order': mention['date_order'],
            'date_published': mention['date_published'],
            'quote': mention['quote'],
            'quote': mention['quote']['html'],
            'truncated_left': mention['quote']['truncated']['left'],
            'truncated_right': mention['quote']['truncated']['right'],
            'stream_item_id': mention['stream_item_id'],
            'title': mention['title'],
            'url': mention['url'],
        }

        mention_obj, _ = self.get_or_create(
            article_id=mention['article_id'],
            defaults=defaults
        )

        mention_obj.save()

        for person_id in mention['people_ids']:
            try:
                person = Person.objects.get(ynr_id=int(person_id))
                mention_obj.people.add(person)
            except Person.DoesNotExist:
                pass



        for post_id in mention['post_ids']:
            mention_obj.posts.add(post_id)

        mention_obj.save()
        return (mention_obj, _)


class Mention(models.Model):
    article_id = models.CharField(max_length=50, db_index=True)
    date_order = models.DateTimeField()
    date_published = models.DateTimeField(null=True)
    quote = models.TextField(blank=True)
    truncated_left = models.BooleanField(default=False)
    truncated_right = models.BooleanField(default=False)
    stream_item_id = models.CharField(max_length=50, db_index=True)
    title = models.CharField(blank=True, max_length=500)
    url = models.URLField(blank=False, max_length=800)
    people = models.ManyToManyField(Person)
    posts = models.ManyToManyField(Post)

    objects = MentionsManager()

    class Meta:
        ordering = ['-date_published']

    def __str__(self):
        return "{} ({})".format(self.article_id, self.title)
