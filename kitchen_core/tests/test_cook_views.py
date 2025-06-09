from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen_core.models import Cook

COOK_LIST_URL = reverse('kitchen_core:cooks-list')


class PublicUserViewTest(TestCase):
    def test_cook_login_required(self):
        response = self.client.get(COOK_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateUserCookViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            first_name="John",
            last_name="Doe",
            password="password123",
            years_of_experience=3,
        )
        self.client.force_login(self.user)

        self.cook1 = Cook.objects.create(
            username="cook1",
            first_name="Alice",
            last_name="Smith",
            years_of_experience=5,
        )
        self.cook2 = Cook.objects.create(
            username="cook2",
            first_name="Bob",
            last_name="Johnson",
            years_of_experience=2,
        )

    def test_retrieve_cook_list(self):
        response = self.client.get(COOK_LIST_URL)
        self.assertEqual(response.status_code, 200)
        cook_list = Cook.objects.all()
        self.assertEqual(list(response.context["cook_list"]), list(cook_list))
        self.assertTemplateUsed(response, "kitchen/cook_list.html")

    def test_cook_search_field_in_context(self):
        response = self.client.get(COOK_LIST_URL)
        self.assertIn("search_field", response.context)
        self.assertEqual(response.context["search_field"].initial["name_cook"], None)

    def test_cook_search_by_username(self):
        response = self.client.get(COOK_LIST_URL, {"name_cook": "cook1"})
        self.assertContains(response, "cook1")
        self.assertNotContains(response, "cook2")

    def test_cook_detail_view(self):
        url = reverse("kitchen_core:cooks-detail", args=[self.cook1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/cook_detail.html")
        self.assertEqual(response.context["cook"], self.cook1)

    def test_cook_create_view_get(self):
        response = self.client.get(reverse("kitchen_core:cooks-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/cook_form.html")

    def test_cook_create_view_post(self):
        valid_data = {
            "username": "user1",
            "first_name": "Dic",
            "last_name": "Douse",
            "years_of_experience": 6,
            "password1": "1Qazcde3",
            "password2": "1Qazcde3",
        }
        response = self.client.post(reverse("kitchen_core:cooks-create"), data=valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Cook.objects.filter(username="user1").exists())
        self.assertTrue(Cook.objects.filter(first_name="Dic").exists())

    def test_cook_update_view_get(self):
        response = self.client.get(reverse("kitchen_core:cooks-update", args=[self.cook1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/cook_form.html")

    def test_cook_update_view_post(self):
        response = self.client.post(
            reverse("kitchen_core:cooks-update", args=[self.cook1.pk]),
            {"years_of_experience": 7},
        )
        self.assertEqual(response.status_code, 302)
        self.cook1.refresh_from_db()
        self.assertEqual(self.cook1.years_of_experience, 7)

    def test_cook_delete_view_get(self):
        response = self.client.get(reverse("kitchen_core:cooks-delete", args=[self.cook1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/cook_confirm_delete.html")

    def test_cook_delete_view_post(self):
        response = self.client.post(reverse("kitchen_core:cooks-delete", args=[self.cook1.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Cook.objects.filter(pk=self.cook1.pk).exists())
