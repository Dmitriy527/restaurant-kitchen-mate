from django.test import TestCase
from django.urls import reverse

from kitchen_core.models import Cook, Dish, DishType

class ModelTests(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(name="Test dish type")
        self.cook = Cook.objects.create_user(
            first_name="FirstName",
            last_name="LastName",
            username="username",
            password="my_secret_password",
            years_of_experience=5,
        )
        self.dish = Dish.objects.create(
            name="Test dish",
            description="Best test dish",
            price=5,
            dish_type=self.dish_type,
        )
        self.dish.cooks.set([self.cook])

    def test_cook_str(self):
        self.assertEqual(str(self.cook), f"{self.cook.username} {self.cook.first_name} {self.cook.last_name}")

    def test_cook_password_check(self):
        self.assertTrue(self.cook.check_password("my_secret_password"))
        self.assertFalse(self.cook.check_password("wrong_password"))

    def test_cook_get_absolute_url(self):
        expected_url = reverse("kitchen_core:cooks-detail", kwargs={"pk": self.cook.pk})
        self.assertEqual(self.cook.get_absolute_url(), expected_url)

    def test_dish_str(self):
        self.assertEqual(str(self.dish), f"{self.dish.name} (price: {self.dish.price}, dish type:  {self.dish.dish_type})")

    def test_dish_type_str(self):
        self.assertEqual(str(self.dish_type), self.dish.dish_type.name)
