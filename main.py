from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import datetime, timedelta

ORIGIN_CITY_IATA = "IAH"

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()


missing_iata_code = False
for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        missing_iata_code = True
if missing_iata_code:
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()


tomorrow = datetime.now() + timedelta(days=1)
six_months_from_now = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_months_from_now
    )

    ################################
    if flight is None:
        print(f"No flights found for {destination['city']}.")
        continue
    ################################

    if flight.price < destination['lowestPrice']:
        users = data_manager.get_customer_emails()
        emails = [row['email'] for row in users]
        names = [row['firstName'] for row in users]

        message = f"Low price alert! Only ${flight.price} to fly from {flight.origin_city}-{flight.origin_airport} " \
                  f"to {flight.destination_city}-{flight.destination_airport}, " \
                  f"on {flight.out_date}."

        if flight.stop_overs > 0:
            message += f"\nFlight has {flight.stop_overs} stop over(s), via {flight.via_city}"

        # print(message)
        notification_manager.send_emails(emails=emails, names=names, message=message)
        # notification_manager.send_sms(message)
