import sys
import marimo as mo
from pathlib import Path
import sympy

from langchain.agents import create_agent
from langchain.tools import tool
from config import chat_model, rule


# Find the Script folder and add it to sys.path so we can import from it
_repo_root = Path.cwd()
#print("Current working directory:", _repo_root)

while not (_repo_root / "pyproject.toml").exists():
    _repo_root = _repo_root.parent
if str(_repo_root / "scripts") not in sys.path:
    sys.path.insert(0, str(_repo_root / "scripts"))

#print (_repo_root)    


