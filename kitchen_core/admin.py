from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from kitchen_core.models import DishType, Cook, Dish

admin.site.register(DishType)


@admin.register(Cook)
class CookAdmin(UserAdmin):
    # Додавання поля years_of_experience до головної сторінки кухарів
    list_display = UserAdmin.list_display + ("years_of_experience",)
    # Додавання додаткового поля years_of_experience до сторінки деталей про кухаря
    fieldsets = UserAdmin.fieldsets + (
        (
            ("Additional Information", {"fields": ("years_of_experience",)}),
        )
    )
    # Додавання додаткових полів до сторінки додавання кухаря
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional Information",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "years_of_experience",
                    )
                },
            ),
        )
    )


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("dish_type",)
