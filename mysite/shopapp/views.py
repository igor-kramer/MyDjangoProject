"""
В этом модуле лежат различные наборы представлений.

Разные View интернет-магазина: по товарам, заказам и т.д.
"""

from timeit import default_timer

from django.contrib.auth.models import Group, User
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .forms import GroupForm
from .models import Product, Order
from .serializers import ProductSerializers, OrderSerializers

import logging


logger = logging.getLogger(__name__)


@extend_schema(description="Product views CRUD")
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product
    Полный CRUD для сущностей товара
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ["name", "description"]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]

    @extend_schema(
        summary="Get one product by ID",
        description="Retrieves **product**, returns 404 if not found",
        responses={
            200: ProductSerializers,
            404: OpenApiResponse(description="Empty response, product by ID not found"),
        }
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
            "items": 5,
        }
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)


class ProductDetailsView(DetailView):

    template_name = 'shopapp/products-details.html'
    model = Product
    context_object_name = "product"


class ProductsListView(ListView):
    template_name = 'shopapp/products-list.html'
    # model = Product
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)


class ProductCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        # return self.request.user.groups.filter(name="secret-group").exists()
        return self.request.user.has_perm('add_product')
    model = Product
    fields = "name", "price", "description", "discount"
    success_url = reverse_lazy("shopapp:products_list")

    def get(self, request, *args, **kwargs):
        logger.info(f'Пользователь {self.request.user.username} создал товар!')
        return super().get(request, *args, **kwargs)


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    fields = "name", "price", "description", "discount"
    template_name_suffix = "_update_form"

    def test_func(self):
        return self.request.user == self.get_object().created_by

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk}
        )

    def get(self, request, *args, **kwargs):
        logger.info(f'Пользователь {self.request.user.username} обновил товар!')
        return super().get(request, *args, **kwargs)


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "shopapp.delete_product"
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = [
        "products__name",
        "user__username",
        "delivery_address",
        "promocode",
    ]
    filterset_fields = [
        "delivery_address",
        "promocode",
        "created_at",
        "user__username",
        "products__name",
    ]
    ordering_fields = [
        "user__username",
        "delivery_address",
        "promocode",
    ]


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrdersDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrderCreateView(CreateView):
    model = Order
    fields = "products", "delivery_address", "promocode", "user"
    success_url = reverse_lazy("shopapp:orders_list")

    def get(self, request, *args, **kwargs):
        logger.info('Создан заказ!')
        return super().get(request, *args, **kwargs)


class OrderUpdateView(UpdateView):
    model = Order
    fields = "products", "delivery_address", "promocode", "user"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:order_details",
            kwargs={"pk": self.object.pk}
        )

    def get(self, request, *args, **kwargs):
        logger.info('Обновлен заказ!')
        return super().get(request, *args, **kwargs)


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")


class OrdersDataExportView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by("pk").all()
        orders_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "products": [product.pk for product in order.products.all()],
                "user": order.user.pk,

            }
            for order in orders
        ]
        return JsonResponse({"orders": orders_data})


class UsersListView(ListView):
    template_name = 'shopapp/users-list.html'
    model = User
    context_object_name = "users"


class UserOrdersListView(UserPassesTestMixin, ListView):

    template_name = 'shopapp/user_orders.html'

    def test_func(self):
        return self.request.user.is_authenticated

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.owner = None

    def get_queryset(self):
        self.owner = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return self.owner

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.owner
        context["orders"] = Order.objects.filter(user=self.owner).prefetch_related("products")
        return context


class UserOrdersDataExportView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated

    def get(self, request: HttpRequest, pk) -> JsonResponse:
        cache_key = f"user_{pk}_orders_data_export"
        orders_data = cache.get(cache_key)
        if orders_data is None:
            user = get_object_or_404(User, pk=pk)
            orders = Order.objects.order_by("pk").filter(user=user).prefetch_related("products")
            orders_data = [
                {
                    "pk": order.pk,
                    "delivery_address": order.delivery_address,
                    "promocode": order.promocode,
                    "products": [product.pk for product in order.products.all()],
                    "user": user.pk,

                }
                for order in orders
            ]
            cache.set(cache_key, orders_data, 180)
        return JsonResponse({"orders": orders_data})

