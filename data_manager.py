import requests
import os
from dotenv import load_dotenv

load_dotenv()

SHEET_API_URL = "https://api.sheety.co/5f2e71425f09ba9a917864d228b52ef4/flightDeals/prices"


class DataManager:
    # This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self.http_header = {
            "Authorization": os.getenv("SHEETY_KEY"),
            "Content-type": "application/json",
        }
        self.destination_data = {}

    def get_destination_data(self):        
        response = requests.get(url=SHEET_API_URL, headers=self.http_header)
        response.raise_for_status()

        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{SHEET_API_URL}/{city['id']}", headers=self.http_header, json=new_data)
            print(response.text)