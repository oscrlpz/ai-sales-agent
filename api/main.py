import logging

from fastapi import FastAPI

from .routes.webhook import webhook_router

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.include_router(webhook_router)
