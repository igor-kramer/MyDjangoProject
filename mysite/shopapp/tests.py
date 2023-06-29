from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from shopapp.models import Order


class OrderDetailViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="probe_name", password="qwerty")
        cls.user.user_permissions.add(Permission.objects.get(codename="view_order"))
    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.order = Order.objects.create(delivery_address='ul Pupkina, d 8',
                                          promocode='SALE123',
                                          created_at='2023-03-24 09:45:12.123293',
                                          user_id=1,
                                          pk=3)

    def tearDown(self) -> None:
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(reverse("shopapp:order_details", kwargs={'pk': self.order.pk}))
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        response_order = response.context['order']
        self.assertEqual(response_order.pk, self.order.pk)

    def test_orders_details_not_authenticaded(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:order_details", kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("myauth:login"), response.url)


class OrdersExportViewTestCase(TestCase):
    fixtures = [
        'users-fixture.json',
        'products-fixture.json',
        'orders-fixture.json',
    ]


    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="probe_name", password="qwerty", is_staff=True)
        cls.user.user_permissions.add(Permission.objects.get(codename="view_order"))
    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_order_view(self):
        response = self.client.get(
            reverse("shopapp:orders-export"),
        )
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "products": [product.pk for product in order.products.all()],
                "user": order.user.pk,

            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(
            orders_data["orders"],
            expected_data,
        )
