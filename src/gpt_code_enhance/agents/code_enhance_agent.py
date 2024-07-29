import os
from ..type import Agent


class CodeEnhanceAgent(Agent):

    def __init__(self) -> None:
        super().__init__()
        self.prompt = """
[YOUR TASK]
Transform the provided code to be production-ready, as well as easy to read and maintain, without altering its logic or external dependencies.

[CONDITION]
- The code must be production-ready.
- Enhance readability and maintainability.
- Preserve the existing logic.
- Do not change external dependencies.
- Provide only the modified code.
- Do not include any explanations, comments, or any other form of text—only the modified code.
- Include only revised code.
"""

    def make_context(self, codebase_dir: str, ext: str) -> str:
        """
        Iterate through a codebase and create a plain text context
        """
        codefiles = []
        for root, dirs, files in os.walk(codebase_dir):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            if os.path.basename(root).startswith("."):
                continue
            for f in files:
                if f.startswith("."):
                    continue
                if ext == "" or os.path.splitext(f)[-1].lower().strip(
                    "."
                ) == ext.lower().strip("."):
                    codefiles.append(os.path.join(root, f))

        contextL = []
        for f in codefiles:
            try:
                with open(f, "r", encoding="utf-8") as fp:
                    contextL.append(
                        f"#### {f}\n```{os.path.splitext(f)[1].strip('.')}\n{fp.read()}\n```"
                    )
            except UnicodeDecodeError:
                continue

        return "\n\n".join(contextL)
