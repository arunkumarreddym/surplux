from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Food, Profile


class SignupForm(UserCreationForm):

    ROLE_CHOICES = (
        ("donor", "Donor"),
        ("buyer", "Buyer"),
        ("ngo", "NGO"),
    )

    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "role"]

    def save(self, commit=True):

        user = super().save(commit)

        Profile.objects.create(
            user=user,
            role=self.cleaned_data["role"]
        )

        return user

class FoodForm(forms.ModelForm):

    class Meta:
        model = Food
        fields = "__all__"
        
from django import forms
from .models import Grocery

class GroceryForm(forms.ModelForm):
    class Meta:
        model = Grocery
        fields = ['image']