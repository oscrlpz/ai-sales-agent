import json
import logging
from typing import Any, Dict

from langchain.prompts import PromptTemplate

# from langchain.chains import LLMChain
from langchain_core.runnables import RunnableSequence
from langchain_openai.chat_models import ChatOpenAI

from ..config.llm_models import AVAILABLE_MODELS
from ..utils.jsonformat import json_to_dict


class _Normalizer:
    logger = logging.getLogger(__name__)
    _temperature = 0

    def __init__(self, model: str, _prompt: dict):
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
        self._prompt = dict(
            input_variables=_prompt["input_variables"],
            template=_prompt["template"],
        )

    @property
    def temperature(self):
        """Get the temperature for the LLM."""
        return self._temperature

    @temperature.setter
    def temperature(self, value: float):
        """Set the temperature for the LLM.

        Args:
            value (float): The temperature value to set.

        Raises:
            ValueError: If the temperature is not a number or is not between 0 and 1.
        """
        if not isinstance(value, (int, float)):
            raise ValueError("Temperature must be a number.")
        if value < 0 or value > 1:
            raise ValueError("Temperature must be between 0 and 1.")
        self._temperature = value

    @property
    def prompt(self):
        """Get the prompt for the LLM."""
        return PromptTemplate(**self._prompt)

    @prompt.setter
    def prompt(self, value: dict):
        """Set the prompt for the LLM.

        Args:
            value (dict): The prompt dictionary to set.

        Raises:
            ValueError: If the prompt is not a dictionary or does not contain the required keys.
        """
        if not isinstance(value, dict):
            raise ValueError("Prompt must be a dictionary.")
        if "template" not in value.keys():
            raise ValueError("Prompt must contain 'template' key.")
        if "input_variables" not in value.keys():
            raise ValueError("Prompt must contain 'input_variables' key.")
        self._prompt = dict(
            input_variables=value["input_variables"],
            template=value["template"],
        )

    def normalize(self, user_input: str) -> Dict[str, Any]:
        """
        Normalize the user input using the LLM chain.

        Args:
            user_input (str): The user input to normalize.

        Returns:
            str: The normalized output.
        """
        # chain = self.prompt | self.client  # RunnableSequence: prompt -> LLM Another way to do this:
        chain = RunnableSequence(first=self.prompt, last=self.client)
        response = chain.invoke({"user_input": user_input})
        self.logger.info(f"Response from LLM: {response}")
        return json_to_dict(response.content)
