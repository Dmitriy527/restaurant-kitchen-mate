from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from kitchen_core.models import DishType, Dish


class CookAdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            password="my_secret_password",
        )

        self.client.force_login(self.admin_user)

        self.cook = get_user_model().objects.create_user(
            username='cook',
            first_name='Cook',
            last_name='Kitchen',
            years_of_experience=5,
            password="my_secret_password",
        )

    def test_cook_list_in_admin_page_with_experience(self):
        url = reverse("admin:kitchen_core_cook_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.cook.years_of_experience)

    def test_cook_detail_with_experience(self):
        url = reverse("admin:kitchen_core_cook_change", args=(self.cook.id, ))
        response = self.client.get(url)
        self.assertContains(response, self.cook.years_of_experience)

    def test_cook_add_form_with_custom_fields(self):
        url = reverse("admin:kitchen_core_cook_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.cook.first_name)
        self.assertContains(response, self.cook.last_name)
        self.assertContains(response, self.cook.years_of_experience)

    def test_cook_search_by_first_name_last_name_in_cook_list_on_admin_page(self):
        url = reverse("admin:kitchen_core_cook_changelist")

        response = self.client.get(url, {"q": "Cook"})
        self.assertContains(response, self.cook.first_name)

        response = self.client.get(url, {"q": "Kitchen"})
        self.assertContains(response, self.cook.last_name)


class DishAdminTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            password="my_secret_password",
        )
        self.client.force_login(self.admin_user)

        self.cook = get_user_model().objects.create_user(
            username='cook',
            first_name='Cook',
            last_name='Kitchen',
            years_of_experience=5,
            password="my_secret_password",
        )

        self.dish_type = DishType.objects.create(name='Dish_type')

        self.dish = Dish.objects.create(
            name='Dish',
            description='Dish description',
            price=10,
            dish_type=self.dish_type,
        )
        self.dish.cooks.set([self.cook])

    def test_search_by_name_in_admin_page_on_dish_list(self):
        url = reverse("admin:kitchen_core_dish_changelist")
        response = self.client.get(url, {"q": "Dish"})
        self.assertContains(response, self.dish.name)

    def test_filter_by_dish_type_in_admin_page_on_dish_list(self):
        url = reverse("admin:kitchen_core_dish_changelist")
        response = self.client.get(url, dish_type__id__exact=self.dish_type.id)
        self.assertContains(response, self.dish.name)
