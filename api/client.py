# api/client.py
import requests
from core.config import BASE_URL, API_KEY

class BSDAPIClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = {
            "Authorization": API_KEY,
            "Accept": "application/json"
        }

    def get_greek_teams(self):
        """
        Τραβάει τη λίστα με τις ομάδες από την Ελλάδα (GR) 
        από το endpoint του API.
        """
        endpoint = f"{self.base_url}/teams/"
        params = {
            "country_code": "GR",
            "in_competition": "true"
        }
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Σφάλμα API: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Αποτυχία σύνδεσης με τον server: {e}")
            return None

    def get_live_events(self):
        """
        Τραβάει τα live γεγονότα/αγώνες για παρακολούθηση ροής.
        """
        endpoint = f"{self.base_url}/events/live/"
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Σφάλμα Live API: {response.status_code}")
                return None
        except Exception as e:
            print(f"Σφάλμα σύνδεσης στα live events: {e}")
            return None