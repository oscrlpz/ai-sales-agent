from ..utils.jsonformat import json_to_dict
from ._basebot import _BaseBot


class Classifier(_BaseBot):
    @property
    def input(self):
        """Get the input for the LLM."""
        return json_to_dict(self._input)

    @input.setter
    def input(self, value):
        self._input = value

    def classify(self, _input: str) -> dict:
        """Classify the input using the LLM.

        Args:
            _input (str): The input to classify.

        Returns:
            dict: The classification result.
        """
        self.logger.info(f"Classifying input: {_input}")
        self.chat_history = []
        self.input = self.send_message(_input, stream=False)
        response = self.input.copy()
        response.update({"input": _input})
        return response


if __name__ == "__main__":
    classifier = Classifier(model="deepseek-v3")

    classifier.system_prompt = """Eres un asistente que clasifica las respuestas de los clientes. El cliente te va a responder si desea un plan de financiamiento o no. Tu tarea es clasificar la respuesta en dos categorias: 'si' o 'no'. Si el cliente dice que si, entonces devuelve 'si', si el cliente dice que no, entonces devuelve 'no'. Responde unicamente con el diccionario JSON que contiene la respuesta. No incluyas ningun otro texto." 
    Ejemplo:

    El cliente dice: "si, me interesa un plan de financiamiento"
    Respuesta: 
    {"response": true}
    """

    classifier.classify("si, me interesa un plan de financiamiento")
