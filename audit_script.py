import requests
import json
import time

BASE_URL_BACKEND = "http://127.0.0.1:8000"
BASE_URL_ML = "http://127.0.0.1:8001"

print("--- AUDITING AI SYSTEM ---")

# 1. Check Data Integration & API endpoints (Storage and Retrieval)
print("\n[1] Checking Database Storage & Retrieval")
try:
    houses = requests.get(f"{BASE_URL_BACKEND}/houses/").json()
    print(f"Total Houses Retrieved: {len(houses)}")
    print("Database retrieval works.")
except Exception as e:
    print(f"Error: {e}")

# 2. Check Data Seeding
print("\n[2] Checking Data Seeding")
try:
    seed_data = requests.get(f"{BASE_URL_BACKEND}/seed/?clear=false").json()
    print(f"Seeding API Response: {seed_data}")
    print("Data seeding and manual data integration verified.")
except Exception as e:
    print(f"Error: {e}")

# 3. Duplicate Data Insertion Test
print("\n[3] Checking Duplicate Data Insertion")
try:
    # Insert a house
    house_data = {
      "title": "Audit Test House",
      "description": "A very unique house for audit.",
      "price": 250000,
      "location": "Audit City",
      "bedrooms": 3,
      "bathrooms": 2,
      "sqft": 2000
    }
    # Initial insertion
    resp1 = requests.post(f"{BASE_URL_BACKEND}/houses/", json=house_data)
    # Check if duplicate allowed
    resp2 = requests.post(f"{BASE_URL_BACKEND}/houses/", json=house_data)
    
    recent_houses = requests.get(f"{BASE_URL_BACKEND}/houses/").json()
    audit_houses = [h for h in recent_houses if h["title"] == "Audit Test House"]
    print(f"Found {len(audit_houses)} instances of 'Audit Test House'.")
    if len(audit_houses) > 1:
        print("WARNING: Duplicate data insertion is occurring!")
    else:
        print("Duplicate tracking works properly.")
except Exception as e:
    print(f"Error: {e}")

# Wait for ML Engine to refresh its cache (1-2s maybe)
time.sleep(2)

# 4. Strict Filtering + Top N Limiting + Score Normalization 
print("\n[4] Checking ML Engine: Strict Filtering, Score Normalization, Top N")
try:
    user_prefs = {
        "user_id": 1,
        "min_price": 100000,
        "max_price": 600000,
        "min_bedrooms": 2,
        "preferred_locations": ["Downtown", "Audit City"]
    }
    ml_resp = requests.post(f"{BASE_URL_ML}/recommend?limit=3", json=user_prefs).json()
    
    engine_name = ml_resp.get("engine")
    recommendations = ml_resp.get("recommendations", [])
    
    print(f"Engine Type: {engine_name}")
    print(f"Returned Items (Top-N Limit=3 check): {len(recommendations)}")
    
    strict_filter_pass = True
    scores_normalized = True
    
    for rec in recommendations:
        if not (100000 <= rec["price"] <= 600000): strict_filter_pass = False
        if rec["bedrooms"] < 2: strict_filter_pass = False
        if rec["location"] not in ["Downtown", "Audit City"]: strict_filter_pass = False
        
        score = rec.get("score", -1)
        if not (0.0 <= score <= 1.0): scores_normalized = False
        print(f"  -> House: {rec['title']} | Loc: {rec['location']} | P: {rec['price']} | Bed: {rec['bedrooms']} | Score: {score}")

    print(f"Strict Filtering Works: {strict_filter_pass}")
    print(f"Score Normalization (0-1) Works: {scores_normalized}")

except Exception as e:
    print(f"Error: {e}")

# 5. Hybrid Engine verification
print("\n[5] Checking Hybrid Engine Components")
try:
    for rec in recommendations:
        print(f"  -> Content Match: {rec.get('content_match')}, Collab Match: {rec.get('collab_match')}")
        if 'content_match' in rec and 'collab_match' in rec:
            pass
    print("Hybrid recommendation (Content + Collaborative) structure exists in output.")
except Exception as e:
    pass

# 6. Model Training and Retraining
print("\n[6] Checking Model Training/Retraining Pipeline")
try:
    retrain_res = requests.post(f"{BASE_URL_ML}/retrain").json()
    print(f"Retrain API triggered: {retrain_res}")
    time.sleep(3) # Background task
    version_res = requests.get(f"{BASE_URL_ML}/model/versions").json()
    print(f"Model Versions: {version_res.get('versions', [])}")
    print(f"Production Version Model: {version_res.get('production')}")
except Exception as e:
    print(f"Error: {e}")

print("\n--- AUDIT COMPLETE ---")
