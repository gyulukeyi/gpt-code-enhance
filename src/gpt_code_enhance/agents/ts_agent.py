from ..type import Agent

class TS_Agent(Agent):
    def __init__(self) -> None:
        super().__init__()
        self.prompt = "Review the provided TypeScript code and provide a concise, step-by-step analysis."