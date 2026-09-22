from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

CHAT_MODEL_RAW = "gpt-5.6-luna"
CHAT_MODEL = f"openai:{CHAT_MODEL_RAW}" # provider and model name

def chat_model(**kwargs):
    return init_chat_model(CHAT_MODEL, **kwargs)

def rule(title: str = "") -> None:
    """
    Section Heading
    """
    if title:
        print("=" * 100)
        print(title)
        print("=" * 100)