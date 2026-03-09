from random import randint as rnd

from config import ACTIVITY_MULTIPLIERS, NUTRITION_RANGES


def calculate_bmi(weight: float, height: float) -> float:
    """Body Mass Index: weight(kg) / height(m)²."""
    return round(weight / ((height / 100) ** 2), 2)


def calculate_bmr(weight: float, height: float, age: int, gender: str) -> float:
    """Basal Metabolic Rate using the Mifflin-St Jeor equation."""
    base = 10 * weight + 6.25 * height - 5 * age
    return base + 5 if gender == "Male" else base - 161


def calculate_tdee(bmr: float, activity: str) -> float:
    """Total Daily Energy Expenditure: BMR × activity multiplier."""
    return bmr * ACTIVITY_MULTIPLIERS[activity]


def build_nutrition_vector(meal_calories: float, meal_type: str) -> list[float]:
    """Build a 9-element nutrition input vector for the recommendation model.

    Randomly samples from per-meal nutrition ranges defined in config.
    Meal types not explicitly in NUTRITION_RANGES (e.g. 'morning snack',
    'afternoon snack') fall back to the 'snack' profile.
    """
    key = meal_type if meal_type in NUTRITION_RANGES else "snack"
    r = NUTRITION_RANGES[key]
    return [
        meal_calories,
        rnd(*r["fat"]),
        rnd(*r["sat_fat"]),
        rnd(*r["cholesterol"]),
        rnd(*r["sodium"]),
        rnd(*r["carbs"]),
        rnd(*r["fiber"]),
        rnd(*r["sugar"]),
        rnd(*r["protein"]),
    ]
