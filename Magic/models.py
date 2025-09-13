from django.db import models


class Skill(models.Model):
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} \n {self.content}"


class Ability(models.Model):
    title = models.CharField(max_length=100, unique=True)
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
    skills = models.ManyToManyField(Skill, through="HeroSkill")
    abilities = models.ManyToManyField(Ability, blank=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class HeroSkill(models.Model):
    """
    Проміжна модель, бо у героя навичка може бути різного рівня (Basic, Advanced, Expert).
    """
    LEVEL_CHOICES = [
        ("basic", "Basic"),
        ("advanced", "Advanced"),
        ("expert", "Expert"),
    ]
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="basic")

    class Meta:
        unique_together = ("hero", "skill")

    def __str__(self):
        return f"{self.hero.name} - {self.skill.name} ({self.level})"

