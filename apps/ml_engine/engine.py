import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict
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

    def recommend(self, user_prefs, house_list, interactions=None):
        """
        Calculates a hybrid recommendation score based on:
        1. Content-based similarity (features)
        2. Collaborative filtering (similar users' behavior)
        """
        if not house_list or not user_prefs:
            return []

        # 1. Content-Based Scoring (Refined similarity logic)
        df_houses = pd.DataFrame(house_list)
        df_user = self._create_mock_user_df(user_prefs)

        def engineer(df):
            df['price_per_sqft'] = df['price'] / df['sqft']
            df['bed_bath_ratio'] = df['bedrooms'] / (df['bathrooms'] + 0.1)
            if 'popularity_score' not in df.columns:
                df['popularity_score'] = 0
            return df

        df_houses = engineer(df_houses)
        df_user = engineer(df_user)

        features = [
            'location', 'house_type', 'price', 'bedrooms', 'bathrooms', 'sqft', 
            'year_built', 'has_parking', 'has_pool', 'price_per_sqft', 
            'bed_bath_ratio', 'popularity_score', 'pref_min_price', 
            'pref_max_price', 'pref_min_bedrooms'
        ]

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

        combined = pd.concat([df_user[features], df_houses[features]])
        preprocessor.fit(combined)
        
        user_transformed = preprocessor.transform(df_user[features])
        houses_transformed = preprocessor.transform(df_houses[features])

        content_similarities = cosine_similarity(user_transformed, houses_transformed)[0]

        # 2. Collaborative Filtering Scoring (User-Behavior Similarity)
        collab_scores = np.zeros(len(df_houses))
        if interactions:
            try:
                df_inter = pd.DataFrame(interactions)
                # Pivot to create User-Item matrix
                user_house_matrix = df_inter.pivot_table(index='user_id', columns='house_id', values='interaction_type', aggfunc='count').fillna(0)
                
                target_user_id = user_prefs.get('user_id', 1)
                if target_user_id in user_house_matrix.index:
                    user_similarities = cosine_similarity(user_house_matrix)
                    user_idx = user_house_matrix.index.get_loc(target_user_id)
                    
                    # Find similar users
                    similar_users_idx = user_similarities[user_idx].argsort()[::-1][1:6] # Top 5
                    
                    # Average interest of similar users in all houses
                    similar_users_interactions = user_house_matrix.iloc[similar_users_idx].mean(axis=0)
                    
                    # Apply these scores to the current house list
                    for i, house in df_houses.iterrows():
                        collab_scores[i] = similar_users_interactions.get(house['id'], 0)
            except Exception as e:
                print(f"Collab Filtering Error: {e}")

        # 3. Hybridize (Weighted sum: 60% content, 40% collaborative)
        # Normalize collab scores to [0, 1] for fair weighting
        if collab_scores.max() > 0:
            collab_scores = collab_scores / collab_scores.max()

        final_scores = (0.6 * content_similarities) + (0.4 * collab_scores)

        # 4. Rank and return
        df_houses['score'] = final_scores
        df_houses['content_match'] = content_similarities
        df_houses['behavior_match'] = collab_scores
        
        top_results = df_houses.sort_values(by='score', ascending=False).head(15)
        
        # 5. Add Explanations
        results = top_results.to_dict(orient='records')
        for res in results:
            res['explanation'] = self._generate_explanation(user_prefs, res)
            
        return results

    def _generate_explanation(self, prefs: Dict, house: Dict) -> Dict:
        """
        Generates a human-readable explanation for why a house was recommended.
        """
        top_matches = []
        
        # Price Check
        if "min_price" in prefs and "max_price" in prefs:
            if prefs["min_price"] <= house["price"] <= prefs["max_price"]:
                top_matches.append("Fits your budget")
        
        # Bedrooms Check
        if "min_bedrooms" in prefs:
            if house["bedrooms"] >= prefs["min_bedrooms"]:
                top_matches.append(f"{house['bedrooms']}+ Bedrooms")
                
        # Location Check
        if "preferred_location" in prefs:
            if prefs["preferred_location"].lower() in house["location"].lower():
                top_matches.append("Preferred location")

        reason = "This home fits your search criteria"
        if top_matches:
            reason = f"Matches your interest in {', '.join(top_matches[:2])}"

        return {
            "reason": reason,
            "top_matches": top_matches
        }

recommender = Recommender()
