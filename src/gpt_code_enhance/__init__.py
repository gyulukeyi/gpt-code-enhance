import os
import dotenv

ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
dotenv.load_dotenv(ENV_PATH, override=True)

MODEL = "gpt-4o-mini"
LARGET_TOKEN_WARNING_THRESHOLD = 10_000

__all__ = ["MODEL"]