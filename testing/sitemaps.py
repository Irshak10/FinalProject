from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from testing.models import Article


class IndexViewSitemap(Sitemap):

    changefreq = 'daily'

    def items(self):
        return ['index', 'all_news', 'library']

    def location(self, obj):
        return reverse(obj)


class ArticleSitemap(Sitemap):

    def items(self):
        return Article.objects.all()
