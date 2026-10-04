import sys 
from config import chat_model, rule , embeddings
from pathlib import Path
import marimo as mo

_repo_root = Path.cwd()

while not (_repo_root / "pyproject.toml").exists():
    _repo_root = _repo_root.parent

if str(_repo_root) not in sys.path:
    sys.path.append(str(_repo_root / "scripts"))    

# print(f"Repository root: {_repo_root}") # D:\AI Projects\agents

embedder = embeddings()
# text = "Apply 55 KG/ ha urea as a basel dressing."
# vector = embedder.embed_query(text)
#print(vector) 

def embed_sentences(embedder):
    sentences = [
        "Apply 55 kg/ha of urea as a basal dressing.",       # 0
        "Urea top dressing at 4 weeks is 75 kg/ha.",         # 1  same subject
        "Maha season runs September to March.",              # 2  different subject
        "Fertiliser application rates for paddy.",           # 3  same subject, no shared words
    ]

    vectors = embedder.embed_documents(sentences)

    for _i, _s in enumerate(sentences):
        print(f"  [{_i}] {len(vectors[_i])} numbers  <- {_s}")
    return


embed_sentences(embedder)