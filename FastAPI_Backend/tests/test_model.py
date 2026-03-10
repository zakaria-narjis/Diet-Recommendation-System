import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from model import (
    extract_ingredient_filtered_data,
    extract_quoted_strings,
    recommend,
    scaling,
)


def test_extract_quoted_strings():
    s = 'c("chicken", "salt", "pepper")'
    result = extract_quoted_strings(s)
    assert result == ["chicken", "salt", "pepper"]


def test_extract_quoted_strings_empty():
    assert extract_quoted_strings("no quotes here") == []


def test_extract_ingredient_filtered_data(mock_dataset):
    result = extract_ingredient_filtered_data(mock_dataset, ["chicken"])
    assert len(result) == 10  # all recipes contain "chicken"


def test_extract_ingredient_filtered_data_no_match(mock_dataset):
    result = extract_ingredient_filtered_data(mock_dataset, ["unicorn_ingredient_xyz"])
    assert len(result) == 0


def test_scaling_output_shape(mock_dataset):
    prep_data, scaler = scaling(mock_dataset)
    assert prep_data.shape == (10, 9)


def test_recommend_returns_none_when_insufficient_data(mock_dataset):
    # Request more neighbors than available rows → should return None
    result = recommend(mock_dataset, [200, 5, 1, 30, 400, 20, 2, 3, 15], params={"n_neighbors": 50, "return_distance": False})
    assert result is None


def test_recommend_returns_dataframe(mock_dataset):
    nutrition = [200.0, 5.0, 1.0, 30.0, 400.0, 20.0, 2.0, 3.0, 15.0]
    result = recommend(mock_dataset, nutrition, params={"n_neighbors": 3, "return_distance": False})
    assert result is not None
    assert len(result) == 3
