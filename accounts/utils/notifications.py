from twilio.rest import Client
from django.conf import settings

def send_sms(to, message):
    account_sid = settings.ACCOUNT_SID
    auth_token = settings.AUTH_TOKEN   
    client = Client(account_sid, auth_token)

    client.messages.create(
        to=to,
        from_='+12564084041',  # Replace with your Twilio phone number
        body=message
    )
        

