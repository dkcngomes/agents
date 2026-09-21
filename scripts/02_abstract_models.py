from config import chat_model

model = chat_model()
response = model.invoke("Name the two paddy cultivation seasons in Sri Lanka.")

# print("=" * 100)
# print(response.usage_metadata)
# print("=" * 100)

# print("=" * 100)
# print(response.text)
# print("=" * 100)

# print("=" * 100)
# print(response.content)
# print("=" * 100)