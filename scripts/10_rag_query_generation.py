import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import sys
    from pathlib import Path

    _repo_root = Path.cwd()
    while not (_repo_root / "pyproject.toml").exists():
        _repo_root = _repo_root.parent
    if str(_repo_root / "scripts") not in sys.path:
        sys.path.insert(0, str(_repo_root / "scripts"))
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # 11 · RAG, and the Step Everyone Skips

    Retrieval-Augmented Generation is two steps: search, then answer from what
    you found. You control both.

    The step people skip is that **what the user typed is rarely a good search
    query**. This notebook shows the difference costing you the right answer,
    then fixes it by having the model write the query.

    Run `10_vector_store.py` first.
    """)
    return


@app.cell
def _():
    from langchain.messages import HumanMessage, SystemMessage
    from langchain_pinecone import PineconeVectorStore

    from config import INDEX_NAME, chat_model, embeddings

    model = chat_model()
    store = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings())

    ANSWER_SYSTEM = SystemMessage(
        "You are an advisor for Sri Lankan paddy farmers. Answer ONLY from the "
        "passages provided. Quote exact figures and cite the source name in square "
        "brackets after each one. If the passages do not answer the question, say so "
        "plainly -- do not fill the gap yourself."
    )

    def answer_from(passages: str, question: str) -> str:
        return model.invoke([
            ANSWER_SYSTEM,
            HumanMessage(f"Passages:\n{passages}\n\nQuestion: {question}"),
        ]).text

    def format_docs(docs) -> str:
        return "\n\n".join(f"[{d.metadata['source']}]\n{d.page_content}" for d in docs)

    return HumanMessage, SystemMessage, answer_from, format_docs, model, store


@app.cell
def _(mo):
    mo.md(r"""
    ## 1 · The naive version — search with exactly what they typed
    """)
    return


@app.cell
def _():
    USER_TEXT = (
        "Hi, quick one -- I'm the guy with the plot near the tank in Polonnaruwa, "
        "put Bg 300 in about three weeks back. Wife says I should be putting "
        "something down again around now? What do you reckon"
    )

    print("What the farmer actually typed:\n")
    print(" ", USER_TEXT)
    print("<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>")
    return (USER_TEXT,)


@app.cell
def _(USER_TEXT, store):
    naive = store.similarity_search(USER_TEXT, k=3)
    print("retrieved with that as the query:")
    for _d in naive:
        print(f"   {_d.id:24s} [{_d.metadata['category']}]")
    return (naive,)


@app.cell
def _(USER_TEXT, answer_from, format_docs, naive):
    print(answer_from(format_docs(naive), USER_TEXT))
    print("<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 2 · Why that searched badly

    The message is mostly noise, as far as an embedding is concerned: a
    greeting, a tank, a wife, "what do you reckon". Those words carry as much
    weight as the two that matter.

    The embedding is the average meaning of the *whole* string. Bury "Bg 300"
    and "three weeks" in chat and you drag the vector away from the fertilizer
    passages and toward nothing in particular.

    ## 3 · Let the model write the query
    """)
    return


@app.cell
def _(HumanMessage, SystemMessage, USER_TEXT, model):
    QUERY_SYSTEM = SystemMessage(
        "You turn a farmer's message into a search query for an agronomy database. "
        "Output ONLY the query -- no preamble, no punctuation beyond what is needed. "
        "Keep it under twelve words. Use the technical terms an agronomy document "
        "would use, not the farmer's phrasing."
    )

    search_query = model.invoke([QUERY_SYSTEM, HumanMessage(USER_TEXT)]).text.strip()
    print("<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("farmer  :", USER_TEXT[:70], "...")
    print("query   :", repr(search_query))
    print("<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>")
    return QUERY_SYSTEM, search_query


@app.cell
def _(search_query, store):
    better = store.similarity_search(search_query, k=3)
    print("<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("retrieved with the generated query:")
    for _d in better:
        print(f"   {_d.id:24s} [{_d.metadata['category']}]")
    return (better,)


@app.cell
def _(USER_TEXT, answer_from, better, format_docs):
    print(answer_from(format_docs(better), USER_TEXT))
    return


@app.cell
def _(mo):
    mo.md("""
    ## 4 · Compare
    """)
    return


@app.cell
def _(better, naive):
    print("naive     :", [d.id for d in naive])
    print("generated :", [d.id for d in better])
    return


@app.cell
def _(mo):
    mo.md(r"""
    Same index, same embeddings, same model. Only the **string that got
    embedded** changed, and the retrieved set changed with it.

    This is the cheapest improvement available in RAG, and it's one extra
    model call. Remember it when your retrieval looks bad — the problem is
    often the query, not the index.

    Note what happened there: the model was used **twice**, for two different
    jobs. Once to write a query, once to write an answer. Neither call knew
    about the other.

    ## 5 · Where this still breaks
    """)
    return


@app.cell
def _(HumanMessage, QUERY_SYSTEM, model, store):
    FOLLOW_UP = "And what changes if I switch to Bg 352 instead?"
    q2 = model.invoke([QUERY_SYSTEM, HumanMessage(FOLLOW_UP)]).text.strip()
    print("<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("question:", FOLLOW_UP)
    print("query   :", repr(q2))

    docs2 = store.similarity_search(q2, k=3)
    print("retrieved:", [d.id for d in docs2])
    return FOLLOW_UP, docs2


@app.cell
def _(FOLLOW_UP, answer_from, docs2, format_docs):
    print(answer_from(format_docs(docs2), FOLLOW_UP))
    return


@app.cell
def _(mo):
    mo.md(r"""
    Bg 352 is a 3.5-month variety, so the right answer moves the last dressing
    to week 8. Getting there needs **two passages joined together**:

    - one saying Bg 352 is a 3.5-month variety
    - one giving the 3.5-month schedule

    Your code searches **once**. However good the query is, one search cannot
    go back for a second thing it only realised it needed after reading the
    first.

    A better query does not fix this. A bigger index does not fix this.
    Something has to **decide to search again**.

    ---
    **Next: `12_agentic_rag.py`**.
    """)
    return


if __name__ == "__main__":
    app.run()