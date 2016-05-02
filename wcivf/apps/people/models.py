from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify

from wcivf import settings

from elections.models import Election, Post
from parties.models import Party

from .managers import PersonPostManager, PersonManager


class PersonPost(models.Model):
    person = models.ForeignKey('Person')
    post = models.ForeignKey(Post)
    party = models.ForeignKey(Party, null=True)
    election = models.ForeignKey(Election, null=True)
    list_position = models.IntegerField(blank=True, null=True)
    objects = PersonPostManager()

    def __str__(self):
        return "{} ({}, {})".format(
            self.person.name,
            self.post.label,
            self.election.slug
        )



class Person(models.Model):
    ynr_id = models.CharField(max_length=255, db_index=True)
    name = models.CharField(blank=True, max_length=255)
    email = models.EmailField(null=True)
    gender = models.CharField(blank=True, max_length=255, null=True)
    birth_date = models.CharField(null=True, max_length=255)
    photo = models.ImageField(upload_to="people/photos", null=True)

    # contact points
    twitter_username = models.CharField(blank=True, null=True, max_length=100)
    facebook_page_url = models.CharField(blank=True, null=True, max_length=800)
    facebook_personal_url = models.CharField(blank=True, null=True, max_length=800)
    linkedin_url = models.CharField(blank=True, null=True, max_length=800)
    homepage_url = models.CharField(blank=True, null=True, max_length=800)

    #Bios
    wikipedia_url = models.CharField(blank=True, null=True, max_length=800)
    wikipedia_bio = models.TextField(null=True)

    posts = models.ManyToManyField(Post, through=PersonPost)
    elections = models.ManyToManyField(Election)

    objects = PersonManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('person_view', args=[
                str(self.ynr_id),
                slugify(self.name)
            ])

    def get_ynr_url(self):
        return "{}/person/{}/".format(settings.YNR_BASE, self.ynr_id)

