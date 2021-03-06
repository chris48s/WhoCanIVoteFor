from django.db import models


class ElectionManager(models.Manager):
    def update_or_create_from_ynr(self, election):
        election_type = self.election_id_to_type(election['id'])

        election_weight = 10
        if election['party_lists_in_use']:
            election_weight = 20
        if election_type == 'mayor':
            election_weight = 5

        return self.update_or_create(
            slug=election['id'],
            defaults={
                'election_date': election['election_date'],
                'name': election['name'].replace('2016', '').strip(),
                'current': election['current'],
                'description': election['description'],
                'election_type': election_type,
                'uses_lists': election['party_lists_in_use'],
                'for_post_role': election['for_post_role'],
                'election_weight': election_weight,
            }
        )

    def election_id_to_type(self, election_id):
        parts = election_id.split('.')
        return parts[0]


class PostManager(models.Manager):
    def update_or_create_from_ynr(self, post):
        from .models import Election
        election = Election.objects.get(slug=post['elections'][0]['id'])
        return self.update_or_create(
            ynr_id=post['id'],
            defaults={
                'label': post['label'],
                'role': post['role'],
                'group': post['group'],
                'organization': post['organization']['name'],
                'area_name': post['area']['name'],
                'area_id': post['area']['identifier'],
                'election': election
            }
        )
