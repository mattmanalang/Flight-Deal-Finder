import requests
import os

SHEETY_ENDPOINT = os.environ["ENV_SHEETY_ENDPOINT"]
SHEETY_HEADERS = {
    "Authorization": os.environ["ENV_SHEETY_TOKEN"]
}
SHEETY_USER = os.getenv("Sheety_User_Endpoint")


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}
        self.customer_data = {}

    def get_destination_data(self):
        """Gets the current data stored in the Google Spreadsheet"""
        response = requests.get(url=SHEETY_ENDPOINT, headers=SHEETY_HEADERS)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        """Updates the destination codes in the Google Spreadsheet"""
        for city in self.destination_data:
            updated_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{SHEETY_ENDPOINT}/{city['id']}", json=updated_data, headers=SHEETY_HEADERS)
            print(response.text)

    def get_customer_emails(self):
        """Gets the list of customers and their emails from the Google Spreadsheet"""
        customers_endpoint = f"{SHEETY_USER}/flightDeals/users"
        response = requests.get(url=customers_endpoint, headers=SHEETY_HEADERS)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data
