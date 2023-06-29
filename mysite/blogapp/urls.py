from django.urls import path

from blogapp.views import ArticlesListView

urlpatterns = [
    path("articles/", ArticlesListView.as_view(), name="articles_list")
]