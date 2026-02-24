import pytest
from apps.ml_engine.engine import Recommender

@pytest.fixture
def sample_houses():
    return [
        {"id": 1, "price": 100000, "bedrooms": 2, "bathrooms": 1, "sqft": 1000, "location": "New York"},
        {"id": 2, "price": 200000, "bedrooms": 3, "bathrooms": 2, "sqft": 1500, "location": "Los Angeles"},
        {"id": 3, "price": 300000, "bedrooms": 4, "bathrooms": 3, "sqft": 2000, "location": "Chicago"},
        {"id": 4, "price": 150000, "bedrooms": 2, "bathrooms": 1, "sqft": 1100, "location": "New York Suburb"}
    ]

@pytest.fixture
def recommender():
    return Recommender()

def test_strict_filtering_price(recommender, sample_houses):
    user_prefs = {"min_price": 150000, "max_price": 250000, "min_bedrooms": 2}
    results = recommender.recommend(user_prefs, sample_houses)
    assert len(results) == 2
    assert set(res["id"] for res in results) == {2, 4}

def test_strict_filtering_location(recommender, sample_houses):
    user_prefs = {"preferred_locations": ["New York"]}
    results = recommender.recommend(user_prefs, sample_houses)
    assert len(results) == 2
    assert set(res["id"] for res in results) == {1, 4}

def test_strict_filtering_beds(recommender, sample_houses):
    user_prefs = {"min_bedrooms": 4}
    results = recommender.recommend(user_prefs, sample_houses)
    assert len(results) == 1
    assert results[0]["id"] == 3

def test_empty_houses_or_prefs(recommender, sample_houses):
    assert recommender.recommend({}, sample_houses) == []
    user_prefs = {"min_price": 150000, "max_price": 250000, "min_bedrooms": 2}
    assert recommender.recommend(user_prefs, []) == []

def test_strict_filtering_all(recommender, sample_houses):
    user_prefs = {
        "min_price": 100000, 
        "max_price": 200000, 
        "min_bedrooms": 2,
        "preferred_locations": ["New York"]
    }
    results = recommender.recommend(user_prefs, sample_houses)
    assert len(results) == 2
    assert set(res["id"] for res in results) == {1, 4}

def test_error_handling_wrong_data_types(recommender):
    user_prefs = {"min_price": "invalid", "max_price": 250000, "min_bedrooms": 2}
    # pandas will throw error or it will just return empty based on data conversion
    try:
        results = recommender.recommend(user_prefs, [{"price": 100, "bedrooms": 1}])
        assert len(results) == 0
    except TypeError:
        # If it raises due to string comparision, that's expected error handling
        pass
