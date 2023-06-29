from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from newsapp.models import Housing, News


def contacts(request: HttpRequest):
    context = {
        "phone_number": "8(999)999-99-99",
        "email": "Thisnews@gmail.com",
    }
    return render(request, "newsapp/contacts.html", context=context)


def about_us(request: HttpRequest):
    context = {
        "info": """We are a real estate agency.
        Our company has been operating in the real
        estate market for over 20 years.
        """,
    }
    return render(request, "newsapp/about_us.html", context=context)


class HousingListView(ListView):
    queryset = (
        Housing.objects
        .select_related("housing_type")
        .all()
    )


class NewsListView(ListView):
    queryset = News.objects.filter(is_published=False)


class NewsDetailView(DetailView):
    model = News
    template_name = "newsapp/news_detail.html"
    context_object_name = "new"
