import logging
import 

from fastapi import APIRouter, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

webhook_router = APIRouter(prefix="/webhook", tags=["whatsapp"],
)

def reply_message(message: str) -> str:
    """
    Function to reply to a message using the KavakGeneralBot.
    """
    # Placeholder for the actual bot logic
    # sales_bot = KavakGeneralBot(model=MODEL)
    # response = sales_bot.send_message(message)
    # return response
    return f"You said: {message}. Thanks for your message!"

@webhook_router.post("/reply")
async def reply_whatsapp(Body: str = Form(...), From: str = Form(...)):
    print(f"Message from {From}: {Body}")

    resp = MessagingResponse()
    msg = resp.message()
    reply = reply_message(Body)
    msg.body(reply)

    return Response(content=str(resp), media_type="application/xml")
