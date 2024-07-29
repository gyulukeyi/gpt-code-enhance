"""caller.py

A type definition for a caller.
"""

from typing import TypedDict
from abc import ABC, abstractmethod


class CallOut(TypedDict):
    content: str
    finished_by: str


class Caller(ABC):
    def __init__(self):
        self._prompt = ""

    @property
    def prompt(self) -> str:
        """The prompt property."""
        return self._prompt

    @prompt.setter
    def prompt(self, value: str) -> None:
        self._prompt = value

    @abstractmethod
    def make_call(self, messages: list, **kwargs) -> CallOut: 
        ...