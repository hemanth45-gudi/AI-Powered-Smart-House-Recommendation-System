"""
Recommendation Engine — works directly with the real database schema:
  house_listings: id, title, description, price, location, bedrooms, bathrooms, sqft
"""
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from typing import Dict, List

NUMERIC_FEATURES = ['price', 'bedrooms', 'bathrooms', 'sqft', 'price_per_sqft', 'bed_bath_ratio']


class Recommender:
    def __init__(self):
        self.scaler = StandardScaler()

    def _engineer(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add derived features from raw house data."""
        df = df.copy()
        df['price_per_sqft'] = df['price'] / (df['sqft'].replace(0, 1))
        df['bed_bath_ratio'] = df['bedrooms'] / (df['bathrooms'].replace(0, 0.1) + 0.1)
        return df

    def _user_vector(self, user_prefs: dict) -> pd.DataFrame:
        """Build a representative 'ideal house' row from user preferences."""
        mid_price = (user_prefs.get('min_price', 100000) + user_prefs.get('max_price', 500000)) / 2
        bedrooms  = user_prefs.get('min_bedrooms', 2)
        row = {
            'price':         mid_price,
            'bedrooms':      bedrooms,
            'bathrooms':     2.0,
            'sqft':          1500.0,
            'price_per_sqft': mid_price / 1500.0,
            'bed_bath_ratio': bedrooms / 2.1,
        }
        return pd.DataFrame([row])

    def recommend(self, user_prefs: dict, house_list: List[dict], interactions=None) -> List[dict]:
        """
        Hybrid recommendation:
        - Content-based: cosine similarity on scaled numeric features
        - Collaborative: interaction-count based scoring
        Returns top-15 houses sorted by score descending.
        """
        if not house_list:
            return []
        if not user_prefs:
            return []

        # --- 1. Prepare house DataFrame ---
        df = pd.DataFrame(house_list)
        # Keep only rows with required columns
        required = ['price', 'bedrooms', 'bathrooms', 'sqft']
        for col in required:
            if col not in df.columns:
                df[col] = 0
        df = self._engineer(df)

        # --- 2. Content-based similarity ---
        df_user = self._user_vector(user_prefs)
        combined = pd.concat([df_user[NUMERIC_FEATURES], df[NUMERIC_FEATURES]], ignore_index=True)
        self.scaler.fit(combined)
        user_vec    = self.scaler.transform(df_user[NUMERIC_FEATURES])
        houses_vec  = self.scaler.transform(df[NUMERIC_FEATURES])
        content_sim = cosine_similarity(user_vec, houses_vec)[0]

        # --- 3. Filter: hard constraints ---
        min_price = user_prefs.get('min_price', 0)
        max_price = user_prefs.get('max_price', float('inf'))
        min_beds  = user_prefs.get('min_bedrooms', 0)
        pref_loc  = user_prefs.get('preferred_location', '').lower()

        in_budget = ((df['price'] >= min_price) & (df['price'] <= max_price)).astype(float)
        has_beds  = (df['bedrooms'] >= min_beds).astype(float)
        loc_match = df['location'].str.lower().str.contains(pref_loc, na=False).astype(float) if pref_loc else pd.Series([0.0] * len(df))

        constraint_bonus = 0.1 * in_budget + 0.1 * has_beds + 0.1 * loc_match

        # --- 4. Collaborative filtering ---
        collab_scores = np.zeros(len(df))
        if interactions:
            try:
                df_inter = pd.DataFrame(interactions)
                if 'house_id' in df_inter.columns and 'user_id' in df_inter.columns:
                    pivot = df_inter.pivot_table(
                        index='user_id', columns='house_id',
                        values='event_type', aggfunc='count'
                    ).fillna(0)
                    target_uid = user_prefs.get('user_id', -1)
                    if target_uid in pivot.index:
                        user_sims = cosine_similarity(pivot)
                        uid_idx = pivot.index.get_loc(target_uid)
                        top_idx = user_sims[uid_idx].argsort()[::-1][1:6]
                        avg_inter = pivot.iloc[top_idx].mean(axis=0)
                        for i, row in df.iterrows():
                            collab_scores[i] = avg_inter.get(row.get('id', -1), 0)
            except Exception as e:
                print(f"[Collab warn] {e}")

        if collab_scores.max() > 0:
            collab_scores = collab_scores / collab_scores.max()

        # --- 5. Hybrid score ---
        final_scores = (0.5 * content_sim) + (0.3 * collab_scores) + (0.2 * constraint_bonus.values)

        df['score']          = np.round(final_scores, 4)
        df['content_match']  = np.round(content_sim, 4)
        df['collab_match']   = np.round(collab_scores, 4)

        top = df.sort_values('score', ascending=False).head(15)

        results = top.to_dict(orient='records')
        for res in results:
            res['explanation'] = self._generate_explanation(user_prefs, res)
        return results

    def _generate_explanation(self, prefs: Dict, house: Dict) -> Dict:
        """Human-readable explanation for why a house was recommended."""
        matches = []
        min_p = prefs.get('min_price', 0)
        max_p = prefs.get('max_price', float('inf'))
        if min_p <= house.get('price', 0) <= max_p:
            matches.append("Fits your budget")
        if house.get('bedrooms', 0) >= prefs.get('min_bedrooms', 0):
            matches.append(f"{house.get('bedrooms')}+ Bedrooms")
        pref_loc = prefs.get('preferred_location', '')
        if pref_loc and pref_loc.lower() in house.get('location', '').lower():
            matches.append("Preferred location")
        reason = f"Matches: {', '.join(matches[:2])}" if matches else "Fits your search criteria"
        return {"reason": reason, "top_matches": matches}


recommender = Recommender()
