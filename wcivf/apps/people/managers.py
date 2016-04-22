import requests

from django.db import models
from django.core.files import File

from django.core.files.temp import NamedTemporaryFile


from elections.models import Election, Post
from parties.models import Party


class PersonPostQuerySet(models.QuerySet):
    def by_party(self):
        return self.order_by('person__party__party_name')


class PersonPostManager(models.Manager):
    def get_queryset(self):
        return PersonPostQuerySet(self.model, using=self._db)

    def by_party(self):
        return self.get_queryset().by_party()


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
                if membership['on_behalf_of']:
                    post.party_id = membership['on_behalf_of']['id']
                else:
                    post.party_id = None
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
            from .models import PersonPost
            # Delete old posts for this person
            PersonPost.objects.filter(person=person_obj).delete()
            for post in posts:
                defaults = {
                    'list_position': post.party_list_position
                }
                if post.party_id:
                    defaults['party'] = Party.objects.get(party_id=post.party_id)
                PersonPost.objects.update_or_create(
                    post=post,
                    person=person_obj,
                    defaults=defaults
                )
        if elections:
            person_obj.elections.add(*elections)

        return (person_obj, _)
