from django.urls import path

from kitchen_core.views import index

urlpatterns = [
    path("", index, name="index"),
]

app_name = "kitchen_core"