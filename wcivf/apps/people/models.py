import requests

from django.db import models
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.urlresolvers import reverse
from django.utils.text import slugify

from elections.models import Election, Post
from parties.models import Party


class PersonManager(models.Manager):
    def update_or_create_from_ynr(self, person):
        posts = []
        elections = []

        defaults = {
            'name': person['name'],
            'email': person['email'] or None,
            'gender': person['gender'] or None,
            'birth_date': person['birth_date'] or None,
        }

        version_data = person['versions'][0]['data']
        if 'twitter_username' in version_data:
            defaults['twitter_username'] = version_data['twitter_username']
        if 'facebook_page_url' in version_data:
            defaults['facebook_page_url'] = version_data['facebook_page_url']
        if 'facebook_personal_url' in version_data:
            defaults['facebook_personal_url'] = \
                version_data['facebook_personal_url']
        if 'linkedin_url' in version_data:
            defaults['linkedin_url'] = version_data['linkedin_url']
        if 'homepage_url' in version_data:
            defaults['homepage_url'] = version_data['homepage_url']
        if 'wikipedia_url' in version_data:
            defaults['wikipedia_url'] = version_data['wikipedia_url']

        if person['memberships']:
            for membership in person['memberships']:

                if membership['election']:
                    election, _ = Election.objects.update_or_create(
                        slug=membership['election']['id'],
                        name=membership['election']['name'],
                    )
                elections.append(election)

                if membership['post']:
                    post, _ = Post.objects.update_or_create(
                        ynr_id=membership['post']['id'],
                        label=membership['post']['label'],
                    )
                post.party_list_position = membership['party_list_position']
                posts.append(post)

            if person['memberships'][0]['on_behalf_of']:
                defaults['party'] = Party.objects.get(
                    pk=person['memberships'][0]['on_behalf_of']['id'])

        person_obj, _ = self.update_or_create(
            ynr_id=person['id'],
            defaults=defaults
        )

        if person['memberships']:
            person_obj.party = Party.objects.get(
                pk=person['memberships'][0]['on_behalf_of']['id'])
            person_obj.save()

        if person['thumbnail']:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(requests.get(person['thumbnail']).content)
            img_temp.flush()

            person_obj.photo.save(person['thumbnail'], File(img_temp))
            person_obj.save()

        if posts:
            for post in posts:
                # Delete old posts for this person
                PersonPost.objects.filter(person=person_obj).delete()

                PersonPost.objects.update_or_create(
                    post=post,
                    person=person_obj,
                    defaults={
                        'list_position': post.party_list_position,
                    }
                )
        if elections:
            person_obj.elections.add(*elections)

        return (person_obj, _)


class PersonPost(models.Model):
    person = models.ForeignKey('Person')
    post = models.ForeignKey(Post)
    list_position = models.IntegerField(blank=True, null=True)


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

    party = models.ForeignKey(Party, null=True)
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
