from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "Magic"

urlpatterns = [
    path("", views.hero_list, name="home"),
    path("skills/", views.all_skills, name="all_skills"),
    path("skills/<int:pk>/", views.skill_detail, name="skill_detail"),

    path("heroes/", views.hero_list, name="hero_list"),
    path("heroes/<int:pk>/", views.hero_detail, name="hero_detail"),
    path("heroes/create/", views.hero_create, name="hero_create"),
    
    path("accounts/login", auth_views.LoginView.as_view(template_name="Magic/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/register/", views.register, name="register"),
]
