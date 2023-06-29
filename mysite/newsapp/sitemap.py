from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from newsapp.models import News


class NewsSitemap(Sitemap):
    changefreg = "weekly"
    priority = 0.9

    def items(self):
        return News.objects.filter(is_published=True).all()

    def lastmod(self, obj: News):
        return obj.published_at


class StaticViewSitemap(Sitemap):

    def items(self):
        return ['contacts', 'about_us']

    def location(self, item):
        return reverse(item)
