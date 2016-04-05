from django.conf.urls import url

from .views import PersonView

urlpatterns = [
    url(
        r'^(?P<pk>[^/]+)/(?P<ignored_slug>.*)$',
        PersonView.as_view(),
        name='person_view'),
]
