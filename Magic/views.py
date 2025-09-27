from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import HeroAbilityForm, HeroForm
from .models import Skill, Specialization, HeroAbility, Ability, Hero


def all_skills(request):
    """Вивід списку всіх скілів."""
    q = request.GET.get("q", "").strip()
    skills = Skill.objects.all().order_by("title")

    if q:
        skills = skills.filter(title__icontains=q)

    ctx = {"skills": skills, "q": q}
    return render(request, "Magic/skill_list.html", ctx)


def skill_detail(request, pk: int):
    """Деталі одного скіла."""
    skill = get_object_or_404(Skill, pk=pk)
    heroes = Hero.objects.filter(skills=skill)

    ctx = {"skill": skill, "heroes": heroes}
    return render(request, "Magic/skill_detail.html", ctx)


@login_required
def hero_detail(request, pk: int):
    """Деталі героя з можливістю додати скіл."""
    hero = get_object_or_404(Hero.objects.select_related("specialization"), pk=pk)

    if request.method == "POST":
        form = HeroAbilityForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    hero_skill = form.save(commit=False)
                    hero_skill.hero = hero
                    hero_skill.save()
            except (ValidationError, IntegrityError) as e:
                form.add_error(None, getattr(e, "message", str(e)))
            else:
                messages.success(request, "Скіл додано герою!")
                return redirect(reverse("Magic:hero_detail", args=[hero.pk]))
    else:
        form = HeroAbilityForm()

    hero_skills = HeroAbility.objects.filter(hero=hero).select_related("skill")
    ctx = {"hero": hero, "form": form, "hero_skills": hero_skills}
    return render(request, "Magic/hero_detail.html", ctx)


@login_required
def hero_create(request):
    if request.method == "POST":
        form = HeroForm(request.POST)
        if form.is_valid():
            hero = form.save()
            messages.success(request, f"Герой {hero.name} створений!")
            return redirect(reverse("Magic:hero_detail", args=[hero.pk]))
    else:
        form = HeroForm()
    return render(request, "Magic/hero_form.html", {"form": form})


def hero_list(request):
    heroes = Hero.objects.select_related("specialization").prefetch_related("skills", "abilities")
    return render(request, "Magic/hero_list.html", {"heroes": heroes})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Обліковий запис створено.")
            return redirect("Magic:hero_list")
    else:
        form = UserCreationForm()
    return render(request, "Magic/auth/register.html", {"form": form})