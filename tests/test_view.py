from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from restaurant.models import DishType, Ingredient, Cook, Dish


class PublicDishTypeTests(TestCase):
    def setUp(self):
        self.test = DishType.objects.create(name="testius")

    def test_login_required_dishtype_list(self):
        url = reverse("restaurant:dish-type-list")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_dishtype_create(self):
        url = reverse("restaurant:dish-type-create")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_dishtype_update(self):
        url = reverse("restaurant:dish-type-update", args=[self.test.pk])
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_dishtype_delete(self):
        url = reverse("restaurant:dish-type-delete", args=[self.test.pk])
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)


class PrivateDishTypeTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "password12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_dish_type_list(self):
        url = reverse("restaurant:dish-type-list")
        response = self.client.get(url)
        dish_types = DishType.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["dish_type_list"]),
            list(dish_types)
        )

    def test_create_dish_type(self):
        url = reverse("restaurant:dish-type-create")
        response = self.client.post(url, data={"name": "New DishType"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DishType.objects.count(), 6)
        new_dish_type = DishType.objects.get(name="New DishType")
        self.assertEqual(new_dish_type.name, "New DishType")

    def test_update_dish_type(self):
        new_dishtype = DishType.objects.create(name="Test DishType")
        url = reverse("restaurant:dish-type-update", args=[new_dishtype.pk])
        response = self.client.post(url, data={"name": "Updated DishType"})
        self.assertEqual(response.status_code, 302)
        new_dishtype.refresh_from_db()
        self.assertEqual(new_dishtype.name, "Updated DishType")

    def test_delete_dish_type(self):
        new_dishtype = DishType.objects.create(name="Test DishType")
        url = reverse("restaurant:dish-type-delete", args=[new_dishtype.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DishType.objects.count(), 5)


class PublicIngredientTests(TestCase):
    def setUp(self):
        self.test = Ingredient.objects.create(name="testius")

    def test_login_required_ingredient_list(self):
        url = reverse("restaurant:ingredient-list")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_ingredient_create(self):
        url = reverse("restaurant:ingredient-create")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_ingredient_update(self):
        url = reverse("restaurant:ingredient-update", args=[self.test.pk])
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_ingredient_delete(self):
        url = reverse("restaurant:ingredient-delete", args=[self.test.pk])
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)


class PrivateIngredientTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "password12345"
        )
        self.client.force_login(self.user)
        self.ingredient = Ingredient.objects.create(name="Ingredient")

    def test_create_ingredient(self):
        url = reverse("restaurant:ingredient-create")
        response = self.client.post(url, data={"name": "New Ingredient"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ingredient.objects.count(), 15)
        new_ingredient = Ingredient.objects.get(name="New Ingredient")
        self.assertEqual(new_ingredient.name, "New Ingredient")

    def test_update_ingredient(self):
        url = reverse("restaurant:ingredient-update", args=[self.ingredient.pk])
        response = self.client.post(url, data={"name": "Updated Ingredient"})
        self.assertEqual(response.status_code, 302)
        self.ingredient.refresh_from_db()
        self.assertEqual(self.ingredient.name, "Updated Ingredient")

    def test_delete_ingredient(self):
        url = reverse("restaurant:ingredient-delete", args=[self.ingredient.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ingredient.objects.count(), 13)

    def test_retrieve_ingredient_list(self):
        url = reverse("restaurant:ingredient-list")
        response = self.client.get(url)
        ingredients = Ingredient.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["ingredient_list"]),
            list(ingredients[:5])
        )


class PublicCookTests(TestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            username="kok",
            password="Testius12345"
        )

    def test_login_required_cook_list(self):
        url = reverse("restaurant:cook-list")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_cook_create(self):
        url = reverse("restaurant:cook-create")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_cook_detail(self):
        url = reverse("restaurant:cook-detail", args=[self.test_user.pk])
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateCookTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "password12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_cook_list(self):
        url = reverse("restaurant:cook-list")
        response = self.client.get(url)
        cooks = Cook.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["cook_list"][:3]),
            list(cooks[:3])
        )

    def test_create_cook(self):
        url = reverse("restaurant:cook-create")
        response = self.client.post(url, data={
            "username": "newcook",
            "password1": "Testpassword1234",
            "password2": "Testpassword1234"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Cook.objects.count(),
            8)  # not 7 cause 6 is already in fixture + 165 line (Setup user for tests)
        new_cook = Cook.objects.get(username="newcook")
        self.assertEqual(new_cook.username, "newcook")

    def test_cook_detail(self):
        new_cook = Cook.objects.create(username="TestCook")
        url = reverse("restaurant:cook-detail", args=[new_cook.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["cook"], new_cook)


class PublicDishTests(TestCase):
    def setUp(self):
        self.dishtype = DishType.objects.create(name="test1")
        self.test = Dish.objects.create(
            name="Sample Dish",
            description="Description of Sample Dish",
            price="10.00",
            dish_type=self.dishtype,
        )

    def test_login_required_dish_list(self):
        url = reverse("restaurant:dish-list")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_dish_detail(self):
        url = reverse("restaurant:dish-detail", kwargs={"pk": self.test.pk})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_dish_create(self):
        url = reverse("restaurant:dish-create")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_dish_update(self):
        url = reverse("restaurant:dish-update", args=[self.test.pk])
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_dish_delete(self):
        url = reverse("restaurant:dish-delete", args=[self.test.pk])
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)


class PrivateDishTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.client.force_login(self.user)
        self.dish_type = DishType.objects.create(name="Sample Dish Type")
        self.ingredient1 = Ingredient.objects.create(name="Ingredient 1")
        self.ingredient2 = Ingredient.objects.create(name="Ingredient 2")

    def test_create_dish(self):
        dish_data = {
            "name": "New Dish",
            "description": "Description of the new dish",
            "price": "15.00",
            "dish_type": self.dish_type.id,
            "ingredients": [self.ingredient1.id, self.ingredient2.id],
        }
        url = reverse("restaurant:dish-create")
        response = self.client.post(url, data=dish_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Dish.objects.count(), 3)

    def test_update_dish(self):
        dish = Dish.objects.create(
            name="Sample Dish",
            description="Sample description",
            price="10.00",
            dish_type=self.dish_type,
        )
        updated_dish_data = {
            "name": "Updated Dish",
            "description": "Updated description",
            "price": "12.00",
            "dish_type": self.dish_type.id,
            "ingredients": [self.ingredient1.id],
        }
        url = reverse("restaurant:dish-update", kwargs={"pk": dish.pk})
        response = self.client.post(url, data=updated_dish_data, follow=True)
        self.assertEqual(response.status_code, 200)
        dish.refresh_from_db()
        self.assertEqual(dish.name, "Updated Dish")

    def test_delete_dish(self):
        dish = Dish.objects.create(
            name="Sample Dish",
            description="Sample description",
            price="10.00",
            dish_type=self.dish_type,
        )
        url = reverse("restaurant:dish-delete", kwargs={"pk": dish.pk})
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Dish.objects.count(), 2)

    def test_retrieve_dish_list(self):
        url = reverse("restaurant:dish-list")
        response = self.client.get(url)
        dishes = Dish.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["dish_list"][:3]),
            list(dishes[:3])
        )
