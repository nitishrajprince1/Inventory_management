from django.urls import path
from inventory_management import views

app_name = "inventory_management"

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.signup, name="register"),
    path("login/", views.signin, name="login"),
    path(
        "inventory_list/<int:pending>", views.inventory_list_view, name="inventory_list"
    ),
    path("inventory_list/", views.inventory_list_view, name="inventory_list"),
    path(
        "update_inventory_list/",
        views.update_inventory_list,
        name="update_inventory_list",
    ),
    path(
        "inventory_detail/<int:product_id>",
        views.inventory_detailed_view,
        name="inventory_detail",
    ),
    path(
        "update_inventory/<int:product_id>",
        views.update_inventory,
        name="update_inventory",
    ),
    path("add_inventory/", views.add_inventory, name="add_inventory"),
    path(
        "delete_inventory/<int:product_id>",
        views.delete_inventory,
        name="delete_inventory",
    ),
    path("logout/", views.auth_logout, name="logout"),
]
