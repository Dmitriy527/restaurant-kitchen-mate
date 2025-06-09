from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen_core.models import Dish, DishType


DISH_LIST_URL = reverse("kitchen_core:dishes-list")


class PublicDishViewTest(TestCase):
    def test_dish_login_required(self):
        response = self.client.get(DISH_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDishViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user0",
            first_name="FirstName",
            last_name="LastName",
            password="my_secret_password",
            years_of_experience=5,
        )
        self.client.force_login(self.user)

        self.dish_type1 = DishType.objects.create(name="Test Dish Type 1")
        self.dish_type2 = DishType.objects.create(name="Test Dish Type 2")
        self.dish_type3 = DishType.objects.create(name="Test Dish Type 3")

        self.dish1 = Dish.objects.create(
            name="Test Dish 1",
            description="Dish 1 description",
            price=10,
            dish_type=self.dish_type1,
        )
        self.dish1.cooks.set([self.user])

        self.dish2 = Dish.objects.create(
            name="Test Dish 2",
            description="Dish 2 description",
            price=20,
            dish_type=self.dish_type2,
        )
        self.dish2.cooks.set([self.user])

    def test_retrieve_dish_list(self):
        response = self.client.get(DISH_LIST_URL)
        self.assertEqual(response.status_code, 200)
        dishes = Dish.objects.all()
        self.assertEqual(list(response.context["dish_list"]), list(dishes))
        self.assertTemplateUsed(response, "kitchen/dish_list.html")

    def test_dish_search_field_in_context(self):
        response = self.client.get(DISH_LIST_URL)
        self.assertIn("search_field", response.context)
        self.assertEqual(response.context["search_field"].initial["name_dish"], None)

    def test_dish_search_by_name(self):
        response = self.client.get(DISH_LIST_URL, {"name_dish": "Test Dish 1"})
        self.assertContains(response, "Test Dish 1")
        self.assertNotContains(response, "Test Dish 2")

    def test_dish_detail_view(self):
        url = reverse("kitchen_core:dish-detail", args=[self.dish1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dish_detail.html")
        self.assertEqual(response.context["dish"], self.dish1)

    def test_dish_create_view_get(self):
        response = self.client.get(reverse("kitchen_core:dish-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dish_form.html")

    def test_dish_create_view_post(self):
        valid_data = {
            "name": "Test Dish 3",
            "description": "Dish 3 description",
            "price": 30,
            "dish_type": self.dish_type3.id,
            "cooks": [self.user.id]
        }
        response = self.client.post(reverse("kitchen_core:dish-create"), data=valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Dish.objects.filter(name="Test Dish 3").exists())

    def test_dish_update_view_get(self):
        response = self.client.get(reverse("kitchen_core:dish-update", args=[self.dish1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dish_form.html")

    def test_dish_update_view_post(self):
        response = self.client.post(
            reverse("kitchen_core:dish-update", args=[self.dish1.pk]),
            {"name": "Test Dish 4",
             "description": "Dish 1 description",
             "price": 10,
             "dish_type": self.dish_type1.id,
             "cooks": [self.user.id]
             }
        )
        self.assertEqual(response.status_code, 302)
        self.dish1.refresh_from_db()
        self.assertEqual(self.dish1.name, "Test Dish 4")

    def test_dish_delete_view_get(self):
        response = self.client.get(reverse("kitchen_core:dish-delete", args=[self.dish1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dish_confirm_delete.html")

    def test_dish_delete_view_post(self):
        response = self.client.post(reverse("kitchen_core:dish-delete", args=[self.dish1.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Dish.objects.filter(pk=self.dish1.pk).exists())
