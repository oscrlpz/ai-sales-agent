import os
from typing import Generator
from agents import KavakGeneralBot

API_LLM_MODEL = os.getenv("API_LLM_MODEL")


def reply_message(message: str) -> str:
    """
    Function to reply to a message using the KavakGeneralBot.
    """
    sales_bot = KavakGeneralBot(model=API_LLM_MODEL)
    response = sales_bot.send_message(message)
    return response


def reply_message_stream(message: str) -> Generator[str, None, None]:
    """
    Function to reply to a message using the KavakGeneralBot.
    """
    sales_bot = KavakGeneralBot(model=API_LLM_MODEL)
    sales_bot.send_message(message, stream=True)
    for chunk in sales_bot.yield_response(200):
        yield chunk
    