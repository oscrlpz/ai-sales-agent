from .baseagents._normalizer import _Normalizer
from .config.prompts import VEHICLE_NORMALIZATION


class VehicleNormalizer(_Normalizer):
    _prompt = dict(
        input_variables=["user_input"],
        template=VEHICLE_NORMALIZATION,
    )

    def __init__(self, model: str):
        super().__init__(model, self._prompt)
