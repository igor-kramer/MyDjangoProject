from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from django.utils.translation import gettext_lazy as _, ngettext

from .forms import AvatarForm
from .models import Profile

import logging

logger = logging.getLogger(__name__)


class HelloView(View):
    welcome_message = _("Hello World!")

    def get(self, request: HttpRequest) -> HttpResponse:
        items_str = request.GET.get("items") or 0
        items = int(items_str)
        products_line = ngettext(
            "one product",
            "{count} products",
            items,
        )
        products_line = products_line.format(count=items)
        return HttpResponse(
            f"<h1>{self.welcome_message}</h1>"
            f"<h2>{products_line}</h2>"
        )


class AboutMeView(DetailView):

    template_name = "myauth/about-me.html"
    model = User
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        context["form"] = AvatarForm(instance=profile)
        return context

    def post(self, request: HttpRequest, pk):
        profile, created = Profile.objects.get_or_create(user=User.objects.get(id=pk))
        form = AvatarForm(request.POST, request.FILES, instance=profile)
        if form.is_valid() and self.request.user.pk == profile.user.pk:
            form.save()
        else:
            raise PermissionDenied

        return redirect(request.path)


class UsersListView(LoginRequiredMixin, ListView):
    template_name = 'myauth/users.html'
    model = User
    context_object_name = "users"


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    # success_url = reverse_lazy("myauth:about-me")

    def get_success_url(self):
        return reverse(
            "myauth:about-me",
            kwargs={"pk": self.object.pk}
        )

    def form_valid(self, form):
        response = super().form_valid(form)

        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password)
        login(request=self.request, user=user)

        logger.info(f"Пользователь {user.username} прошёл аутентификацию!")
        return response


class MyLoginView(LoginView):

    def get_success_url(self):
        logger.info(f'Пользователь {self.request.user.username} прошёл аутентификацию!')
        return reverse(
            "myauth:about-me",
            kwargs={"pk": self.request.user.pk}
        )


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/admin/')
        return render(request, 'myauth/login.html')

    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/admin/')

    return render(request, "myauth/login.html", {"error": "Invalid login credentials"})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect(reverse("myauth:login"))


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    responce = HttpResponse("Cookie set")
    responce.set_cookie("fizz", "buzz", max_age=3600)
    return responce


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})
