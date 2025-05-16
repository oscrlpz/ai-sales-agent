import json
import logging
import os

import pandas as pd

from agents import (
    FinancingBoolClassifier,
    FinancingExplainer,
    FinancingTermClassifier,
    IntentClassifier,
    KavakGeneralBot,
    VehicleNormalizer,
    VehicleRecommender,
)
from agents.utils.chat_history_manager import ChatHistoryManager
from agents.utils.financing_plan import calc_financing

# logging.basicConfig(level=logging.INFO)

# Parametros de entrada
DATA = pd.read_csv(os.getenv("CATALOG_PATH"))
MODEL = os.getenv("API_LLM_MODEL")
DB_PATH = os.getenv("DB_PATH")

chat_manager = ChatHistoryManager(DB_PATH)

# Los agentes:
intent = IntentClassifier(model=MODEL)
general = KavakGeneralBot(model=MODEL)
normalizer = VehicleNormalizer(model=MODEL)
recommender = VehicleRecommender(model=MODEL, data=DATA)
financing = FinancingBoolClassifier(model=MODEL)
tern_classifier = FinancingTermClassifier(model=MODEL)
financing_explainer = FinancingExplainer(model=MODEL)


def run_chat(user_input: str, session_id: str, verbose: bool = True) -> str:
    if verbose:
        print(f"Session ID: {session_id}")

    # Load chat history from DB
    history = chat_manager.get_history(session_id)
    general.chat_history = history
    latest_entry = history[-1] if history else None
    if latest_entry:
        state = latest_entry.get("state", "start")
        car_data = (
            json.loads(latest_entry["car_data"]) if latest_entry["car_data"] else {}
        )

    else:
        state = "start"
        car_data = {}

    # user_input
    if verbose:
        print(f"Tú: {user_input}")

    # Save user message
    chat_manager.save_message(
        session_id=session_id,
        role="user",
        content=user_input,
        state=state,
        car_data=json.dumps(car_data) if car_data else None,
    )

    # Handle the chat logic
    if state == "start":
        intent_type = intent.classify(user_input)["_type"]
        if intent_type == "general":
            response = general.send_message(user_input)
        elif intent_type == "catalog":
            try:
                norm = normalizer.normalize(user_input)
                rec = recommender.get_recommendations(user_input, norm)
                response = rec["readable"]
                car_data = rec["raw"]
                state = "awaiting_financing"
            except Exception as e:
                response = general.send_message(user_input)
    elif state == "awaiting_financing":
        fin = financing.classify(user_input)["response"]

        if fin:
            response = "¡Perfecto! Tenemos una tasa de interés del 10% y plazos de financiamiento de entre 3 y 6 años ¿A cuantos años quieres financiarlo y con cuanto de enganche?"
            state = "awaiting_financing_terms"
        else:
            response = "Entiendo, seguimos sin financiamiento."
            state = "start"

    elif state == "awaiting_financing_terms":
        # try:
        terms = tern_classifier.classify(user_input)
        if terms["wants_financing"]:
            financing_plan = calc_financing(
                total_price=car_data[0]["precio"],
                down_payment=terms["down_payment"],
                term=terms["term"],
            )
            response = financing_explainer.send_message(str(financing_plan))
        else:
            response = "Entiendo, seguimos sin financiamiento."
        state = "start"
        # except Exception as e:
        #     if verbose: print(f"Error: {e}")
        #     response = "¿A cuantos años quieres financiarlo y con cuanto de enganche?"

    # Save assistant message
    chat_manager.save_message(
        session_id=session_id,
        role="assistant",
        content=response,
        state=state,
        car_data=json.dumps(car_data) if car_data else None,
    )
    if verbose:
        print(f"🤖 {response}\n")
    return response
