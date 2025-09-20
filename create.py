# populate.py
import django
import os

# Встановлюємо змінну середовища для Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "App.settings")
django.setup()

from Magic.models import Skill, Ability, Specialization, Hero, HeroAbility

def run():
    # Створюємо навички
    attack = Skill.objects.create(title="Attack", content="Підвищує шкоду ближнього бою.")
    defense = Skill.objects.create(title="Defense", content="Зменшує отримані ушкодження.")
    sorcery = Skill.objects.create(title="Sorcery", content="Прискорює відновлення мани.")

    # Створюємо здібності
    archery = Ability.objects.create(title="Archery", content="Збільшує шкоду стрільців.")
    magic_resistance = Ability.objects.create(title="Magic Resistance", content="Зменшує дію ворожої магії.")
    magic_resistance.prerequisites.add(archery)

    # Створюємо спеціалізацію
    bow_mastery = Specialization.objects.create(name="Bow Mastery", description="Герой отримує бонус до шкоди лучників.")

    # Створюємо героя
    hero = Hero.objects.create(name="Alaric", faction="Sylvan", specialization=bow_mastery)

    # Прив’язуємо навички до героя
    HeroAbility.objects.create(hero=hero, skill=attack, level="basic")
    HeroAbility.objects.create(hero=hero, skill=defense, level="advanced")
    HeroAbility.objects.create(hero=hero, skill=sorcery, level="expert")

    # Прив’язуємо здібності
    hero.abilities.add(archery, magic_resistance)

    print("База успішно заповнена!")

if __name__ == "__main__":
    run()
