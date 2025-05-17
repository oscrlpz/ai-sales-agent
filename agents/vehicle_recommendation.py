from typing import Dict

from pandas import DataFrame

from .baseagents._recommender import _Recommender
from .config.prompts import (
    VEHICLE_RECOMMENDATION_CONTEXT,
    VEHICLE_RECOMMENDATION_SYSTEM,
)


class VehicleRecommender(_Recommender):
    """
    A class to handle the recommendation process for vehicles.
    """

    weights = {
        "make": 50,
        "model": 50,
        "year": 10,
        "version": 20,
        "price": 30,
        "km": 20,
        "bluetooth": 20,
        "car_play": 20,
        "tamaño": 20,
        "carrocería": 20,
    }

    def __init__(self, model: str, data: DataFrame):
        """
        Initialize the recommender with a model and data.

        Args:
            model (str): The model to use for recommendations.
            data (DataFrame): The data to use for recommendations.
            weights (Dict[str, float], optional): Weights for the recommendation criteria.
                Defaults to None.
        """
        super().__init__(model, data, self.weights)
        self.system_prompt = VEHICLE_RECOMMENDATION_SYSTEM

    def get_recommendations(
        self, user_input: str, normalized_input: str, top_n: int = 1
    ) -> Dict[str, str]:
        """
        Get vehicle recommendations based on user input.

        Args:
            user_input (str): The user input to filter by.
            normalized_input (str): The normalized user input to filter by.
            top_n (int): The number of top recommendations to return.

        Returns:
            Dict[str, str]: The recommendations.
        """
        self.recommend(normalized_input, top_n)
        self.context = VEHICLE_RECOMMENDATION_CONTEXT.format(user_input=user_input)
        return self.recommendations
