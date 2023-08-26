import os
import requests
from flight_data import FlightData

kiwi_locations_endpoint = f"{os.environ['ENV_KIWI_ENDPOINT']}/locations/query"
kiwi_search_endpoint = f"{os.environ['ENV_KIWI_ENDPOINT']}/v2/search"
kiwi_header = {
    "apikey": os.environ["ENV_KIWI_KEY"]
}


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        pass

    def get_destination_code(self, city: str):
        """Get the IATA code for the city using the Tequila API"""
        query_params = {
            "term": city,
            "location_types": "city",
        }
        response = requests.get(url=kiwi_locations_endpoint, headers=kiwi_header, params=query_params)
        data = response.json()["locations"]
        code = data[0]["code"]
        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        """Get the flight(s) from the Tequila Search API"""
        kiwi_query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "one_for_city": 1,
            "max_stopovers": 0,
            "max_sector_stopovers": 0,
            "ret_from_diff_airport": 0,
            "ret_to_diff_airport": 0,
            "curr": "USD",
        }

        response = requests.get(
            url=kiwi_search_endpoint,
            headers=kiwi_header,
            params=kiwi_query
        )

        try:
            data = response.json()["data"][0]
        except IndexError:
            # No direct flights, increase max_stopovers to 2
            kiwi_query["max_stopovers"] = 2
            kiwi_query["max_sector_stopovers"] = 1
            response = requests.get(
                url=kiwi_search_endpoint,
                headers=kiwi_header,
                params=kiwi_query
            )
            try:
                data = response.json()["data"][0]
            except IndexError:
                return None
            else:
                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][1]["cityTo"],
                    destination_airport=data["route"][1]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][2]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=data["route"][0]["cityTo"]
                )
                # print(f"{flight_data.destination_city}: ${flight_data.price}")
                return flight_data
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
            # print(f"{flight_data.destination_city}: ${flight_data.price}")
            return flight_data
