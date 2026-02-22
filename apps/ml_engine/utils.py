import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import requests
import os

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://backend_api:8000")

def fetch_house_listings():
    """Fetches all house listings from the backend API."""
    try:
        response = requests.get(f"{BACKEND_API_URL}/houses/")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching house listings: {e}")
        return []

def fetch_user_preferences(user_id: int):
    """Fetches user preferences from the backend API."""
    try:
        response = requests.get(f"{BACKEND_API_URL}/users/{user_id}/preferences")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching user preferences: {e}")
        return None

def preprocess_data(listings):
    """Converts listings to a DataFrame and scales numerical features."""
    if not listings:
        return pd.DataFrame()
    
    df = pd.DataFrame(listings)
    
    # Scale numerical features
    scaler = StandardScaler()
    numerical_cols = ['price', 'bedrooms', 'bathrooms', 'sqft']
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    
    return df
