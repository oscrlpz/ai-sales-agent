from typing import Any, Dict, List

from pandas import DataFrame

from ..utils.fuzzysearch import fuzzy_filter
from ._basebot import _BaseBot


class _Recommender(_BaseBot):
    """
    A class to handle the recommendation process for a given model.
    """

    def __init__(self, model: str, data: DataFrame, weights: Dict[str, float] = None):
        """
        Initialize the recommender with a model and data.

        Args:
            model (str): The model to use for recommendations.
            data (DataFrame): The data to use for recommendations.
            weights (Dict[str, float], optional): Weights for the recommendation criteria.
                Defaults to None.

        """
        super().__init__(model)
        self.data = data
        self.weights = weights if weights else None

    def recommend(self, user_input: str, top_n: int = 1):
        df_slice = fuzzy_filter(self.data, user_input, weights=self.weights)
        self._raw_recommendations = df_slice.nlargest(top_n, "similarity_score")

    def explain_recommendation(self) -> str:
        """
        Generate a human-readable explanation for the recommendation.

        Args:
            recommendation (DataFrame): The recommendation to explain.

        Returns:
            str: A human-readable explanation of the recommendation.
        """
        self.chat_history = []
        self.logger.info(
            f"Generating explanation for recommendation: {self.raw_recommendations}"
        )
        self.logger.info(f"Context: {self.context}")

        readable_recs = self.send_message(
            self.context.format(str(self.raw_recommendations)),
            stream=False,
        )
        return readable_recs

    @property
    def raw_recommendations(self) -> Dict[str, Any]:
        """Get the raw recommendations.

        Returns:
            Dict[str, Any]: The raw recommendations.
        """
        return self._raw_recommendations.to_dict(orient="records")

    @property
    def recommendations(self):
        return {
            "raw": self.raw_recommendations,
            "readable": self.explain_recommendation(),
        }

    @property
    def context(self):
        """The way the model should frame the recommendation request."""
        return self._context

    @context.setter
    def context(self, context: str):
        """Set the context for the model."""
        self._context = context
