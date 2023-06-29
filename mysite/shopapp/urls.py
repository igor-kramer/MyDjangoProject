from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    ShopIndexView,
    GroupsListView,
    OrderViewSet,
    OrdersListView,
    OrdersDetailView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    OrdersDataExportView,
    ProductDetailsView,
    ProductsListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductViewSet,
    UsersListView,
    UserOrdersListView,
    UserOrdersDataExportView,
)

app_name = "shopapp"

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("api/", include(routers.urls)),
    path("groups/", GroupsListView.as_view(), name="groups_list"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archived/", ProductDeleteView.as_view(), name="product_delete"),

    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/export/", OrdersDataExportView.as_view(), name="orders-export"),
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
    path("orders/<int:pk>/", OrdersDetailView.as_view(), name="order_details"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),

    path("users/", UsersListView.as_view(), name="users_list"),
    path("users/<int:pk>/orders/", UserOrdersListView.as_view(), name="user_orders"),
    path("users/<int:pk>/orders/export/", UserOrdersDataExportView.as_view(), name="user_orders_export"),
]
