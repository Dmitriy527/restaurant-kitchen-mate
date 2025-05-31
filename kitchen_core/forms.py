from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

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


class CookSearchForm(forms.Form):
    name_cook = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "search by username"}
        )
    )


def validate_years_of_experience(year_of_experience):
    if int(year_of_experience) < 0:
        raise ValidationError("years of experience must be greater or equal to zero")

    return year_of_experience


class CookCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "years_of_experience",
        )
    def clean_years_of_experience(self):
        return validate_years_of_experience(self.cleaned_data["years_of_experience"])


class CookUpdateForm(forms.ModelForm):
    class Meta:
        model = Cook
        fields = ("years_of_experience", )

    def clean_years_of_experience(self):
        return validate_years_of_experience(self.cleaned_data["years_of_experience"])


class DishForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = Dish
        fields = "__all__"
