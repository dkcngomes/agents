from openai import OpenAI
import os
from pathlib import Path
from dotenv import load_dotenv

# initialize environment variables from .env file
env_path = Path(__file__).parent.parent/".env"
result =  load_dotenv(dotenv_path=env_path, override=True)

# constants
OPEN_API_KEY = os.getenv("OPEN_API_KEY")
CHAT_MODEL = "gpt-5.6-luna"

client = OpenAI()

response = client.chat.completions.create(
    model=CHAT_MODEL,
    messages=[
        {"role": "user", "content": "What is the capital of France?"}
    ]
)

print(response.choices[0].message.content)