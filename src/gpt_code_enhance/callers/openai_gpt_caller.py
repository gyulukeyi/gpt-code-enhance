import os
from openai import OpenAI
from .. import MODEL
from ..type import Caller
from ..type.caller import CallOut


class OpenAIGptCaller(Caller):
    def __init__(self, api_key: str = os.environ.get("OPENAI_API_KEY", "")):
        super().__init__()
        self.caller = OpenAI(api_key=api_key)

    def make_call(self, messages, **kwargs) -> CallOut:
        response = self.caller.chat.completions.create(
            messages=messages,
            model=MODEL,
            max_tokens=4096,
            temperature=0.9,
            **kwargs,
        )

        return CallOut(
            finished_by=response.choices[0].finish_reason,
            content=response.choices[0].message.content,
        )