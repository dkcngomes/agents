import sys
import marimo as mo
from pathlib import Path

# Find the Script folder and add it to sys.path so we can import from it
_repo_root = Path.cwd()

#print("Current working directory:", _repo_root)

while not (_repo_root / "pyproject.toml").exists():
    _repo_root = _repo_root.parent
if str(_repo_root / "scripts") not in sys.path:
    sys.path.insert(0, str(_repo_root / "scripts"))

#print(str(_repo_root / "scripts")) # D:\AI Projects\agents\scripts
    
from langchain.agents import create_agent
from langchain.tools import tool
from config import chat_model, rule


@tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    #print(f"   >>> add({a}, {b}) = {a + b}")
    return a + b

@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    #print(f"   >>> add({a}, {b}) = {a + b}")
    return a * b

@tool
def substract(a: float, b: float) -> float:
    """Substract one number form another number."""
    return a * b

@tool
def division(a: float, b: float) -> float:
    """Divide one number form another number."""
    return a / b

agent = create_agent(
    chat_model(),
    tools=[add],
    system_prompt="""You are a calculator. You can not do calculations yourself. Using the tools provided you can do arithmatic operations asked for, .In your final answer also mention the work out solution""",
    
)

# simple_result =  agent.invoke({"messages": [("user", "What is 20 + 25?")]})
# print("Addition Final Answer:", simple_result)
# print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

# simple_result2 =  agent.invoke({"messages": [("user", "What is 20 multiply by 100?")]})
# print("Multiplication Final Answer:", simple_result2)
# print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

# simple_result3 =  agent.invoke({"messages": [("user", "What is 20 substracted from 100?")]})
# print("Substraction Final Answer:", simple_result3)
# print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

# simple_result4 =  agent.invoke({"messages": [("user", "What is 1000 divided from 100?")]})
# print("Division Final Answer:", simple_result4)
# print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

question = """A farmer has 3 plots of 1.75 hectares each.Urea is applied at 225 KG each per hectare.And a bag holds 50 KG.How many bags does he needs and how much left over ?"""

simple_result =  agent.invoke({"messages": [("user", question)]})

final_content = simple_result["messages"][-1].content
text_result = final_content[0]["text"]
print(text_result)
