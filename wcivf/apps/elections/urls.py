from django.conf.urls import url

from .views import PostcodeView, ElectionsView, ElectionView, PostView

urlpatterns = [
    url(
        r'^$',
        ElectionsView.as_view(),
        name='elections_view'),
    url(
        r'^(?P<pk>[a-z0-9\.\-]+)/(?P<ignored_slug>[^/]+)$',
        ElectionView.as_view(),
        name='election_view'),
    url(
        r'^(?P<pk>[a-z0-9\.\-]+)/post-(?P<post_id>.*)/(?P<ignored_slug>[^/]+)$',
        PostView.as_view(),
        name='post_view'),
    url(
        r'^(?P<postcode>[^/]+)/$',
        PostcodeView.as_view(),
        name='postcode_view'),
]
