from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from restaurant.models import DishType

DISH_TYPE_URL = reverse("restaurant:dish-type-list")


class PublicDishTypeTests(TestCase):
    def test_login_required(self):
        res = self.client.get(DISH_TYPE_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDishTypeTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "password12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_dish_type(self):
        DishType.objects.create(name="test1")
        DishType.objects.create(name="test2")

        res = self.client.get(DISH_TYPE_URL)
        dish_types = DishType.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["dish_type_list"]),
            list(dish_types)
        )
