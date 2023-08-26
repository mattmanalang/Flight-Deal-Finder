from twilio.rest import Client
import os
import smtplib

TWILIO_SID = os.environ['ENV_TWILIO_SID']
TWILIO_AUTH_TOKEN = os.environ['ENV_TWILIO_TOKEN']
TWILIO_VIRTUAL_NUMBER = os.environ['ENV_TWILIO_VIRTUAL_NUM']
TWILIO_VERIFIED_NUMBER = os.environ['ENV_TWILIO_VERIF_NUM']
MY_EMAIL = os.getenv("My_Email")
MY_PASSWORD = os.getenv("My_App_Password")


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message):
        """Send SMS alerts to users via Twilio's API"""
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_VERIFIED_NUMBER,
        )
        print(message.sid)

    def send_emails(self, names, emails, message):
        """Send email alerts to users via SMTP"""
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            for name, email in zip(names, emails):
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=email,
                    msg=f"Subject:New Flight Deal Found!\n\n"
                        f"{name}!\n"
                        f"{message}".encode('utf-8')
                )
