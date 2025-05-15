import os

import pytest

from agents.utils.chat_history_manager import ChatHistoryManager

DB_PATH = "/home/oscar/projects/ai-sales-agent/data/db/chat_history.db"
SESSION_ID = "api_test_session_000"


@pytest.fixture(scope="module")
def session_id():
    yield SESSION_ID


@pytest.fixture(scope="module")
def chat_history(session_id):
    chat_manager = ChatHistoryManager(DB_PATH)
    yield
    chat_manager.get_history(session_id=session_id)
    # chat_manager.delete_session(SESSION_ID)


@pytest.fixture(scope="function")
def user_inputs_1():
    return [
        "Hola, mi nombre es Oscar",
        "Que sedes tienen en CDMX?",
        "Hola estoy buscando un honda cibic 2016",
        "Si, me gustaría financiarlo",
        "3 años y 20% de enganche",
        "A que hora abren?",
    ]


@pytest.fixture(scope="function")
def user_inputs_2():
    return [
        "Recuerdame cual el auto que me recomendaste?",
        "¿Cual era el plan de financiamiento?",
    ]
