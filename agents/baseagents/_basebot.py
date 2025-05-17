import logging
import re
from typing import Any, Dict, List

from openai import OpenAI

from ..config.llm_models import AVAILABLE_MODELS


class _BaseBot:
    logger = logging.getLogger(__name__)
    _chat_history: List[Dict[str, str]] = []
    _system_prompt: str = None

    def __init__(self, model: str):
        self.model = model
        self.model_info = AVAILABLE_MODELS[model]
        self.base_url = self.model_info["url"]
        self.model_name = self.model_info["model_name"]
        self.api_key = self.model_info["api_key"]
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    @staticmethod
    def _merge_consecutive_messages(messages):
        if not messages:
            return []

        merged = [messages[0]]
        for msg in messages[1:]:
            last = merged[-1]
            if msg["role"] == last["role"]:
                last["content"] += "\n" + msg["content"]
            else:
                merged.append(msg)
        return merged

    @property
    def chat_history(self):
        history = [
            {"role": x["role"], "content": x["content"]} for x in self._chat_history
        ]
        history = self._merge_consecutive_messages(history)

        if hasattr(self, "system_prompt") and self.system_prompt:
            sys_prompt = {"role": "system", "content": self.system_prompt}
            history = [sys_prompt] + history
        return [{"role": x["role"], "content": x["content"]} for x in history]

    @chat_history.setter
    def chat_history(self, _chat_history: List[Dict[str, str]]):
        self._chat_history = _chat_history

    @property
    def system_prompt(self):
        return self._system_prompt

    @system_prompt.setter
    def system_prompt(self, _system_prompt: str):
        self._system_prompt = _system_prompt.strip()
        self.logger.info(f"Setting system prompt: {self._system_prompt}")

    def _update_chat_history(self, role: str, content: str):
        self._chat_history.append({"role": role, "content": content})
        self.logger.info(f"Updated chat history with {role}: {content}")

    def send_message(self, message: str, stream: bool = False):
        self.logger.info(f"Sending message: {message}")
        self._update_chat_history(role="user", content=message)
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=self.chat_history,
            stream=stream,
        )
        self.response = response
        if stream is False:
            response_content = response.choices[0].message.content
            self._update_chat_history(role="assistant", content=response_content)
            self.logger.info(f"Received response: {response_content}")
            return response_content

    def yield_response(self, max_chars: int = 500):
        """
        Yields complete sentences from a streamed response, only when a sentence ends with a period,
        exclamation mark, question mark, or newline, and the accumulated self.buffer has reached at least `max_chars`.
        Also ensures the last remainder is yielded even if it's smaller than `max_chars`.
        """
        if not hasattr(self, "response"):
            raise ValueError(
                "No streamed response found. Call send_message(..., stream=True) first."
            )

        self.buffer = ""
        last_yielded_index = 0

        # Updated pattern to capture sentence-ending punctuation: . ? ! \n
        sentence_end_pattern = re.compile(r"[.!?](?=\s|$)|\n")

        try:
            for chunk in self.response:
                delta = chunk.choices[0].delta.content or ""
                self.buffer += delta

                if len(self.buffer) < max_chars:
                    continue  # wait until self.buffer has enough text to yield

                # Find all sentence ends
                sentence_boundaries = [
                    m.end() for m in sentence_end_pattern.finditer(self.buffer)
                ]

                for end_idx in sentence_boundaries:
                    if end_idx <= last_yielded_index:
                        continue  # already yielded

                    if end_idx - last_yielded_index >= max_chars:
                        candidate = self.buffer[last_yielded_index:end_idx].strip()
                        if candidate:  # Make sure the candidate is not empty
                            yield candidate
                            last_yielded_index = end_idx
                            break  # yield one chunk per iteration

            # Yield any remaining text if it's a complete sentence, even if it's smaller than max_chars
            remainder = self.buffer[last_yielded_index:].strip()
            if remainder:
                yield remainder

        except Exception as e:
            self.logger.error(f"Error yielding streamed response: {e}")
            raise
