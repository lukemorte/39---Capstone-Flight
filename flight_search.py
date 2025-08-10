import requests
from dotenv import load_dotenv
import os


load_dotenv()


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    def __init__(self):
        self.api_key = os.getenv("AMADEUS_API_KEY")
        self.api_secret = os.getenv("AMADEUS_API_SECRET")
        self._token = self._get_new_token()

    def get_destination_code(self, city_name):
        print(f"Using this token to get destination {self._token}")
        headers = {"Authorization": f"Bearer {self._token}"}
        IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations"
        query_params = {
            "keyword": city_name,
            "subType": "CITY",
        }

        response = requests.get(url=IATA_ENDPOINT, headers=headers, params=query_params)
        try:
            code = response.json()["data"][0]["iataCode"]
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}.")
            return "Not found"
        return code

    def _get_new_token(self):
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        body = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret,
        }
        response = requests.post(url="https://test.api.amadeus.com/v1/security/oauth2/token", headers=header, data=body)
        print(f"Your token is {response.json()['access_token']}")
        print(f"Your token expires in {response.json()['expires_in']} seconds")
        return response.json()['access_token']
