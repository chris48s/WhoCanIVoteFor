import datetime

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify


from .managers import ElectionManager, PostManager


class Election(models.Model):
    slug = models.CharField(max_length=128, unique=True)
    election_date = models.DateField()
    name = models.CharField(max_length=128)
    current = models.BooleanField()
    description = models.TextField()
    ballot_colour = models.CharField(blank=True, max_length=100)
    election_type = models.CharField(blank=True, max_length=100)
    voting_system = models.ForeignKey('VotingSystem', null=True)
    uses_lists = models.BooleanField(default=False)
    voter_age = models.CharField(blank=True, max_length=100)
    voter_citizenship = models.TextField(blank=True)

    objects = ElectionManager()

    class Meta:
        ordering = ['election_date']

    def __str__(self):
        return self.name

    def in_past(self):
        return self.election_date < datetime.date.today()

    @property
    def nice_election_name(self):
        if self.election_type == "local":
            return "Local"
        if self.election_type == "sp":
            return "Scottish parliament"
        if self.election_type == "naw":
            return "Welsh assembly"
        if self.election_type == "gla":
            return "Greater London assembly"
        if self.election_type == "pcc":
            return "Police and crime commissioner"
        if self.election_type == "mayor":
            return "City mayor"
        if self.election_type == "nia":
            return "Northern Ireland assembly"
        return self.name

    def get_absolute_url(self):
        return reverse('election_view', args=[
                str(self.slug),
                slugify(self.name)
            ])


class Post(models.Model):
    """
    A post has an election and candidates
    """
    ynr_id = models.CharField(blank=True, max_length=100, primary_key=True)
    label = models.CharField(blank=True, max_length=255)
    role = models.CharField(blank=True, max_length=255)
    group = models.CharField(blank=True, max_length=100)
    organization = models.CharField(blank=True, max_length=100)
    area_name = models.CharField(blank=True, max_length=100)
    area_id = models.CharField(blank=True, max_length=100)
    election = models.ForeignKey(Election)

    objects = PostManager()

    def get_absolute_url(self):
        return reverse('post_view', args=[
                str(self.election.slug),
                str(self.ynr_id),
                slugify(self.label)
            ])


class VotingSystem(models.Model):
    slug = models.SlugField(primary_key=True)
    name = models.CharField(blank=True, max_length=100)
    wikipedia_url = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
