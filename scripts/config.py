"""Shared setup. The only file here that is not a lesson concept.

Everything else is a numbered script you run top to bottom. This holds the model
names and the key checks so thirteen files do not each repeat them.
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

CHAT_MODEL_RAW = "gpt-5.6-luna"           # what the OpenAI API itself takes (00)
CHAT_MODEL = f"openai:{CHAT_MODEL_RAW}"   # provider:model — LangChain resolves it
EMBED_MODEL = "text-embedding-3-small"
EMBED_DIM = 1536

INDEX_NAME = os.getenv("PINECONE_INDEX", "fieldoracle")
NTFY_TOPIC = os.getenv("NTFY_TOPIC", "")


def require(name: str) -> str:
    """Exit with something readable instead of a stack trace."""
    value = os.getenv(name)
    if not value:
        sys.exit(
            f"\n{name} is not set.\n"
            f"Copy .env.example to .env, fill it in, and run this again.\n"
        )
    return value


def chat_model(**kwargs):
    """The chat model every file uses.

    init_chat_model takes "provider:model" and hands back a chat model object.

    use_responses_api routes every call to OpenAI's /v1/responses endpoint, which
    is the one that allows function tools alongside reasoning — /v1/chat/completions
    rejects that combination for gpt-5.6-luna. OpenAI-only, but so is this project.
    """
    from langchain.chat_models import init_chat_model

    require("OPENAI_API_KEY")
    return init_chat_model(CHAT_MODEL, use_responses_api=True, **kwargs)


def embeddings():
    from langchain_openai import OpenAIEmbeddings

    require("OPENAI_API_KEY")
    return OpenAIEmbeddings(model=EMBED_MODEL)


def rule(title: str = "") -> None:
    """Section heading, so a script reads like a lesson while it runs."""
    print("\n" + "=" * 78)
    if title:
        print(title)
        print("=" * 78)