import logging

from fastapi import APIRouter, BackgroundTasks, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

from ..services.sales_agent import run_chat
from ..services.whatsapp_service import send_message

logger = logging.getLogger(__name__)
webhook_router = APIRouter(prefix="/webhook", tags=["whatsapp"])


@webhook_router.post("/reply")
async def reply_whatsapp(
    Body: str = Form(...),
    From: str = Form(...),
    test: bool = False,
    background_tasks: BackgroundTasks = None,
):
    """Function to reply to a WhatsApp message.

    Receives the message from the whatsapp webhook and sends a reply using the Twilio API as a background task.
    """
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
