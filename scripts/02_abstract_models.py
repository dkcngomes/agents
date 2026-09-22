from config import chat_model,rule
from langchain_core.messages import SystemMessage , HumanMessage

# print("=" * 100)
# print(response.usage_metadata)
# print("=" * 100)

# print("=" * 100)
# print(response.text)
# print("=" * 100)

# print("=" * 100)
# print(response.content)
# print("=" * 100)

# Example 1
rule(" MESSAGE WITHOUT ROLES ")
model = chat_model()
response = model.invoke("Name the two paddy cultivation seasons in Sri Lanka.")
print (response.text)

# Example 2 
rule(" MESSAGE WITH ROLES ")
messages = [
    SystemMessage("You are a terse agricultural advisor for Sri Lankan farmers"),
    HumanMessage("What is BG 300?"),
]

response = model.invoke(messages)
print (response.text)
print("=" * 100)