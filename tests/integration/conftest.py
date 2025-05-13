import os

import pytest

from agents.utils.chat_history_manager import ChatHistoryManager

DB_PATH = "/home/oscar/projects/ai-sales-agent/data/db/chat_history.db"
SESSION_ID = "test_session_000"


@pytest.fixture(scope="module")
def chat_history():
    chat_manager = ChatHistoryManager(DB_PATH)
    yield
    chat_manager.get_history(SESSION_ID)
    chat_manager.delete_session(SESSION_ID)


@pytest.fixture(scope="function")
def user_inputs_1():
    return [
        "Hola, mi nombre es Oscar",
        "Que sedes tienen en CDMX?",
        "Hola estoy buscando un honda cibic 2016",
        "Si, me gustaría financiarlo",
        "A que hora abren?",
        "exit",
    ]


@pytest.fixture(scope="function")
def user_inputs_2():
    return [
        "Recuerdame cual el auto que me recomendaste?",
        "exit",
    ]


@pytest.fixture(scope="module")
def set_env_var():
    # Set the environment variable
    os.environ["TEST_SESSION_ID"] = SESSION_ID
    yield  # Test will run here
    # Cleanup: Reset the environment variable after the test if needed
    del os.environ["TEST_SESSION_ID"]
