from twilio.rest import Client
from django.conf import settings

def send_sms(to, message):
     
    client = Client(account_sid, auth_token)

    client.messages.create(
        to=to,
        from_='+12564084041',  
        body=message
    )
        

