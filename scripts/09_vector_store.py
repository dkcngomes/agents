import sys
import time
import marimo as mo

from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

# Local config & corpus imports
from pathlib import Path
from config import EMBED_DIM, INDEX_NAME, embeddings, require
from corpus import DOCS

# 1. Resolve workspace root and adjust system path
_repo_root = Path.cwd()
while not (_repo_root / "pyproject.toml").exists() and _repo_root != _repo_root.parent:
    _repo_root = _repo_root.parent

if (_repo_root / "scripts").exists() and str(_repo_root / "scripts") not in sys.path:
    sys.path.insert(0, str(_repo_root / "scripts"))


def main():
    # --- Lesson Overview ---
    mo.md(r"""
    # 10 · A Managed Vector Store, Through LangChain

    Run this notebook once. It creates the Pinecone index that lessons 11 and
    12 both query.

    Lesson 09 showed why exact search doesn't scale, and the idea behind
    HNSW: links, layers, and a dial between fast and accurate. Pinecone runs
    one for you. LangChain wraps it so the code is the same shape whatever
    store is underneath — swap `PineconeVectorStore` for FAISS or Chroma and
    the rest of this notebook is unchanged.
    """)

    # --- 1 · Create the Index ---
    mo.md(r"""
    ## 1 · Create the index

    The Pinecone client is only needed to create the index. After that,
    LangChain talks to it for you.
    """)

    pc = Pinecone(api_key=require("PINECONE_API_KEY"))

    # STEP 1 CREATE INDEX
    if not pc.has_index(INDEX_NAME):
        pc.create_index(
            name=INDEX_NAME,
            dimension=EMBED_DIM,  # 1536, because that is what the model returns
            metric="cosine",  # the metric you compared by hand in lesson 09
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        print(f"Created {INDEX_NAME!r}")
    else:
        print(f"{INDEX_NAME!r} index already exists")

    # --- 2 · Documents, Not Strings ---
    mo.md(r"""
    Two decisions, and you understand both now:

    - **dimension** — how many numbers per vector (lesson 08)
    - **metric** — how "close" is measured (lesson 09)

    ## 2 · Documents, not strings

    A LangChain `Document` is text plus metadata. Metadata is what you filter
    on.
    """)

    documents = [
        Document(
            page_content=d["text"],
            metadata={"source": d["source"], "category": d["category"]},
            id=d["id"],
        )
        for d in DOCS
    ]

    if documents:
        example = documents[4] if len(documents) > 4 else documents[0]
        print("page_content:", example.page_content[:90], "...")
        print("metadata    :", example.metadata)
        print("id          :", example.id)

    # --- 3 · Embed and Store ---
    mo.md(r"""
    The id is yours, so you can update or delete this passage by name later.

    ## 3 · Embed and store, in one call
    """)

    # Call embeddings function if it returns an instance, or pass directly
    embed_model = embeddings() if callable(embeddings) else embeddings
    store = PineconeVectorStore(index_name=INDEX_NAME, embedding=embed_model)
    store.add_documents(documents)

    print("add_documents method did three things we did by hand in an earlier level:")
    print("  1. embedded every page_content")
    print("  2. attached the metadata")
    print("  3. upserted the lot into Pinecone")

    # Poll serverless write status
    index = pc.Index(INDEX_NAME)
    count = 0
    for _ in range(60):
        count = index.describe_index_stats().get("total_vector_count", 0)
        if count >= len(documents):
            break
        time.sleep(1)
    print(f"Index now holds {count} vectors -- on a server, not in this process")

    # --- 4 · Search ---
    mo.md("""
    ## 4 · Search
    """)

    query = "How much urea for a three month variety, and when?"
    results = store.similarity_search_with_score(query, k=5)

    print("<<<<<<<<>>>>>>>>>>>>>>>>>>>>")
    print("query:", query, "\n")
    for _doc, _score in results:

        category = _doc.metadata.get("category", "N/A")
        doc_id = getattr(_doc, "id", "N/A") or "N/A"

        print(f"  {_score:.5f}  {doc_id:24s} [{category}]")
    print("<<<<<<<<>>>>>>>>>>>>>>>>>>>>")

    mo.md(r"""
    That interface matters. Anything shaped like a retriever can be dropped
    into a chain — or handed to an agent as a tool, which is exactly what
    lesson 12 does.
    """)

if __name__ == "__main__":
    main()