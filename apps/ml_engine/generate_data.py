import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_synthetic_data(num_houses=100, num_users=50, num_interactions=500):
    # 1. House Features
    locations = ['Downtown', 'Suburbs', 'Uptown', 'Rural', 'Beachside']
    house_types = ['Apartment', 'Villa', 'Condo', 'Townhouse']
    
    houses = []
    for i in range(num_houses):
        houses.append({
            'house_id': i + 1,
            'title': f'House {i+1}',
            'location': random.choice(locations),
            'house_type': random.choice(house_types),
            'price': random.randint(100000, 2000000),
            'bedrooms': random.randint(1, 6),
            'bathrooms': random.randint(1, 4),
            'sqft': random.randint(500, 5000),
            'year_built': random.randint(1950, 2024),
            'has_parking': random.choice([True, False]),
            'has_pool': random.choice([True, False])
        })
    df_houses = pd.DataFrame(houses)
    
    # 2. User Preferences
    users = []
    for i in range(num_users):
        users.append({
            'user_id': i + 1,
            'pref_min_price': random.randint(50000, 500000),
            'pref_max_price': random.randint(600000, 3000000),
            'pref_min_bedrooms': random.randint(1, 3),
            'pref_preferred_location': random.choice(locations)
        })
    df_users = pd.DataFrame(users)
    
    # 3. User Interactions (Click, View, Save)
    interactions = []
    start_date = datetime.now() - timedelta(days=30)
    for i in range(num_interactions):
        interactions.append({
            'user_id': random.randint(1, num_users),
            'house_id': random.randint(1, num_houses),
            'interaction_type': random.choice(['click', 'view', 'save']),
            'timestamp': start_date + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
        })
    df_interactions = pd.DataFrame(interactions)
    
    return df_houses, df_users, df_interactions

if __name__ == "__main__":
    h, u, i = generate_synthetic_data()
    h.to_csv('houses.csv', index=False)
    u.to_csv('users.csv', index=False)
    i.to_csv('interactions.csv', index=False)
    print("Synthetic data generated: houses.csv, users.csv, interactions.csv")
 holdings = {
        'houses': h,
        'users': u,
        'interactions': i
    }
