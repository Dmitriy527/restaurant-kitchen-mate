from django.urls import path

from kitchen_core.views import (
    index,
    DishTypesList,

)

urlpatterns = [
    path("", index, name="index"),
    path("dish-types/", DishTypesList.as_view(), name="dish_types_list"),
]

app_name = "kitchen_core"