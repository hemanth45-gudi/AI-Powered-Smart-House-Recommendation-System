from locust import HttpUser, task, between
import json

class SmartHouseUser(HttpUser):
    wait_time = between(1, 4)
    
    @task(3)
    def view_homes(self):
        """Simulate discovering random homes endpoint"""
        self.client.get("/houses", catch_response=True)
            
    @task(2)
    def get_recommendations(self):
        """Simulate ad-hoc generic ML requests"""
        payload = {
            "min_price": 50000,
            "max_price": 400000,
            "min_bedrooms": 3
        }
        # In this demo setup, this points to backend, 
        # but one would point directly to /recommend 
        # if proxying directly against ML port.
        headers = {'Content-Type': 'application/json'}
        self.client.post("/recommend", data=json.dumps(payload), headers=headers)
