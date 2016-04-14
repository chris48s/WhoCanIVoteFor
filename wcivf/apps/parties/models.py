import requests

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import models
from django.conf import settings


class PartyManager(models.Manager):
    def update_or_create_from_ynr(self, party):
        defaults = {
            'party_name': party['name']
        }

        party_obj, _ = self.update_or_create(
            party_id=party['id'],
            defaults=defaults
        )
        if party['images']:
            selected_image = party['images'][0]
            for image in party['images']:
                if image['is_primary']:
                    selected_image = image

            url = "{}{}".format(settings.YNR_BASE, selected_image['image_url'])

            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(requests.get(url).content)
            img_temp.flush()

            party_obj.emblem.save(url, File(img_temp))
            party_obj.save()

        return (party_obj, _)


class Party(models.Model):
    """
    Represents a UK political party.
    """
    party_id = models.CharField(blank=True, max_length=100, primary_key=True)
    party_name = models.CharField(max_length=765)
    emblem = models.ImageField(upload_to="parties/emblems", null=True)

    class Meta:
        verbose_name_plural = 'Parties'
        ordering = ('party_name', )

    objects = PartyManager()

    def __str__(self):
        return "%s (%s)" % (self.party_name, self.pk)
