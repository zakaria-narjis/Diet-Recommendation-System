# All application constants — no magic numbers in business logic or UI code.

BMI_THRESHOLDS = {
    "underweight": 18.5,
    "normal": 25.0,
    "overweight": 30.0,
}

# Harris-Benedict / Mifflin-St Jeor activity multipliers for TDEE calculation.
ACTIVITY_MULTIPLIERS = {
    "Little/no exercise": 1.2,
    "Light exercise": 1.375,
    "Moderate exercise (3-5 days/wk)": 1.55,
    "Very active (6-7 days/wk)": 1.725,
    "Extra active (very active & physical job)": 1.9,
}

WEIGHT_LOSS_PLANS = {
    "Maintain weight":     {"factor": 1.0, "weekly_loss": "0 kg/week"},
    "Mild weight loss":    {"factor": 0.9, "weekly_loss": "0.25 kg/week"},
    "Weight loss":         {"factor": 0.8, "weekly_loss": "0.5 kg/week"},
    "Extreme weight loss": {"factor": 0.6, "weekly_loss": "1 kg/week"},
}

# Calorie distribution across meals for 3, 4, or 5 meals per day.
MEALS_CALORIES_PERC = {
    3: {"breakfast": 0.35, "lunch": 0.40, "dinner": 0.25},
    4: {"breakfast": 0.30, "morning snack": 0.05, "lunch": 0.40, "dinner": 0.25},
    5: {
        "breakfast": 0.30,
        "morning snack": 0.05,
        "lunch": 0.40,
        "afternoon snack": 0.05,
        "dinner": 0.20,
    },
}

# Per-meal nutrition target ranges (min, max) used to generate recommendation vectors.
# Values are in grams (fat, carbs, protein, fiber, sugar, sat_fat) or mg (cholesterol, sodium).
# Snack profile is also used as a fallback for "morning snack" and "afternoon snack".
NUTRITION_RANGES = {
    "breakfast": {
        "fat": (10, 30), "sat_fat": (0, 4), "cholesterol": (0, 30),
        "sodium": (0, 400), "carbs": (40, 75), "fiber": (4, 10),
        "sugar": (0, 10), "protein": (30, 100),
    },
    "lunch": {
        "fat": (20, 40), "sat_fat": (0, 4), "cholesterol": (0, 30),
        "sodium": (0, 400), "carbs": (40, 75), "fiber": (4, 20),
        "sugar": (0, 10), "protein": (50, 175),
    },
    "dinner": {
        "fat": (20, 40), "sat_fat": (0, 4), "cholesterol": (0, 30),
        "sodium": (0, 400), "carbs": (40, 75), "fiber": (4, 20),
        "sugar": (0, 10), "protein": (50, 175),
    },
    "snack": {
        "fat": (10, 30), "sat_fat": (0, 4), "cholesterol": (0, 30),
        "sodium": (0, 400), "carbs": (40, 75), "fiber": (4, 10),
        "sugar": (0, 10), "protein": (30, 100),
    },
}

NUTRITION_COLUMNS = [
    "Calories",
    "FatContent",
    "SaturatedFatContent",
    "CholesterolContent",
    "SodiumContent",
    "CarbohydrateContent",
    "FiberContent",
    "SugarContent",
    "ProteinContent",
]

DEFAULT_N_NEIGHBORS = 5

# Consistent image display width (px) across all recipe cards.
IMAGE_DISPLAY_WIDTH = 200
