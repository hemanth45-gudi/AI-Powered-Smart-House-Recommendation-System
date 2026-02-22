import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import os
from .utils import fetch_house_listings, fetch_user_preferences, fetch_user_interactions

class HouseDataPipeline:
    def __init__(self):
        # We only use features that actually exist in our DB
        self.numeric_features = ['price', 'bedrooms', 'bathrooms', 'sqft', 'price_per_sqft', 'bed_bath_ratio', 'popularity_score']
        self.categorical_features = ['location']
        
    def process(self):
        """Run the full pipeline using live data from the backend."""
        print("Fetching live data from backend...")
        houses_list = fetch_house_listings()
        interactions_list = fetch_user_interactions()
        
        if not houses_list:
            raise ValueError("No houses found in the database. Please seed the data first.")
        
        houses = pd.DataFrame(houses_list)
        interactions = pd.DataFrame(interactions_list) if interactions_list else pd.DataFrame(columns=['user_id', 'house_id', 'event_type'])
        
        print(f"Processing {len(houses)} houses and {len(interactions)} interactions...")
        
        # 1. Feature Engineering: House Features
        houses['price_per_sqft'] = houses['price'] / (houses['sqft'].replace(0, 1))
        houses['bed_bath_ratio'] = houses['bedrooms'] / (houses['bathrooms'].replace(0, 0.1) + 0.1)
        
        # 2. Feature Engineering: Popularity Score
        if not interactions.empty and 'house_id' in interactions.columns:
            pop_scores = interactions.groupby('house_id').size().reset_index(name='popularity_score')
            houses = houses.merge(pop_scores, left_on='id', right_on='house_id', how='left').fillna({'popularity_score': 0})
        else:
            houses['popularity_score'] = 0
            
        # 3. Create Training Dataset (Matches)
        # For training a classifier, we need some 'positive' interactions (saves)
        # If no interactions, we can't really 'train' a personalized model correctly, 
        # but we can create a dummy label for the pipeline to function.
        if not interactions.empty and 'user_id' in interactions.columns:
            # Join interactions with houses
            data = interactions.merge(houses, left_on='house_id', right_on='id')
            # Label 1 for 'save', 0 for others
            data['label'] = (data['event_type'] == 'save').astype(int)
        else:
            # Fallback: create dummy data if no interactions exist yet
            data = houses.copy()
            data['label'] = 0
            
        # 4. Final Feature Selection
        # Note: In a real system we'd also include user profile features here.
        # For this version, we focus on house features being liked by users.
        X = data[self.numeric_features + self.categorical_features]
        y = data['label']
        
        # 5. Preprocessing
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), self.numeric_features),
                ('cat', OneHotEncoder(handle_unknown='ignore'), self.categorical_features)
            ])
        
        print("Splitting and transforming data...")
        if len(X) < 2:
            # Not enough data to split, just return the same for both
            X_transformed = preprocessor.fit_transform(X)
            return X_transformed, X_transformed, y, y
            
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        X_train_transformed = preprocessor.fit_transform(X_train)
        X_test_transformed = preprocessor.transform(X_test)
        
        return X_train_transformed, X_test_transformed, y_train, y_test

if __name__ == "__main__":
    pipeline = HouseDataPipeline()
    try:
        X_train, X_test, y_train, y_test = pipeline.process()
        print(f"Pipeline complete. Training set shape: {X_train.shape}")
    except Exception as e:
        print(f"Error in pipeline: {e}")
