# we import the Twilio client from the dependency we just installed
from twilio.rest import Client

clientIdHalf = 'ACa34bd8ffed125040'
ClientIdOther = '6642b1801b24da28'
halfAuth = "8f31f5a2178908"
otherAuth = "926794f25fb427bff9"
# the following line needs your Twilio Account SID and Auth Token
messenger = Client(clientIdHalf+ClientIdOther, halfAuth+otherAuth)

# change the "from_" number to your Twilio number and the "to" number
# to the phone number you signed up for Twilio with, or upgrade your
# account to send SMS to any phone number
messenger.messages.create(to="+18658046479", 
                       from_="+12185271160", 
                       body="Hello from Python!")