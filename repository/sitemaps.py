from django.contrib.sitemaps import Sitemap
from repository.models import Person, Poetry


class PersonSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return Person.objects.all()

    def lastmod(self, obj):
        return obj.date_modified


class PoetrySitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return Poetry.published.all()

    def lastmod(self, obj):
        return obj.date_modified
