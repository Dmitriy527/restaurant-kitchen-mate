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
    CookCreateView,
    CookDetailView,
    CookUpdateView,
    CookDeleteView,

)

urlpatterns = [
    path("", index, name="index"),
    path("dish-types-list/", DishTypesListView.as_view(), name="dish-types-list"),
    path("dish-types/create/", DishTypesCreateView.as_view(), name="dish-types-create"),
    path("dish-types/<int:pk>/update/", DishTypesUpdateView.as_view(), name="dish-types-update"),
    path("dish-types/<int:pk>/delete/", DishTypesDeleteView.as_view(), name="dish-types-delete"),
    path("dishes-list/", DishListView.as_view(), name="dishes-list"),
    path("dishes/create/", DishCreateView.as_view(), name="dish-create"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("dishes/<int:pk>/update/", DishUpdateView.as_view(), name="dish-update"),
    path("dishes/<int:pk>/delete/", DishDeleteView.as_view(), name="dish-delete"),
    path("dishes/<int:pk>/switch_assign_cook/", switch_assign_to_food, name="switch-assign-cook"),
    path("cooks-list/", CookListView.as_view(), name="cooks-list"),
    path("cooks/create/", CookCreateView.as_view(), name="cooks-create"),
    path("cooks/<int:pk>/", CookDetailView.as_view(), name="cooks-detail"),
    path("cooks/<int:pk>/update/", CookUpdateView.as_view(), name="cooks-update"),
    path("cooks/<int:pk>/delete/", CookDeleteView.as_view(), name="cooks-delete")
]

app_name = "kitchen_core"