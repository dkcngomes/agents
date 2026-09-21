from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# constants
CHAT_MODEL = "gpt-5.6-luna"
QUESTION = "Name the two paddy cultivation sesasons in Sri Lanka."

load_dotenv()

chat_model = ChatOpenAI(model=CHAT_MODEL, temperature=0.7, max_tokens=1000)
response = chat_model.invoke(QUESTION)

print("=" * 100)
print(response.text)
print("=" * 100)