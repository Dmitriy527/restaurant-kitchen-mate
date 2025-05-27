from django.urls import path

from kitchen_core.views import (
    index,
    DishTypesListView,

)

urlpatterns = [
    path("", index, name="index"),
    path("dish-types/", DishTypesListView.as_view(), name="dish_types_list"),
]

app_name = "kitchen_core"