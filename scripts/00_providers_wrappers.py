#import os
#from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# initialize environment variables from .env file
# env_path = Path(__file__).parent.parent/".env"
# result =  load_dotenv(dotenv_path=env_path, override=True)
# OPEN_API_KEY = os.getenv(" ")

load_dotenv()

# constants
CHAT_MODEL = "gpt-5.6-luna"

client = OpenAI()

 
response = client.chat.completions.create(
    model=CHAT_MODEL,
    messages=[
        {"role": "user", "content": "Name the two paddy cultivation sesasons in Sri Lanka."}
    ]
)

print("=" * 100)
print(response.choices[0].message.content)
print("=" * 100)