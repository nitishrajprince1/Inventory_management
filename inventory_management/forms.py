from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from inventory_management.models import Inventory, UserProfile


class UserRolesForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["roles"]


class UserRegistrationForm(UserCreationForm):
    roles = UserRolesForm()
    username = forms.CharField(max_length=150)

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = [
            "product_id",
            "product_name",
            "vendor",
            "mrp",
            "batch_num",
            "batch_date",
            "quantity",
            "status",
        ]
