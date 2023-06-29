from django.shortcuts import render
from django.views.generic import ListView

from blogapp.models import Article


class ArticlesListView(ListView):
    queryset = (
        Article.objects
        .select_related("author")
        .prefetch_related("tags")
        .defer("content")
    )
