import json
import os
import sys
from typing import Optional

sys.path.append("/home/oscar/projects/ai-sales-agent")
import logging

import pandas as pd

from agents.kavak_classifiers import FinancingBoolClassifier, IntentClassifier
from agents.kavak_general import KavakGeneralBot
from agents.utils.chat_history_manager import ChatHistoryManager
from agents.vehicle_normalizer import VehicleNormalizer
from agents.vehicle_recommendation import VehicleRecommender

# logging.basicConfig(level=logging.INFO)

# Parametros de entrada
data = pd.read_csv(
    "/home/oscar/projects/ai-sales-agent/data/csv/sample_caso_ai_engineer.csv"
)
model = "deepseek-v3"
DB_PATH = "/home/oscar/projects/ai-sales-agent/data/db/chat_history.db"

chat_manager = ChatHistoryManager(DB_PATH)

# Los agentes:
intent = IntentClassifier(model=model)
general = KavakGeneralBot(model=model)
normalizer = VehicleNormalizer(model=model)
recommender = VehicleRecommender(model=model, data=data)
financing = FinancingBoolClassifier(model=model)


def run_chat(user_inputs: Optional[list[str]] = None, session_id: Optional[str] = None):
    if session_id is None:
        session_id = os.getenv("TEST_SESSION_ID", "test_session_000")
    session_id = "test_session_000"
    print(session_id)
    print("🤖 Asistente Kavak (escribe 'salir' para terminar)\n")
    state = "start"
    inputs = iter(user_inputs) if user_inputs else None

    # Load chat history from DB
    history = chat_manager.get_history(session_id)
    general.chat_history = history
    for entry in history:
        print(f"{'Tú' if entry['role'] == 'user' else '🤖'}: {entry['content']}")

    while True:
        if inputs:
            try:
                user_input = next(inputs)
                print(f"Tú: {user_input}")
            except StopIteration:
                break
        else:
            user_input = input("Tú: ")

        if user_input.lower() in ["salir", "exit", "quit"]:
            print("👋 Adiós.")
            break

        # Save user message
        chat_manager.save_message(session_id, "user", user_input)

        # Handle the chat logic
        if state == "start":
            intent_type = intent.classify(user_input)["_type"]
            if intent_type == "general":
                response = general.send_message(user_input)
            elif intent_type == "catalog":
                try:
                    norm = normalizer.normalize(user_input)
                    response = recommender.get_recommendations(user_input, norm)[
                        "readable"
                    ]
                    state = "awaiting_financing"
                except Exception as e:
                    response = general.send_message(user_input)
        elif state == "awaiting_financing":
            fin = financing.classify(user_input)["response"]
            response = (
                "¡Perfecto! Aquí tienes opciones de financiamiento."
                if fin
                else "Entiendo, seguimos sin financiamiento."
            )
            state = "start"

        # Save assistant message
        chat_manager.save_message(session_id, "assistant", response)
        print(f"🤖 {response}\n")


if __name__ == "__main__":
    run_chat()
