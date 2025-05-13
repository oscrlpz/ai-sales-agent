import logging

from .baseagents._basebot import _BaseBot
from .config.prompts import KAVAK_SALES


class KavakGeneralBot(_BaseBot):
    logger = logging.getLogger(__name__)
    _system_prompt = KAVAK_SALES
