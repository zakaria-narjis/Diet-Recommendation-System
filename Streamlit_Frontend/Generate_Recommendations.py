import os

import requests

BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:8080")


class Generator:
    def __init__(
        self,
        nutrition_input: list,
        ingredients: list = [],
        params: dict = {'n_neighbors': 5, 'return_distance': False},
    ):
        self.nutrition_input = nutrition_input
        self.ingredients = ingredients
        self.params = params

    def set_request(self, nutrition_input: list, ingredients: list, params: dict):
        self.nutrition_input = nutrition_input
        self.ingredients = ingredients
        self.params = params

    def generate(self):
        request = {
            'nutrition_input': self.nutrition_input,
            'ingredients': self.ingredients,
            'params': self.params,
        }
        response = requests.post(url=f"{BACKEND_URL}/predict/", json=request)
        return response
