from ..type import Agent

class PY_Agent(Agent):

    def __init__(self) -> None:
        super().__init__()
        self.prompt = "Review the given Python code and provide a concise, step-by-step analysis."