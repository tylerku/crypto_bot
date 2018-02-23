from twilio.rest import Client

def send_notification(hint, str_index):

    twilio_account_sid = "ACf338d2ae78871a96cabce61d4b90ec7e"
    twilio_auth_token = "4fb434ee98ad2c52330af8711d64096a"
    twilio_client = Client(twilio_account_sid, twilio_auth_token)
    message_body = hint + ' BTC on neuryx \nStrength Index: ' + str(str_index)
    print(message_body)
    message = twilio_client.messages.create(
            body=message_body,
        	to="7244064427",
			from_="+15012381073 ")

