import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from inventory_management.forms import *
from inventory_management.models import *

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def index(request):
    logger.info('start')
    return render(request, "index.html")


@login_required()
def auth_logout(request):
    logout(request)
    return render(request, "index.html")


@login_required()
def update_inventory_list(request):
    if request.method == "POST":
        selected_inventory_ids = request.POST.getlist("selected_inventory")
        qs1 = Inventory.objects.filter(
            product_id__in=selected_inventory_ids,
            status__in=["Change Pending", "Pending"],
        )
        if qs1:
            qs1.update(status="Approved")
        qs2 = Inventory.objects.filter(
            product_id__in=selected_inventory_ids, status="Delete Pending"
        )
        if qs2:
            qs2.delete()
    return inventory_list_view(request)


@login_required()
def inventory_list_view(request, pending=None):
    current_user = UserProfile.objects.get(user=request.user)
    roles_qs = current_user.roles.values_list("name", flat=True)
    roles = ", ".join([item for item in roles_qs])
    if pending:
        inventory_list = Inventory.objects.filter(
            status__in=["Change Pending", "Delete Pending", "Pending"]
        )
    else:
        inventory_list = Inventory.objects.all()
    context = {
        "inventory_list": inventory_list,
        "current_user": current_user,
        "roles": roles,
    }
    logger.info('Inventory Listing View')
    return render(request, "inventory_list.html", context)


@login_required()
def inventory_detailed_view(request, product_id):
    user = UserProfile.objects.get(user=request.user)
    inventory = Inventory.objects.get(product_id=product_id)
    context = {"inventory": inventory, "user": user}
    return render(request, "inventory_detail.html", context)


@login_required()
def add_inventory(request):
    if request.method == "POST":
        form = InventoryForm(request.POST)
        if form.is_valid():
            new_inventory = form.save()
            current_user = UserProfile.objects.get(user=request.user)
            if current_user.roles.filter(name="Store Manager"):
                new_inventory.status = "Approved"
            else:
                new_inventory.status = "Pending"
            new_inventory.save()
            return inventory_list_view(request)
    else:
        form = InventoryForm()
    return render(request, "add_inventory.html", {"form": form})


@login_required()
def delete_inventory(request, product_id):
    item = Inventory.objects.filter(product_id=product_id)
    current_user = UserProfile.objects.get(user=request.user)
    if current_user.roles.filter(name="Store Manager"):
        item.delete()
    else:
        item.update(status="Delete Pending")
    return inventory_list_view(request)


@login_required()
def update_inventory(request, product_id):
    inventory = Inventory.objects.get(product_id=product_id)
    if request.method == "POST":
        form = InventoryForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data
            product_name = item.get("product_name")
            vendor = item.get("vendor")
            mrp = item.get("mrp")
            batch_num = item.get("batch_num")
            batch_date = item.get("batch_date")
            quantity = item.get("quantity")
            product_qs = Inventory.objects.filter(product_id=product_id)
            product_qs.update(
                product_name=product_name,
                vendor=vendor,
                mrp=mrp,
                batch_date=batch_date,
                batch_num=batch_num,
                quantity=quantity,
            )
            current_user = UserProfile.objects.get(user=request.user)
            if current_user.roles.filter(name="Store Manager"):
                product_qs.update(status="Approved")
            else:
                product_qs.update(status="Change Pending")
            return inventory_list_view(request)
    current_inventory = InventoryForm(instance=inventory)
    context = {"form": current_inventory}
    return render(request, "update_inventory.html", context)


def signup(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        roles_form = UserRolesForm(request.POST)
        if user_form.is_valid() and roles_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data["username"]
            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.create(user=user)
            roles = roles_form.cleaned_data["roles"]
            user_profile.roles.set(roles)
            return redirect("/login")
    else:
        user_form = UserRegistrationForm()
        roles_form = UserRolesForm()
    return render(
        request, "register.html", {"user_form": user_form, "roles_form": roles_form}
    )


def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            try:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("/inventory_list")
            except User.DoesNotExist:
                return render(request, "login.html")
        else:
            return render(request, "login.html")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})
