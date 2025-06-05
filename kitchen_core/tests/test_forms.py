from django.contrib.auth import get_user_model
from django.test import TestCase

from kitchen_core.forms import (
    DishForm,
    CookCreationForm,
    CookUpdateForm,
    DishTypeSearchForm,
    DishSearchForm,
    CookSearchForm)
from kitchen_core.models import DishType


class DishFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
        )
        self.dish_type = DishType.objects.create(
            name="Dish Type",
        )

    def test_dish_form_valid_data(self):
        dish_data = {
            "name": "dish_name",
            "description": "dish_description",
            "price": 20,
            "dish_type": self.dish_type,
            "cooks": (self.user, )
        }
        form = DishForm(data=dish_data)
        self.assertTrue(form.is_valid())


    def test_dish_form_with_missing_field_name(self):
        dish_data = {
            "description": "dish_description",
            "price": 20,
            "dish_type": self.dish_type,
            "cooks": (self.user,)
        }
        form = DishForm(data=dish_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_dish_form_cooks_field_queryset(self):
        form = DishForm()
        self.assertIn(self.user, form.fields['cooks'].queryset)

    def test_dish_form_cooks_widget(self):
        form = DishForm()
        widget = form.fields['cooks'].widget.__class__.__name__
        self.assertEqual(widget, "CheckboxSelectMultiple")


class CooksFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "new_user1",
            "password1": "user_password1",
            "password2": "user_password1",
            "first_name": "first_name1",
            "last_name": "last_name1",
            "years_of_experience": 20,
        }
        self.cook = get_user_model().objects.create(
            username="test_cook",
            first_name="Test",
            last_name="Cook",
            years_of_experience=5
        )
    def test_cook_creation_form_with_license_first_last_name_is_valid(self):
        form = CookCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(
            form.cleaned_data["username"] == self.form_data["username"]
        )
        self.assertTrue(
            form.cleaned_data["first_name"] == self.form_data["first_name"]
        )
        self.assertTrue(
            form.cleaned_data["last_name"] == self.form_data["last_name"]
        )
        self.assertTrue(
            form.cleaned_data["years_of_experience"] == self.form_data["years_of_experience"]
        )
        self.form_data["years_of_experience"] = -1
        form = CookCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_field_experience_in_cook_update_form_with_valid_data(self):
        form = CookUpdateForm(
            instance = self.cook,
            data = {"years_of_experience": 10}
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["years_of_experience"], 10)

    def test_field_experience_in_cook_update_form_with_invalid_data(self):
        form = CookUpdateForm(
            instance = self.cook,
            data = {"years_of_experience": -1}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)


class DishTypeSearchFormTest(TestCase):
    def test_search_form_valid_with_query(self):
        form_data = {"name_dish_type": "search term"}
        form = DishTypeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_search_form_valid_with_empty_query(self):
        form = DishTypeSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_search_form_label_is_empty(self):
        form = DishTypeSearchForm()
        self.assertEqual(form["name_dish_type"].label, "")

    def test_search_form_has_placeholder(self):
        form = DishTypeSearchForm()
        placeholder = form["name_dish_type"].field.widget.attrs.get("placeholder", "")
        self.assertEqual(placeholder, "search by name")


class DishSearchFormTest(TestCase):
    def test_search_form_valid_with_query(self):
        form_data = {"name_dish": "search term"}
        form = DishSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_search_form_valid_with_empty_query(self):
        form = DishSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_search_form_label_is_empty(self):
        form = DishSearchForm()
        self.assertEqual(form["name_dish"].label, "")

    def test_search_form_has_placeholder(self):
        form = DishSearchForm()
        placeholder = form["name_dish"].field.widget.attrs.get("placeholder", "")
        self.assertEqual(placeholder, "search by name")


class CookSearchFormTest(TestCase):
    def test_search_form_valid_with_query(self):
        form_data = {"name_cook": "search term"}
        form = CookSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_search_form_valid_with_empty_query(self):
        form = CookSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_search_form_label_is_empty(self):
        form = CookSearchForm()
        self.assertEqual(form["name_cook"].label, "")

    def test_search_form_has_placeholder(self):
        form = CookSearchForm()
        placeholder = form["name_cook"].field.widget.attrs.get("placeholder", "")
        self.assertEqual(placeholder, "search by username")