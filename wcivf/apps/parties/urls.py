from django.conf.urls import url

from .views import PartiesView, PartyView

urlpatterns = [
    url(
        r'^$',
        PartiesView.as_view(),
        name='parties_view'),
    url(
        r'^(?P<pk>[^/]+)/(?P<ignored_slug>.*)$',
        PartyView.as_view(),
        name='party_view'),
]
