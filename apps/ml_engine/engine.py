import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .utils import preprocess_data

class Recommender:
    def __init__(self):
        self.scaler_price_range = (0, 10000000) # Example range for normalization
        
    def recommend(self, user_prefs, listings):
        """
        Ranks listings based on cosine similarity to user preferences.
        """
        if not listings or not user_prefs:
            return []
            
        df = pd.DataFrame(listings)
        
        # Create a 'user vector' from preferences
        # We'll use a simplified vector: [price, bedrooms, sqft]
        # For 'price', we'll use the average of min and max if available
        pref_price = (user_prefs.get('min_price', 0) + user_prefs.get('max_price', 500000)) / 2
        pref_bedrooms = user_prefs.get('min_bedrooms', 2)
        pref_sqft = 1500 # Default sqft preference
        
        user_vector = np.array([[pref_price, pref_bedrooms, pref_sqft]])
        
        # Listing vectors
        listing_vectors = df[['price', 'bedrooms', 'sqft']].values
        
        # Calculate similarity
        similarities = cosine_similarity(user_vector, listing_vectors)[0]
        
        # Add scores and sort
        df['score'] = similarities
        top_recommendations = df.sort_values(by='score', ascending=False).head(10)
        
        return top_recommendations.to_dict(orient='records')

recommender = Recommender()
