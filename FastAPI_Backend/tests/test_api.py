import sys
import os

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


FAKE_IMAGE_URL = "http://test-image.example.com/img.jpg"


@pytest.fixture
def client(mock_dataset, monkeypatch):
    import main
    monkeypatch.setattr(main, "dataset", mock_dataset)
    monkeypatch.setattr(main, "get_image_url", lambda _: FAKE_IMAGE_URL)
    from fastapi.testclient import TestClient
    with TestClient(main.app) as client:
        yield client


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"health_check": "OK"}


def test_predict_returns_results(client):
    payload = {
        "nutrition_input": [200.0, 5.0, 1.0, 30.0, 400.0, 20.0, 2.0, 3.0, 15.0],
        "ingredients": [],
        "params": {"n_neighbors": 3, "return_distance": False},
    }
    response = client.post("/predict/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["output"] is not None
    assert len(data["output"]) == 3
    assert "Name" in data["output"][0]
    assert "Calories" in data["output"][0]
    assert data["output"][0]["image_url"] == FAKE_IMAGE_URL


def test_predict_no_results_with_impossible_ingredient(client):
    payload = {
        "nutrition_input": [200.0, 5.0, 1.0, 30.0, 400.0, 20.0, 2.0, 3.0, 15.0],
        "ingredients": ["unicorn_ingredient_xyz_impossible"],
        "params": {"n_neighbors": 3, "return_distance": False},
    }
    response = client.post("/predict/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"output": None}


def test_generate_meal_plan_returns_results(client):
    payload = {
        "age": 30, "height": 175.0, "weight": 70.0,
        "gender": "Male", "activity": "Little/no exercise",
        "number_of_meals": 3, "weight_loss": "Maintain weight",
    }
    response = client.post("/generate-meal-plan/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "bmi" in data
    assert "meals" in data
    assert len(data["meals"]) == 3
    first_recipe = data["meals"][0]["recipes"][0]
    assert "image_url" in first_recipe
    assert first_recipe["image_url"] == FAKE_IMAGE_URL


def test_predict_invalid_input_shape(client):
    payload = {
        "nutrition_input": [200.0, 5.0],  # only 2 values instead of 9
        "ingredients": [],
        "params": {"n_neighbors": 3, "return_distance": False},
    }
    response = client.post("/predict/", json=payload)
    assert response.status_code == 422
