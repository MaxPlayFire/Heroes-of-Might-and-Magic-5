from django.db import models


class Skill(models.Model):
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField(blank=True)
    
    

    def __str__(self):
        return f"{self.title} \n {self.content}"


class Ability(models.Model):
    LEVEL_CHOICES = [
        ("basic", "Basic"),
        ("advanced", "Advanced"),
        ("expert", "Expert"),
        ("hero", "Hero")
    ]
    title = models.CharField(max_length=100, unique=True)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True, blank=True)
    
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="basic")
    content = models.TextField()

    # Нове поле: залежності між талантами
    prerequisites = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="unlocks"
    )

    def __str__(self):
        return f"{self.title} \n {self.content}"



class Specialization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Hero(models.Model):
    name = models.CharField(max_length=100, unique=True)
    faction = models.CharField(max_length=100, blank=True)
    skills = models.ManyToManyField(Skill)
    abilities = models.ManyToManyField(Ability, through='HeroAbility', through_fields=('hero', 'ability'), related_name='heroes', null=True , blank=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class HeroAbility(models.Model):
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE, related_name="hero_abilities")
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE, related_name="aility_links", null=True, blank=True)

    class Meta:
        unique_together = ("hero", "ability")

    def __str__(self):
        return f"{self.hero.name} - {self.ability.title}"

