from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from kitchen_core.models import Dish, DishType


class SwitchAssignToFoodAndIndexTest(TestCase):
    def setUp(self):
        # Створюємо тестового кухаря
        self.cook = get_user_model().objects.create_user(
            username="test_cook",
            password="testpass123",
            years_of_experience=5
        )

        # Створюємо тестові страви
        self.dish_type = DishType.objects.create(name="Test Type")
        self.dish1 = Dish.objects.create(
            name="Test Dish 1",
            description="Test Description",
            price=10,
            dish_type=self.dish_type
        )
        self.dish1.cooks.add(self.cook)
        self.dish2 = Dish.objects.create(
            name="Test Dish 2",
            description="Test Description",
            price=20,
            dish_type=self.dish_type
        )
        self.url = reverse("kitchen_core:index")

    def test_index_view_without_login(self):
        """Тест доступу без авторизації"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_index_view_with_login(self):
        """Тест доступу з авторизацією"""
        self.client.force_login(self.cook)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/index.html")

    def test_index_view_context_data(self):
        """Тест контекстних даних"""
        self.client.force_login(self.cook)
        response = self.client.get(self.url)

        # Перевіряємо кількість об'єктів
        self.assertEqual(response.context["num_cooks"], 1)
        self.assertEqual(response.context["num_dish_types"], 1)
        self.assertEqual(response.context["num_dishes"], 2)

        # Перевіряємо лічильник відвідувань
        self.assertEqual(response.context["num_visits"], 1)

        # Оновлюємо сторінку для перевірки лічильника
        response = self.client.get(self.url)
        self.assertEqual(response.context["num_visits"], 2)

    def test_index_view_with_multiple_objects(self):
        """Тест з кількома об'єктами"""
        # Додаємо ще одного кухаря
        get_user_model().objects.create_user(
            username="test_cook2",
            password="testpass123",
            years_of_experience=3
        )

        # Додаємо ще один тип страви
        DishType.objects.create(name="Test Type 2")

        # Додаємо ще одну страву
        Dish.objects.create(
            name="Test Dish 2",
            description="Test Description",
            price=20,
            dish_type=self.dish_type
        )

        self.client.force_login(self.cook)
        response = self.client.get(self.url)

        self.assertEqual(response.context["num_cooks"], 2)
        self.assertEqual(response.context["num_dish_types"], 2)
        self.assertEqual(response.context["num_dishes"], 3)

    def test_add_dish_to_cook(self):
        """Тест додавання страви до кухаря"""
        self.client.force_login(self.cook)
        # Спочатку переконуємось, що страва не належить кухарю
        self.cook.dishes.remove(self.dish1)

        url = reverse("kitchen_core:switch-assign-cook", args=[self.dish1.pk])
        response = self.client.get(url)

        # Перевіряємо редирект
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("kitchen_core:dish-detail", kwargs={"pk": self.dish1.pk}))

        # Перевіряємо, що страва додалась
        self.assertTrue(self.dish1 in self.cook.dishes.all())

    def test_remove_dish_from_cook(self):
        """Тест видалення страви з кухаря"""
        self.client.force_login(self.cook)
        # Спочатку додаємо страву
        self.cook.dishes.add(self.dish1)

        url = reverse("kitchen_core:switch-assign-cook", args=[self.dish1.pk])
        response = self.client.get(url)

        # Перевіряємо, що страва видалилась
        self.assertFalse(self.dish1 in self.cook.dishes.all())
