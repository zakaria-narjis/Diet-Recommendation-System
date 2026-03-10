import pandas as pd
import pytest

from model import extract_quoted_strings


# Columns match the real dataset schema.
# model.py uses iloc[:,6:15] for nutritional features (Calories → ProteinContent).
COLUMNS = [
    "RecipeId",
    "Name",
    "CookTime",
    "PrepTime",
    "TotalTime",
    "RecipeIngredientParts",
    "Calories",
    "FatContent",
    "SaturatedFatContent",
    "CholesterolContent",
    "SodiumContent",
    "CarbohydrateContent",
    "FiberContent",
    "SugarContent",
    "ProteinContent",
    "RecipeInstructions",
]


def _make_recipe(i: int) -> dict:
    return {
        "RecipeId": i,
        "Name": f"Recipe {i}",
        "CookTime": "PT30M",
        "PrepTime": "PT15M",
        "TotalTime": "PT45M",
        "RecipeIngredientParts": f'c("chicken", "salt", "pepper", "ingredient_{i}")',
        "Calories": 200.0 + i * 10,
        "FatContent": 5.0 + i,
        "SaturatedFatContent": 1.0 + i * 0.1,
        "CholesterolContent": 30.0 + i,
        "SodiumContent": 400.0 + i * 5,
        "CarbohydrateContent": 20.0 + i,
        "FiberContent": 2.0 + i * 0.2,
        "SugarContent": 3.0 + i * 0.3,
        "ProteinContent": 15.0 + i,
        "RecipeInstructions": f'c("Step 1 for recipe {i}.", "Step 2 for recipe {i}.")',
    }


@pytest.fixture
def mock_dataset() -> pd.DataFrame:
    df = pd.DataFrame([_make_recipe(i) for i in range(10)], columns=COLUMNS)
    df["_ingredients_parsed"] = df["RecipeIngredientParts"].apply(
        lambda x: frozenset(extract_quoted_strings(x))
    )
    return df
