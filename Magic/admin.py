from django.contrib import admin
from .models import Skill, Ability, Specialization, Hero, HeroSkill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("title", "short_content")
    search_fields = ("title",)

    def short_content(self, obj):
        return (obj.content[:50] + "...") if len(obj.content) > 50 else obj.content
    short_content.short_description = "Content"


class AbilityAdmin(admin.ModelAdmin):
    list_display = ("title", "short_content")
    search_fields = ("title",)
    filter_horizontal = ("prerequisites",)

    def short_content(self, obj):
        return (obj.content[:50] + "...") if len(obj.content) > 50 else obj.content
    short_content.short_description = "Content"


admin.site.register(Ability, AbilityAdmin)


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ("name", "short_description")
    search_fields = ("name",)

    def short_description(self, obj):
        return (obj.description[:50] + "...") if len(obj.description) > 50 else obj.description
    short_description.short_description = "Description"


class HeroSkillInline(admin.TabularInline):
    model = HeroSkill
    extra = 1


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ("name", "faction", "specialization")
    list_filter = ("faction", "specialization")
    search_fields = ("name", "faction")
    inlines = [HeroSkillInline]
    filter_horizontal = ("abilities",)


@admin.register(HeroSkill)
class HeroSkillAdmin(admin.ModelAdmin):
    list_display = ("hero", "skill", "level")
    list_filter = ("level", "hero", "skill")
    search_fields = ("hero__name", "skill__title")
