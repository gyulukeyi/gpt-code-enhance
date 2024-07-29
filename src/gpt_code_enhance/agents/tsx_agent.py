from ..type import Agent


class TSX_Agent(Agent):

    def __init__(self) -> None:
        super().__init__()
        self.prompt = "Review the given TypeScript code for React.js and provide a concise analysis."