import logging
import time 

from fastapi import APIRouter, Form, BackgroundTasks
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client as TwilioClient

from ..services.chatbot import reply_message_stream


logger = logging.getLogger(__name__)
webhook_router = APIRouter(prefix="/webhook", tags=["whatsapp"])


def send_message(body: str, to_num: str) -> str:
    """
    Function to reply to a message using the KavakGeneralBot.
    """
    from dotenv import load_dotenv
    import os
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_client = TwilioClient(account_sid, auth_token)
    for reply in reply_message_stream(body):
        logger.info(f"Sending message to {to_num}: {reply}")
        # twilio_client.messages.create(
        #     body=reply,
        #     from_="whatsapp:+14155238886",
        #     to=f"{to_num}"
        # )

@webhook_router.post("/reply")
async def reply_whatsapp(
    Body: str = Form(...), 
    From: str = Form(...),
    background_tasks: BackgroundTasks = None
):
    logger.info(f"Message from {From}: {Body}")
    resp = MessagingResponse()
    msg = resp.message()
    # msg.body(f"You said: {Body}. Thanks for your message!")
    if Body.lower() != "join there-fish":
        # reply = reply_message(Body)
        # msg.body(reply)
        # return Response(content=str(reply), media_type="application/xml")
        background_tasks.add_task(send_message, Body, From)
