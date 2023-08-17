from django.contrib import admin
from .models import UserProfile, Inventory


def display_roles(obj):
    return ", ".join(role.name for role in obj.roles.all())


display_roles.short_description = "Roles"


class UserAdmin(admin.ModelAdmin):
    list_display = ("user", display_roles)

    search_fields = ["user"]

    list_filter = ("roles",)


admin.site.register(UserProfile, UserAdmin)


class InventoryAdmin(admin.ModelAdmin):
    list_display = ("product_name", "vendor", "mrp", "status")

    search_fields = ["product_name"]
    list_filter = ("status", "vendor", "batch_date")

    list_per_page = 50
    show_full_result_count = False


admin.site.register(Inventory, InventoryAdmin)
