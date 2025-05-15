import logging
import os
import time

from dotenv import load_dotenv
from fastapi import APIRouter, BackgroundTasks, Form
from fastapi.responses import Response
from twilio.rest import Client as TwilioClient
from twilio.twiml.messaging_response import MessagingResponse

# from ..services.chatbot import reply_message_stream
from ..services.sales_agent import run_chat

logger = logging.getLogger(__name__)
webhook_router = APIRouter(prefix="/webhook", tags=["whatsapp"])


def send_message(body: str, to_num: str) -> str:
    """
    Function to reply to a message using the KavakGeneralBot.
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
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
    twilio_client.messages.create(
        body=reply, from_="whatsapp:+14155238886", to=f"{to_num}"
    )


@webhook_router.post("/reply")
async def reply_whatsapp(
    Body: str = Form(...),
    From: str = Form(...),
    test: bool = False,
    background_tasks: BackgroundTasks = None,
):
    logger.info(f"Message from {From}: {Body}")
    resp = MessagingResponse()
    msg = resp.message()
    # msg.body(f"You said: {Body}. Thanks for your message!")
    if Body.lower() != "join there-fish":
        # msg.body(reply)
        # return Response(content=str(reply), media_type="application/xml")
        if test:
            reply = run_chat(user_input=Body, session_id=From)
            return Response(content=str(reply), media_type="application/xml")
        else:
            background_tasks.add_task(send_message, Body, From)
