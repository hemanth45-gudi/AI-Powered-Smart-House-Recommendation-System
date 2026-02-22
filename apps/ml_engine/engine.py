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

    def recommend(self, user_prefs: dict, house_list: List[dict], interactions=None, limit: int = 15) -> List[dict]:
        """
        Hybrid recommendation:
        - Content-based: cosine similarity on scaled numeric features
        - Collaborative: interaction-count based scoring
        Returns top-N houses sorted by score descending.
        """
        if not house_list:
            return []
        if not user_prefs:
            return []

        # --- 1. Prepare house DataFrame ---
        df_full = pd.DataFrame(house_list)
        # Keep only rows with required columns
        required = ['price', 'bedrooms', 'bathrooms', 'sqft']
        for col in required:
            if col not in df_full.columns:
                df_full[col] = 0
        df_full = self._engineer(df_full)

        # --- 2. Apply Filters (Strict -> Relaxed) ---
        min_price = user_prefs.get('min_price', 0)
        max_price = user_prefs.get('max_price', float('inf'))
        min_beds  = user_prefs.get('min_bedrooms', 0)
        
        pref_locs = user_prefs.get('preferred_locations')
        if not pref_locs:
            single_loc = user_prefs.get('preferred_location')
            pref_locs = [single_loc] if single_loc else []
        pref_locs_lower = [loc.lower() for loc in pref_locs if loc]

        # A. Strict Filter
        mask = (
            (df_full['price'] >= min_price) & 
            (df_full['price'] <= max_price) & 
            (df_full['bedrooms'] >= min_beds)
        )
        if pref_locs_lower:
            loc_mask = df_full['location'].str.lower().apply(lambda x: any(loc in x for loc in pref_locs_lower))
            mask = mask & loc_mask
        
        df = df_full[mask].reset_index(drop=True)
        message = None

        # B. Fallback: Relaxed Filter (Ignore min_price and location if empty)
        if df.empty:
            message = "Relaxing constraints: Showing best results (Strict criteria too restrictive for current inventory)."
            relaxed_mask = (df_full['price'] <= max_price) & (df_full['bedrooms'] >= min_beds)
            df = df_full[relaxed_mask].reset_index(drop=True)
        
        # C. Fallback: All Houses (If still empty, just find most similar)
        if df.empty:
            message = "Showing global best matches (Current filters have zero available inventory)."
            df = df_full.copy()
        
        if df.empty:
            return []

        # --- 3. Content-based similarity ---
        df_user = self._user_vector(user_prefs)
        combined = pd.concat([df_user[NUMERIC_FEATURES], df[NUMERIC_FEATURES]], ignore_index=True)
        self.scaler.fit(combined)
        user_vec    = self.scaler.transform(df_user[NUMERIC_FEATURES])
        houses_vec  = self.scaler.transform(df[NUMERIC_FEATURES])
        content_sim = cosine_similarity(user_vec, houses_vec)[0]

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
        final_scores = (0.6 * content_sim) + (0.4 * collab_scores)

        df['score']          = np.round(final_scores, 4)
        df['content_match']  = np.round(content_sim, 4)
        df['collab_match']   = np.round(collab_scores, 4)

        top = df.sort_values('score', ascending=False).head(limit)

        results = top.to_dict(orient='records')
        for res in results:
            res['explanation'] = self._generate_explanation(user_prefs, res)
            if message:
                res['fallback_message'] = message
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
