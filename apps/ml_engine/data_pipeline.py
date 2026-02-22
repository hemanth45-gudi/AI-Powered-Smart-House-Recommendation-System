import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import os

class HouseDataPipeline:
    def __init__(self):
        self.encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        self.scaler = StandardScaler()
        
    def collect_data(self):
        """Mock data collection: Load from local CSVs or generate on the fly."""
        # In a real system, this would fetch from backend_api/database
        from generate_data import generate_synthetic_data
        houses, users, interactions = generate_synthetic_data()
        return houses, users, interactions

    def clean_data(self, df):
        """Perform basic data cleaning."""
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Simple imputation for numeric columns if any were missing (synthetic data is clean but good practice)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        
        return df

    def feature_engineering(self, houses, users, interactions):
        """Create engineered features across all data sources."""
        # 1. House features
        houses['price_per_sqft'] = houses['price'] / houses['sqft']
        houses['bed_bath_ratio'] = houses['bedrooms'] / (houses['bathrooms'] + 0.1)
        
        # 2. Aggregating User Interactions
        interaction_counts = interactions.groupby('house_id').size().reset_index(name='popularity_score')
        houses = houses.merge(interaction_counts, on='house_id', how='left').fillna({'popularity_score': 0})
        
        # 3. Joining with User Preferences (Creating Interaction Pairs)
        # For simplicity, we create a 'match' dataset where we label if a house follows user prefs
        merged_data = interactions.merge(houses, on='house_id').merge(users, on='user_id')
        
        # Target variable: 1 if user saved, 0 otherwise (for binary classification demo)
        merged_data['label'] = (merged_data['interaction_type'] == 'save').astype(int)
        
        return merged_data

    def process(self):
        """Run the full pipeline."""
        print("Starting data collection...")
        houses, users, interactions = self.collect_data()
        
        print("Cleaning data...")
        houses = self.clean_data(houses)
        
        print("Engineering features...")
        data = self.feature_engineering(houses, users, interactions)
        
        # Define features for training
        features = [
            'location', 'house_type', 'price', 'bedrooms', 'bathrooms', 'sqft', 
            'year_built', 'has_parking', 'has_pool', 'price_per_sqft', 
            'bed_bath_ratio', 'popularity_score', 'pref_min_price', 
            'pref_max_price', 'pref_min_bedrooms'
        ]
        
        X = data[features]
        y = data['label']
        
        # Preprocessing: Encoding and Scaling
        numeric_features = ['price', 'bedrooms', 'bathrooms', 'sqft', 'year_built', 
                            'price_per_sqft', 'bed_bath_ratio', 'popularity_score', 
                            'pref_min_price', 'pref_max_price', 'pref_min_bedrooms']
        categorical_features = ['location', 'house_type', 'has_parking', 'has_pool']
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numeric_features),
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
            ])
        
        print("Splitting data and applying transformations...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        X_train_transformed = preprocessor.fit_transform(X_train)
        X_test_transformed = preprocessor.transform(X_test)
        
        print(f"Pipeline complete. Training set size: {X_train_transformed.shape}")
        return X_train_transformed, X_test_transformed, y_train, y_test

if __name__ == "__main__":
    pipeline = HouseDataPipeline()
    X_train, X_test, y_train, y_test = pipeline.process()
    print("Processed Features Sample (First Row):", X_train[0])
