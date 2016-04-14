from django.contrib.gis.db import models

from django_extensions.db.models import TimeStampedModel


class LoggedPostcode(TimeStampedModel):
    postcode = models.CharField(max_length=100)
    utm_source = models.CharField(blank=True, max_length=100, db_index=True)
    utm_medium = models.CharField(blank=True, max_length=100, db_index=True)
    utm_campaign = models.CharField(blank=True, max_length=100, db_index=True)


    def __str__(self):
        return "{0}".format(self.postcode)
