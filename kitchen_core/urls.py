from django.urls import path

from kitchen_core.models import DishType
from kitchen_core.views import (
    index,
    DishTypesListView,
    DishTypesCreateView,
    DishTypesUpdateView,
    DishTypesDeleteView,
    DishListView,
    DishCreateView,
    DishDetailView,
    DishUpdateView,
    DishDeleteView,
    switch_assign_to_food,
    CookListView,

)

urlpatterns = [
    path("", index, name="index"),
    path("dish-types/", DishTypesListView.as_view(), name="dish-types-list"),
    path("dish-types/create/", DishTypesCreateView.as_view(), name="dish-types-create"),
    path("dish-types/<int:pk>/update/", DishTypesUpdateView.as_view(), name="dish-types-update"),
    path("dish-types/<int:pk>/delete/", DishTypesDeleteView.as_view(), name="dish-types-delete"),
    path("dishes/", DishListView.as_view(), name="dishes-list"),
    path("dishes/create/", DishCreateView.as_view(), name="dish-create"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("dishes/<int:pk>/update/", DishUpdateView.as_view(), name="dish-update"),
    path("dishes/<int:pk>/delete/", DishDeleteView.as_view(), name="dish-delete"),
    path("dishes/<int:pk>/switch_assign_cook", switch_assign_to_food, name="switch-assign-cook"),
    path("cooks/", CookListView.as_view(), name="cooks-list"),
]

app_name = "kitchen_core"