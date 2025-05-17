from .baseagents._basebot import _BaseBot
from .config.prompts import KAVAK_SALES


class KavakGeneralBot(_BaseBot):
    _system_prompt = KAVAK_SALES
