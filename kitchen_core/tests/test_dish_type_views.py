from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen_core.models import DishType


DISH_TYPE_LIST_URL = reverse("kitchen_core:dish-types-list")


class PublicDishTypesViewTest(TestCase):
    def test_dish_types_login_required(self):
        response = self.client.get(DISH_TYPE_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDishTypesViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            first_name="FirstName",
            last_name="LastName",
            password="my_secret_password",
            years_of_experience=5,
        )
        self.client.force_login(self.user)

        self.dish_type1 = DishType.objects.create(name="Test Dish Type 1")
        self.dish_type2 = DishType.objects.create(name="Test Dish Type 2")

    def test_retrieve_dish_type_list(self):
        response = self.client.get(DISH_TYPE_LIST_URL)
        self.assertEqual(response.status_code, 200)
        dish_types = DishType.objects.all()
        self.assertEqual(list(response.context["dish_types_list"]), list(dish_types))
        self.assertTemplateUsed(response, "kitchen/dish_types_list.html")

    def test_dish_type_search_field_in_context(self):
        response = self.client.get(DISH_TYPE_LIST_URL)
        self.assertIn("search_field", response.context)
        self.assertEqual(response.context["search_field"].initial["name_dish_type"], None)

    def test_dish_type_search_by_name(self):
        response = self.client.get(DISH_TYPE_LIST_URL, {"name_dish_type": "Test Dish Type 1"})
        self.assertContains(response, "Test Dish Type 1")
        self.assertNotContains(response, "Test Dish Type 2")

    def test_dish_type_create_view_get(self):
        response = self.client.get(reverse("kitchen_core:dish-types-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dish_type_form.html")

    def test_dish_type_create_view_post(self):
        valid_data = {
            "name": "Test Dish Type 3",
        }
        response = self.client.post(reverse("kitchen_core:dish-types-create"), data=valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(DishType.objects.filter(name="Test Dish Type 3").exists())

    def test_dish_type_update_view_get(self):
        response = self.client.get(reverse("kitchen_core:dish-types-update", args=[self.dish_type1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dish_type_form.html")

    def test_dish_type_update_view_post(self):
        response = self.client.post(
            reverse("kitchen_core:dish-types-update", args=[self.dish_type1.pk]),
            {"name": "Test Dish Type 4"},
        )
        self.assertEqual(response.status_code, 302)
        self.dish_type1.refresh_from_db()
        self.assertEqual(self.dish_type1.name, "Test Dish Type 4")

    def test_dish_type_delete_view_get(self):
        response = self.client.get(reverse("kitchen_core:dish-types-delete", args=[self.dish_type1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dish_type_confirm_delete.html")

    def test_dish_type_delete_view_post(self):
        response = self.client.post(reverse("kitchen_core:dish-types-delete", args=[self.dish_type1.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(DishType.objects.filter(pk=self.dish_type1.pk).exists())

