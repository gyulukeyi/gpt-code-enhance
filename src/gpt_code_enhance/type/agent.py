"""agent.py

A type definition for an agent.
"""

from abc import ABC


class Agent(ABC):
    def __init__(self) -> None:
        self._caller = ""

    @property
    def prompt(self):
        """The caller property."""
        return self._caller

    @prompt.setter
    def prompt(self, value: str) -> None:
        self._caller = value
