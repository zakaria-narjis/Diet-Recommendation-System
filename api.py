from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Union
from datetime import timedelta
from data import FoodData
import keys
from model import recommend

username = keys.username
password= keys.password
CONNECTION_URL = "mongodb+srv://"+username+":"+password+"@fooddata.9pkittm.mongodb.net/test"
data=FoodData(CONNECTION_URL)
dataset=data.test()

app = FastAPI()


# class Person(BaseModel):
#     age: int
#     Gender: bool
#     height: float
#     weight: float
#     bmi:
#     def calculate_bmi(self,):
#         bmi=

class PredictionIn(BaseModel):
    nutrition_input:list[float]
    ingredients:list[str]=[]
    params:dict={'return_distance':False}

class Recipe(BaseModel):
    name:str
    CookTime:timedelta=timedelta(0)
    PrepTime:timedelta=timedelta(0)
    TotalTime:timedelta=timedelta(0)
    RecipeIngredientParts:list[str]
    Calories:float
    FatContent:float
    SaturatedFatContent:float
    CholesterolContent:float
    SodiumContent:float
    CarbohydrateContent:float
    FiberContent:float
    SugarContent:float
    ProteinContent:float
    RecipeInstructions:list[str]

class PredictionOut(BaseModel):
    output:List[Recipe]=[]


@app.get("/")
def home():
    return {"health_check": "OK"}


@app.post("/predict/",response_model=PredictionOut)
def update_item(prediction_input:PredictionIn):
    return recommend(dataset,PredictionIn.nutrition_input,PredictionIn.ingredients,PredictionIn.params)
