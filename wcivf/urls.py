from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.views.decorators.cache import cache_page

from elections.sitemaps import ElectionSitemap, PostSitemap
from people.sitemaps import PersonSitemap

sitemaps = {
    'elections': ElectionSitemap,
    'posts': PostSitemap,
    'people': PersonSitemap,
}

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('core.urls')),
    url(r'^elections/', include('elections.urls')),
    url(r'^person/', include('people.urls')),
    url(r'^sitemap\.xml$', cache_page(86400)(sitemap), {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

