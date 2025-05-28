from django import forms
from django.contrib.auth import get_user_model

from kitchen_core.models import Dish, Cook


class DishTypeSearchForm(forms.Form):
    name_dish_type = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "search by name"}
        )
    )


class DishSearchForm(forms.Form):
    name_dish = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "search by name"}
        )
    )


class DishForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = Dish
        fields = "__all__"
