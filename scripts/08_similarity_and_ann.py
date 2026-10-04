import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # 09 · How "Close" Is Measured, and Why Big Searches Cheat

    Two ideas, in this order:

    1. cosine vs. euclidean, on 2-D vectors small enough to check by hand
    2. exact search is slow, and the trick every vector database uses instead

    No API key needed. Everything here is local, and you can check the first
    two sections' numbers with a pen.
    """)
    return


@app.cell
def _():
    import time

    import numpy as np

    return np, time


@app.cell
def _(mo):
    mo.md(r"""
    ## 1 · Two ways to say "close"

    `a` and `b` point in the same direction, but `b` is three times longer.
    `c` is the same length as `a`, but points in a completely different
    direction.
    """)
    return


@app.cell
def _(np):
    a = np.array([2.0, 2.0])     # up-right
    b = np.array([6.0, 6.0])     # same direction as a, longer
    c = np.array([2.0, -2.0])    # same length as a, opposite direction

    print("a =", a, "  b =", b, "  (same direction as a, longer)")
    print("c =", c, "  (same length as a, different direction)")
    return a, b, c


@app.cell
def _(a, b, c, np):
    def euclidean(p, q):
        """Straight-line distance. Lower is closer."""
        return float(np.linalg.norm(p - q))

    def cosine_similarity(p, q):
        """Angle between them: 1 = same direction, 0 = perpendicular, -1 = opposite."""
        return float(np.dot(p, q) / (np.linalg.norm(p) * np.linalg.norm(q)))

    print(f"{'pair':8s} {'euclidean':>12s} {'cosine':>10s}")
    print(f"{'a vs b':8s} {euclidean(a, b):>12.3f} {cosine_similarity(a, b):>10.3f}")
    print(f"{'a vs c':8s} {euclidean(a, c):>12.3f} {cosine_similarity(a, c):>10.3f}")
    return cosine_similarity, euclidean


@app.cell
def _(mo):
    mo.md(r"""
    Read that carefully. By euclidean distance, `a` is closer to `c` than to
    `b`. By cosine, `a` is **identical** to `b` (1.0) and **perpendicular** to
    `c` (0.0).

    Cosine ignores length and only looks at direction — exactly what text
    needs: a long paragraph and a short sentence about the same thing should
    match, even though one is ten times longer. That's why text vector stores
    default to cosine.

    ## 2 · On unit vectors, the two metrics agree
    """)
    return


@app.cell
def _(a, b, c, cosine_similarity, euclidean, np):
    au, bu, cu = (v / np.linalg.norm(v) for v in (a, b, c))
    print("divide each vector by its own length, and:")
    print(f"  euclidean(a,b) = {euclidean(au, bu):.3f}   cosine(a,b) = {cosine_similarity(au, bu):.3f}")
    print(f"  euclidean(a,c) = {euclidean(au, cu):.3f}   cosine(a,c) = {cosine_similarity(au, cu):.3f}")
    return


@app.cell
def _(mo):
    mo.md(r"""
    Same ranking under both metrics. That's why stores usually normalise
    vectors on the way in — then a plain dot product equals cosine similarity,
    and a dot product is the cheapest thing a computer computes.

    ## 3 · Exact search checks every vector

    k-nearest-neighbours, done exactly, means: score the query against every
    vector you have and keep the best `k`. Foolproof, because nothing is
    skipped — and O(N): double the data, double the work.
    """)
    return


@app.cell
def _(np):
    DIM = 256
    exact_rng = np.random.default_rng(0)

    def exact_knn(data, query, k=10):
        """Brute force: score every vector against the query, take the top k."""
        scores = data @ query
        return np.argsort(scores)[::-1][:k]

    return DIM, exact_knn, exact_rng


@app.cell
def _(DIM, exact_knn, exact_rng, np, time):
    print(f"{'vectors':>10}  {'ms per query':>13}")
    for _n in (1_000, 20_000, 100_000):
        _data = exact_rng.random((_n, DIM), dtype=np.float32)
        _data /= np.linalg.norm(_data, axis=1, keepdims=True)
        _reps = max(3, 30_000 // _n)
        _t0 = time.perf_counter()
        for _ in range(_reps):
            exact_knn(_data, _data[0])
        print(f"{_n:>10,}  {(time.perf_counter() - _t0) / _reps * 1000:>13.2f}")
        del _data
    return


@app.cell
def _(mo):
    mo.md(r"""
    Linear, as promised. Now imagine 50 million rows and 200 people searching
    at once. This section is the whole reason vector databases exist.

    ## 4 · Approximate search: hop, don't look

    Approximate Nearest Neighbour (ANN) search gives up the guarantee "these
    are the best k" in exchange for not looking at most of the data.

    The whole trick fits in one sentence: before searching, **connect** each
    vector to a few of its neighbours; a query then hops from vector to vector
    along those links, always to the neighbour most like the query, and stops
    when no hop improves it.

    Watch it happen on made-up data — 45 vectors in three topic clusters.
    """)
    return


@app.cell
def _(np):
    graph_rng = np.random.default_rng(7)
    centres = np.array([[0.0, 0.0], [5.0, 0.0], [2.0, 5.0]])
    points = np.vstack([c + graph_rng.normal(0, 0.4, (15, 2)) for c in centres])
    cluster = np.repeat([0, 1, 2], 15)
    points = points / np.linalg.norm(points, axis=1, keepdims=True)
    N = len(points)

    # the "links" -- every vector remembers its 3 most similar vectors
    similarity = points @ points.T
    np.fill_diagonal(similarity, -np.inf)
    neighbours = np.argsort(similarity, axis=1)[:, ::-1][:, :3]

    # a query that lives inside cluster 2
    q = centres[2] + np.array([0.2, -0.3])
    q = q / np.linalg.norm(q)

    truth = points @ q
    best = int(np.argmax(truth))

    # the search: hop to the neighbour most like q, stop when nothing improves
    current, seen = 0, [0]
    for _ in range(N):
        hop = int(neighbours[current][np.argmax(points[neighbours[current]] @ q)])
        if hop in seen or points[hop] @ q <= points[current] @ q:
            break
        seen.append(hop)
        current = hop

    print(f"{N} vectors, in three clusters. Each vector keeps links to its 3 best")
    print("neighbours. The query sits inside cluster 2.\n")
    print(f"{'vector':>8} {'cluster':>9}   similarity to query")
    for _v in seen:
        print(f"{_v:>8,d} {cluster[_v]:>9,d}         {truth[_v]:.3f}")
    print(f"-- stop: no link improves on {points[current] @ q:.3f}.\n")
    print(f"vectors examined: {len(seen)} of {N:,}")
    print(f"checking everyone instead: best is vector {best}, cluster {cluster[best]}, score {truth[best]:.3f}")
    return


@app.cell
def _(mo):
    mo.md(r"""
    Four hops, less than a tenth of the data, and it landed in the right
    cluster with a score close to the true best. Sometimes it lands a slot off
    the exact answer. That's the whole trade: a pinch of accuracy for a lot of
    speed.

    ## 5 · HNSW: the real one

    Real vector databases run **HNSW** — Hierarchical Navigable Small World.
    It's the graph idea above plus two upgrades:

    - **layers** — several copies of the graph, stacked. The top layer has
      fewer, longer links — the motorway. Lower layers have more, shorter
      links — the streets. A query enters on the motorway, travels far fast,
      and drops down to a lower layer to home in on the street.
    - **a dial** — the algorithm peeks at `k` candidates, then `2k`, then `4k`
      ... Its "how hard do I look" knob is called `ef`. Peek more: slower and
      nearer-perfect. Peek less: fast and quietly wrong sometimes.

    You will never write HNSW yourself. Pinecone runs one for you, and
    LangChain hides whichever store you pick behind the same three calls —
    `add_documents`, `similarity_search`, `as_retriever`. That's the whole plot
    of the next lesson.

    | term | meaning |
    |---|---|
    | KNN | exact, O(N), correct until it's too slow |
    | ANN | the family of approximate methods — what everyone uses |
    | HNSW | the specific one inside Pinecone, FAISS, Chroma, and friends |

    One consequence worth keeping: your retrieval can be slightly wrong for
    reasons that have nothing to do with your embeddings or your prompt.

    ---
    **Next: `10_vector_store.py`** — the same idea, on a server, wrapped by
    LangChain.
    """)
    return


if __name__ == "__main__":
    app.run()
