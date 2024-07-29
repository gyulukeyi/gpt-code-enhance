"""pipe.py 

A pipeline to generate enhanced code.
"""

import re
from typing import Literal, List

import tiktoken

from . import MODEL, LARGET_TOKEN_WARNING_THRESHOLD
from .type import Agent, Caller
from .callers.openai_gpt_caller import OpenAIGptCaller
from .agents.code_enhance_agent import CodeEnhanceAgent
from .agents.ts_agent import TS_Agent
from .agents.tsx_agent import TSX_Agent
from .agents.py_agent import PY_Agent

enc = tiktoken.encoding_for_model(MODEL)


class Pipe:
    agent: Agent
    caller: Caller

    def __init__(
        self,
        mode: Literal["codebase", "py", "ts", "tsx"],
        caller: Caller = OpenAIGptCaller(),
    ):
        self.agent = self.initialize_agent(mode)
        self.caller = caller

    def initialize_agent(self, mode: str) -> Agent:
        agents = {
            "codebase": CodeEnhanceAgent,
            "py": PY_Agent,
            "ts": TS_Agent,
            "tsx": TSX_Agent,
        }
        if mode not in agents:
            raise RuntimeError(f"unsupported mode {mode}")
        return agents[mode]()

    def enhance_codebase(self, codebase_dir: str, code_to_fix: str, ext: str) -> str:
        assert isinstance(
            self.agent, CodeEnhanceAgent
        ), "Should be codebase mode to refine a codebase"
        context = self.agent.make_context(codebase_dir, ext)
        self.check_token_count(context)
        
        messages = self.prepare_messages(context, code_to_fix)
        
        generated = self.generate_code(messages)
        return self.clean_generated_code(generated)

    def check_token_count(self, context: str) -> None:
        token_count = len(enc.encode(context))
        if token_count > LARGET_TOKEN_WARNING_THRESHOLD:
            print(f"context has {token_count:,d} tokens")
            if input("continue? (y/N): ").lower().strip() != "y":
                exit(1)

    def prepare_messages(self, context: str, code_to_fix: str) -> List[dict]:
        return [
            {
                "role": "system",
                "content": f"""
<<Context>>

{context}

<<Instruction>>

{self.agent.prompt}
                """,
            },
            {
                "role": "user",
                "content": f"make an improved version of the code for {code_to_fix}",
            }
        ]

    def generate_code(self, messages: List[dict]) -> List[str]:
        generated = []
        print("improving your code...")
        while True:
            out = self.caller.make_call(messages)
            generated.append(out["content"])
            if out["finished_by"] == "length":
                messages.append({"role": "assistant", "content": out["content"]})
            else:
                break
        return generated

    def clean_generated_code(self, generated: List[str]) -> str:
        gen_str = "\n\n".join(generated)
        gen_str = gen_str.replace("\r\n", "\n")
        return re.sub(r"(?:^|\n)```.*?(?:\n|$)", "", gen_str)

    def enhance_single(self, codefile: str) -> str:
        codestring = self.load_codefile(codefile)
        
        assert not isinstance(
            self.agent, CodeEnhanceAgent
        ), "Codebase mode cannot be used for single code enhance"
        
        messages = self.prepare_single_messages(codestring)
        
        understanding = self.caller.make_call(messages)
        messages.append({"role": "assistant", "content": understanding["content"]})
        messages.append(
            {
                "role": "user",
                "content": """make an improved version of the code. 
                
[CONDITION]
- make the code production-ready 
- make the code easy to read and maintain 
- avoid changing logics 
- avoid changing external dependencies
- response only with your changed code 
- do not explain your code. Just response with code.
""",
            }
        )

        generated = self.generate_code(messages)
        return self.clean_generated_code(generated)

    def load_codefile(self, codefile: str) -> str:
        with open(codefile, "r", encoding="utf-8") as f:
            return f.read()

    def prepare_single_messages(self, codestring: str) -> List[dict]:
        return [
            {"role": "system", "content": self.agent.prompt},
            {"role": "user", "content": codestring},
        ]