import os
import re
from contextlib import asynccontextmanager
from typing import Annotated, List, Literal, Optional

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from config import DEFAULT_N_NEIGHBORS, MEALS_CALORIES_PERC, WEIGHT_LOSS_PLANS
from image_finder import get_image_url
from model import output_recommended_recipes, recommend
from nutrition import build_nutrition_vector, calculate_bmi, calculate_bmr, calculate_tdee

# Absolute path so the app works regardless of working directory.
_DATASET_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'Data', 'dataset.csv'
)

dataset: Optional[pd.DataFrame] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global dataset
    if dataset is None:
        # Pre-process ingredient strings into frozensets once at startup.
        # Enables fast set-based filtering in extract_ingredient_filtered_data()
        # instead of scanning every row with a compound regex on each request.
        dataset = pd.read_csv(_DATASET_PATH, compression='gzip')
        dataset['_ingredients_parsed'] = dataset['RecipeIngredientParts'].apply(
            lambda x: frozenset(s.lower() for s in re.findall(r'"([^"]*)"', x))
        )
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost",
        "http://localhost:80",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


# ---------------------------------------------------------------------------
# Shared models
# ---------------------------------------------------------------------------

class Recipe(BaseModel):
    Name: str
    CookTime: str
    PrepTime: str
    TotalTime: str
    RecipeIngredientParts: list[str]
    Calories: float
    FatContent: float
    SaturatedFatContent: float
    CholesterolContent: float
    SodiumContent: float
    CarbohydrateContent: float
    FiberContent: float
    SugarContent: float
    ProteinContent: float
    RecipeInstructions: list[str]
    image_url: Optional[str] = None


# ---------------------------------------------------------------------------
# /predict/ — custom nutrition-based recommendation
# ---------------------------------------------------------------------------

class Params(BaseModel):
    n_neighbors: int = DEFAULT_N_NEIGHBORS
    return_distance: bool = False


class PredictionIn(BaseModel):
    nutrition_input: Annotated[list[float], Field(min_length=9, max_length=9)]
    ingredients: list[str] = []
    params: Optional[Params] = None


class PredictionOut(BaseModel):
    output: Optional[List[Recipe]] = None


# ---------------------------------------------------------------------------
# /generate-meal-plan/ — automatic meal plan from personal data
# ---------------------------------------------------------------------------

class PersonData(BaseModel):
    age: int
    height: float               # cm
    weight: float               # kg
    gender: Literal["Male", "Female"]
    activity: str               # must be a key in ACTIVITY_MULTIPLIERS
    number_of_meals: Literal[3, 4, 5]
    weight_loss: str            # must be a key in WEIGHT_LOSS_PLANS


class MealRecommendation(BaseModel):
    meal_name: str
    recipes: List[Recipe]


class MealPlanOut(BaseModel):
    bmi: float
    bmr: float
    maintain_calories: float    # TDEE (no weight-loss adjustment)
    target_calories: float      # TDEE × weight-loss factor
    meals: List[MealRecommendation]


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/")
def home():
    return {"health_check": "OK"}


@app.post("/predict/", response_model=PredictionOut)
def predict(prediction_input: PredictionIn):
    params = (
        prediction_input.params.model_dump()
        if prediction_input.params
        else {"n_neighbors": DEFAULT_N_NEIGHBORS, "return_distance": False}
    )
    recommendation_dataframe = recommend(
        dataset,
        prediction_input.nutrition_input,
        prediction_input.ingredients,
        params,
    )
    output = output_recommended_recipes(recommendation_dataframe)
    if output:
        for recipe in output:
            recipe['image_url'] = get_image_url(recipe['Name'])
    return {"output": output}


@app.post("/generate-meal-plan/", response_model=MealPlanOut)
def generate_meal_plan(person: PersonData):
    bmi = calculate_bmi(person.weight, person.height)
    bmr = calculate_bmr(person.weight, person.height, person.age, person.gender)
    maintain_calories = calculate_tdee(bmr, person.activity)
    factor = WEIGHT_LOSS_PLANS[person.weight_loss]["factor"]
    target_calories = maintain_calories * factor

    meals = []
    for meal_name, perc in MEALS_CALORIES_PERC[person.number_of_meals].items():
        vector = build_nutrition_vector(target_calories * perc, meal_name)
        recs = recommend(
            dataset, vector, [],
            {"n_neighbors": DEFAULT_N_NEIGHBORS, "return_distance": False},
        )
        recipes = output_recommended_recipes(recs) if recs is not None else []
        for recipe in recipes:
            recipe['image_url'] = get_image_url(recipe['Name'])
        meals.append(MealRecommendation(
            meal_name=meal_name,
            recipes=recipes,
        ))

    return MealPlanOut(
        bmi=bmi,
        bmr=round(bmr, 2),
        maintain_calories=round(maintain_calories),
        target_calories=round(target_calories),
        meals=meals,
    )
