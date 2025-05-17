from .baseagents._classifier import Classifier
from .config.prompts import (
    BOOLEAN_FINANCING_CLASSIFICATION,
    FINANCING_TERM_CLASSIFICATION,
    INTENT_CLASSIFICATION,
)


class FinancingBoolClassifier(Classifier):
    """
    A class to classify whether a customer is interested in financing or not.
    """

    def __init__(self, model: str):
        super().__init__(model)
        self.system_prompt = BOOLEAN_FINANCING_CLASSIFICATION


class IntentClassifier(Classifier):
    """
    A class to classify general customer queries.
    """

    def __init__(self, model: str):
        super().__init__(model)
        self.system_prompt = INTENT_CLASSIFICATION


class FinancingTermClassifier(Classifier):
    """
    A class to classify the financing term.
    """

    def __init__(self, model: str):
        super().__init__(model)
        self.system_prompt = FINANCING_TERM_CLASSIFICATION
