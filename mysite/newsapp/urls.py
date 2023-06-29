from django.urls import path

from newsapp.feeds import LatestNewsFeed
from newsapp.views import contacts, about_us, HousingListView, NewsListView, NewsDetailView

urlpatterns = [
    path("contacts/", contacts, name="contacts"),
    path("about_us/", about_us, name="about_us"),
    path("", NewsListView.as_view(), name="housing_list"),
    path("<int:pk>", NewsDetailView.as_view(), name="housing_detail"),
    path("feed/", LatestNewsFeed()),
]
