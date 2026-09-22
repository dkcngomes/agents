from config import chat_model, rule
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from corpus import DOCS

model = chat_model()

QUESTION = "I'm growing BG 300 paddy under irrigation in the Dry Zone. Exactly how much urea fertilizer should I apply to get the best yield? and at what times.Give me the schedule in KG per hecture"

SYSTEM = SystemMessage("You are a terse agricultural advisor for Sri Lankan farmers")

#rule("<ASK IT THREE TIMES>")

#print(QUESTION)

# Example 1 - repeetitive questioning the same question to see if the model gives the same answer each time. This is a test of consistency and reliability of the model's responses.
# for attempt in (1, 2, 3):
#     print(f"\n----- Attempt {attempt}" + "-" * 25)
    
#     # 1. Pass messages inside a list: [SYSTEM, HumanMessage(QUESTION)]
#     # 2. Access .content from the returned AIMessage
#     response = model.invoke([SYSTEM, HumanMessage(QUESTION)])
#     print(response.content)

# Example 2 - provide facts with corpse
rule("<COPY THE DOCS INTO THE SYSTEM PROMPT>")    
facts = DOCS
#print(facts)

grounded = model.invoke([
    SystemMessage(f"You are a terse agricultural advisor for Sri Lankan farmers. Here are some facts about rice varieties in Sri Lanka: {facts}. Quote from these facts to answer the questions."),
    HumanMessage(QUESTION)
])

print(grounded.text)