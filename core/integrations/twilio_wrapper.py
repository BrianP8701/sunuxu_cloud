import os

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse


class TwilioWrapper:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TwilioWrapper, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.client = Client(self.account_sid, self.auth_token)

    async def send_message(self, from_number, to_number, body, media_urls=None):
        message = self.client.messages.create(
            body=body, from_=from_number, to=to_number, media_url=media_urls
        )
        return message.sid

    def create_phone_number(self, area_code="123"):
        incoming_phone_number = self.client.incoming_phone_numbers.create(
            area_code=area_code
        )
        return incoming_phone_number.phone_number

    @staticmethod
    def handle_incoming_messages(request):
        # Extract data from request
        from_number = request.values.get("From")
        to_number = request.values.get("To")
        body = request.values.get("Body")
        media_urls = [
            request.values.get(f"MediaUrl{i}")
            for i in range(0, int(request.values.get("NumMedia", 0)))
        ]

        # Create a response object
        response = MessagingResponse()
        response.message("Thank you for your message!")

        return {
            "from_number": from_number,
            "to_number": to_number,
            "body": body,
            "media_urls": media_urls,
        }, str(response)


# Example usage
if __name__ == "__main__":
    pass
    # from flask import Flask, request
    # import asyncio

    # app = Flask(__name__)
    # twilio_wrapper = TwilioWrapper()

    # @app.route("/send-message", methods=["POST"])
    # async def send_message():
    #     data = request.json
    #     from_number = data["from_number"]
    #     to_number = data["to_number"]
    #     body = data["body"]
    #     media_urls = data.get("media_urls")
    #     message_sid = await twilio_wrapper.send_message(from_number, to_number, body, media_urls)
    #     return {"message_sid": message_sid}, 200

    # @app.route("/create-phone-number", methods=["POST"])
    # def create_phone_number():
    #     area_code = request.json.get("area_code", "123")
    #     phone_number = twilio_wrapper.create_phone_number(area_code)
    #     return {"phone_number": phone_number}, 200

    # @app.route("/incoming-message", methods=["POST"])
    # def incoming_message():
    #     message_data, response = TwilioWrapper.handle_incoming_messages(request)
    #     # Here you can process the message_data as needed
    #     return response, 200

    # if __name__ == "__main__":
    #     app.run(port=5000)
