from django.urls import path

from kitchen_core.views import (
    index,
    DishTypesListView,
    DishTypesCreateView,

)

urlpatterns = [
    path("", index, name="index"),
    path("dish-types/", DishTypesListView.as_view(), name="dish-types-list"),
    path("dish-types/create/", DishTypesCreateView.as_view(), name="dish-types-create"),
]

app_name = "kitchen_core"