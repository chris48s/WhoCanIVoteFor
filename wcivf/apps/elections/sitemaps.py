from django.contrib.sitemaps import Sitemap
from .models import Election, Post


class ElectionSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return Election.objects.all()


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.2
    protocol = "https"

    def items(self):
        return Post.objects.all()
