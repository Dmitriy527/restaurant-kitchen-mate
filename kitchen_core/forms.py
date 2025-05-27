from django import forms


class DishTypeSearchForm(forms.Form):
    name_dish_type = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "search by name"}
        )
    )
