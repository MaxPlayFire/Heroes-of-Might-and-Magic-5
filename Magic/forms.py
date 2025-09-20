from django import forms
from .models import HeroAbility, Hero


class HeroAbilityForm(forms.ModelForm):
    class Meta:
        model = HeroAbility
        fields = ["ability",]
        widgets = {
            "ability": forms.Select(attrs={"class": "form-select"}),
        }


class HeroForm(forms.ModelForm):
    class Meta:
        model = Hero
        fields = ["name", "faction", "specialization", "abilities"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "faction": forms.TextInput(attrs={"class": "form-control"}),
            "specialization": forms.Select(attrs={"class": "form-select"}),
            "abilities": forms.SelectMultiple(attrs={"class": "form-select"}),
        }
