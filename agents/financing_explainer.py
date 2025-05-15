from .baseagents._basebot import _BaseBot
from .config.prompts import FINANCING_EXPLAINER


class FinancingExplainer(_BaseBot):
    _system_prompt = FINANCING_EXPLAINER
