from twilio.rest import Client

def send_sms(to, message):
    account_sid = 'AC61fe16df9db3d696ac414d37cb06c66d'  # Replace with your Account SID
    auth_token = '8bb4fb0866d247697be7a54a830e2b69'    # Replace with your Auth Token
    client = Client(account_sid, auth_token)

    client.messages.create(
        to=to,
        from_='+12564084041',  # Replace with your Twilio phone number
        body=message
    )
