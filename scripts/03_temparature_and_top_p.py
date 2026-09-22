# nuclear sampling
from config import chat_model,rule
from langchain_core.messages import SystemMessage , HumanMessage , AIMessage

# reasoning models can not have a temperature above 0, so we will use a different model for the hot case
cold = chat_model(reasoning_effort="none", temperature=0)
hot = chat_model(reasoning_effort="medium", temperature=2.0)

rule("<MESSAGE WITH TEMPARATURE AND TOP_P>")

response = cold.invoke([HumanMessage("Give me a list of 10 random numbers between 1 and 100.")])
print(f"Response: {response.text}")

print("=" * 100)
response = hot.invoke([HumanMessage("Give me a list of 10 random numbers between 1 and 100.")])
print(f"Response: {response.text}")