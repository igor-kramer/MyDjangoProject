from rest_framework import serializers

from .models import Product, Order


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "pk",
            "name",
            "description",
            "price",
            "discount",
            "created_at",
            "archived",
        )


class OrderSerializers(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    products = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "delivery_address",
            "promocode",
            "created_at",
            "username",
            "products",
        )

    def get_products(self, model):
        products = Product.objects.select_related("created_by").all()
        for product in products:
            yield product.name

