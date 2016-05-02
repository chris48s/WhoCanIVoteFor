from django.db import models


class Profile(models.Model):
    person_post = models.OneToOneField('people.PersonPost', primary_key=True)
    text = models.TextField(blank=True)
    url = models.CharField(blank=True, max_length=800)
