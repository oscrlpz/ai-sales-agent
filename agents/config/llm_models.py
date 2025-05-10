import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

AVAILABLE_MODELS = {
    "local-deepseek-r1:14b": {
        "model_name": "deepseek-r1:14b",
        "url": "http://localhost:11434/v1",
        "api_key": "not-needed",
    },
    "deepseek-v3": {
        "model_name": "deepseek-chat",
        "url": "https://api.deepseek.com",
        "api_key": DEEPSEEK_API_KEY,
    },
    "deepseek-r1": {
        "model_name": "deepseek-reasoner",
        "url": "https://api.deepseek.com",
        "api_key": DEEPSEEK_API_KEY,
    },
    "gpt-3.5-turbo": {
        "model_name": "gpt-3.5-turbo",
        "url": "https://api.openai.com/v1",
        "api_key": OPENAI_API_KEY,
    },
}
