from django.contrib.syndication.views import Feed
from django.db.models import QuerySet
from django.urls import reverse
from newsapp.models import News


class LatestNewsFeed(Feed):
    title = "News"
    link = "/sitenews/"
    description = "Latest news"

    def items(self) -> QuerySet:
        return News.objects.order_by('-published_at')[10:]

    def item_title(self, item: News) -> str:
        return item.title

    def item_description(self, item: News) -> str:
        return item.description

    def item_link(self, item: News) -> str:
        return reverse('news-item', args=[item.pk])
