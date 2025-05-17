import os
import time

from twilio.rest import Client as TwilioClient

from .sales_agent import run_chat


def send_message(body: str, to_num: str) -> str:
    """
    Function to reply to a message using the KavakGeneralBot.
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_number = os.getenv("TWILIO_NUMBER", "whatsapp:+14155238886")
    twilio_client = TwilioClient(account_sid, auth_token)
    # for reply in reply_message_stream(body):
    #     logger.info(f"Sending message to {to_num}: {reply}")
    #     time.sleep(1)
    #     twilio_client.messages.create(
    #         body=reply,
    #         from_="whatsapp:+14155238886",
    #         to=f"{to_num}"
    #     )
    reply = run_chat(user_input=body, session_id=to_num)
    twilio_client.messages.create(body=reply, from_=twilio_number, to=f"{to_num}")
