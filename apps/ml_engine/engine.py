import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .data_pipeline import HouseDataPipeline

class Recommender:
    def __init__(self):
        self.pipeline = HouseDataPipeline()
        
    def _create_mock_user_df(self, user_prefs):
        """Creates a single-row DataFrame representing the user's 'ideal' house."""
        return pd.DataFrame([{
            'location': user_prefs.get('preferred_location', 'Suburbs'),
            'house_type': 'Apartment', # Default assumption
            'price': (user_prefs.get('min_price', 0) + user_prefs.get('max_price', 500000)) / 2,
            'bedrooms': user_prefs.get('min_bedrooms', 2),
            'bathrooms': 2, # Default
            'sqft': 1500, # Default
            'year_built': 2010, # Default
            'has_parking': True,
            'has_pool': False,
            'price_per_sqft': 0, # Placeholder, will be calculated in pipeline
            'bed_bath_ratio': 1.0, # Placeholder
            'popularity_score': 0, # Placeholder
            'pref_min_price': user_prefs.get('min_price', 0),
            'pref_max_price': user_prefs.get('max_price', 500000),
            'pref_min_bedrooms': user_prefs.get('min_bedrooms', 2)
        }])

    def recommend(self, user_prefs, house_list):
        """
        Calculates cosine similarity between user preferences and house listings
        using the standardized data pipeline for feature encoding and scaling.
        """
        if not house_list or not user_prefs:
            return []

        # 1. Prepare DataFrames
        df_houses = pd.DataFrame(house_list)
        df_user = self._create_mock_user_df(user_prefs)

        # 2. Run feature engineering (to add price_per_sqft etc)
        # We simulate the pipeline's feature engineering step
        def engineer(df):
            df['price_per_sqft'] = df['price'] / df['sqft']
            df['bed_bath_ratio'] = df['bedrooms'] / (df['bathrooms'] + 0.1)
            # Ensure columns exist locally
            if 'popularity_score' not in df.columns:
                df['popularity_score'] = 0
            return df

        df_houses = engineer(df_houses)
        df_user = engineer(df_user)

        # 3. Define the relevant features (matching data_pipeline.py)
        features = [
            'location', 'house_type', 'price', 'bedrooms', 'bathrooms', 'sqft', 
            'year_built', 'has_parking', 'has_pool', 'price_per_sqft', 
            'bed_bath_ratio', 'popularity_score', 'pref_min_price', 
            'pref_max_price', 'pref_min_bedrooms'
        ]

        # 4. Use the pipeline's preprocessor for consistent encoding/scaling
        # Note: In a production env, the preprocessor would be fitted on 
        # the entire historical dataset during a training job.
        from sklearn.compose import ColumnTransformer
        from sklearn.preprocessing import StandardScaler, OneHotEncoder

        numeric_features = ['price', 'bedrooms', 'bathrooms', 'sqft', 'year_built', 
                            'price_per_sqft', 'bed_bath_ratio', 'popularity_score', 
                            'pref_min_price', 'pref_max_price', 'pref_min_bedrooms']
        categorical_features = ['location', 'house_type', 'has_parking', 'has_pool']
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numeric_features),
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
            ])

        # Combine user and house data to fit the encoder properly (avoiding unknown cat errors)
        combined = pd.concat([df_user[features], df_houses[features]])
        preprocessor.fit(combined)
        
        # Transform both
        user_transformed = preprocessor.transform(df_user[features])
        houses_transformed = preprocessor.transform(df_houses[features])

        # 5. Calculate Cosine Similarity
        # user_transformed is (1, N), houses_transformed is (M, N)
        similarities = cosine_similarity(user_transformed, houses_transformed)[0]

        # 6. Rank and return
        df_houses['score'] = similarities
        top_results = df_houses.sort_values(by='score', ascending=False).head(15)
        
        return top_results.to_dict(orient='records')

recommender = Recommender()
