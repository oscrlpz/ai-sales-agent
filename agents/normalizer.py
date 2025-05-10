import json
import logging
from typing import Optional, Dict, Any
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from .config.llm_models import AVAILABLE_MODELS
from .config.prompts import VEHICLE_NORMALIZATION   




class VehicleNormalizer:
    logger = logging.getLogger(__name__)    
    _temperature = 0
    _prompt = dict(
        input_variables=["user_input"],
        template=VEHICLE_NORMALIZATION,
    )

    def __init__(self, model: str):
        self.model = model
        self.model_info = AVAILABLE_MODELS[model]
        self.base_url = self.model_info["url"]
        self.model_name = self.model_info["model_name"]
        self.api_key = self.model_info["api_key"]

        self.client = ChatOpenAI(
            model=self.model_name,
            openai_api_key=self.api_key,
            openai_api_base=self.base_url,
            temperature=self.temperature,
        )

    @property
    def temperature(self):
        return self._temperature
    
    @temperature.setter
    def temperature(self, value: float):
        if not isinstance(value, (int, float)):
            raise ValueError("Temperature must be a number.")
        if value < 0 or value > 1:
            raise ValueError("Temperature must be between 0 and 1.")
        self._temperature = value

    @property
    def prompt(self):
        return PromptTemplate(**self._prompt)
    
    @prompt.setter
    def prompt(self, value: dict):
        if not isinstance(value, dict):
            raise ValueError("Prompt must be a dictionary.")
        if "template" not in value.keys():
            raise ValueError("Prompt must contain 'template' key.")
        if "input_variables" not in value.keys():
            raise ValueError("Prompt must contain 'input_variables' key.")
        self._prompt = value

    def normalize(self, user_input: str) -> Dict[str, Any]:
        """
        Normalize the user input using the LLM chain.

        Args:
            user_input (str): The user input to normalize.

        Returns:
            str: The normalized output.
        """
        normalize_chain = LLMChain(
            llm=self.client,
            prompt=self.prompt,
        )
        response = normalize_chain.run(user_input=user_input)
        self.logger.info(f"Response from LLM: {response}")
        return self._to_json(response)
    
    @staticmethod
    def _to_json(response: str) -> dict:
        """
        Convert the response string to a JSON object.

        Args:
            response (str): The response string to convert.

        Returns:
            dict: The converted JSON object.
        """
        response = response.replace("'", '"')
        response = response.replace("\n", "")
        response = response.replace(" ", "")
        # if ```json is present, remove it and the closing ```
        if response.startswith("```json"):
            response = response[7:]
        if response.endswith("```"):
            response = response[:-3]
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode JSON: {e}")