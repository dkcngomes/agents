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
    # 04 · Tools, and the Loop That Makes an Agent

    A Roomba senses, decides, acts, and repeats until the room is clean. A bare
    model does none of that — it has no senses, no actions, and no loop. It
    reads text and writes text, once.

    This notebook gives it the missing three, one at a time. Watch the
    `CALLS` counter below — it's the whole first half of the lesson.
    """)
    return


@app.cell
def _():
    from langchain.messages import HumanMessage, SystemMessage
    from langgraph.prebuilt import ToolNode
    from langgraph.runtime import CONF, CONFIG_KEY_RUNTIME, DEFAULT_RUNTIME
    from langchain.tools import tool

    from config import chat_model
    from weather import FORECAST_URL, TIMEZONE, geocode
    from send_mobile_notify import send_notification

    model = chat_model()
    CALLS = []
    return (
        CONF,
        CONFIG_KEY_RUNTIME,
        DEFAULT_RUNTIME,
        CALLS,
        FORECAST_URL,
        HumanMessage,
        SystemMessage,
        TIMEZONE,
        ToolNode,
        geocode,
        model,
        tool,
        send_notification,
    )


@app.cell
def _(mo):
    mo.md(r"""
    ## 1 · A tool is just a function

    `@tool` turns an ordinary Python function into something a model can be
    told about. Its body is a real HTTP request to open-meteo.com — a free
    weather API with no key and no account. Nothing about it is a stub.
    """)
    return


@app.cell
def _(CALLS, FORECAST_URL, TIMEZONE, geocode, tool):
    import requests

    @tool
    def get_rainfall(district: str) -> str:
        """Get the rainfall in the last 7 days for a Sri Lankan district, in mm."""
        CALLS.append(district)
        print(f"   >>> get_rainfall RAN (call {len(CALLS)}) district={district!r}")

        lat, lon, name = geocode(district)
        daily = requests.get(
            FORECAST_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "daily": "precipitation_sum",
                "timezone": TIMEZONE,
                "past_days": 7,
                "forecast_days": 1,
            },
            timeout=20,
        ).json()["daily"]

        # The response covers the last seven days plus today. Today is still in
        # progress, so drop it.
        week = daily["precipitation_sum"][:7]
        rainy = sum(1 for mm in week if mm >= 1.0)

        return f"{name}: {sum(week):.1f} mm over the last 7 days, {rainy} rainy days."

    return (get_rainfall,)


@app.cell
def _(get_rainfall):
    print("name        :", get_rainfall.name)
    print("description :", get_rainfall.description)
    print("args        :", get_rainfall.args)
    return


@app.cell
def _(mo):
    mo.md(r"""
    The name came from the function. The description came from the docstring.
    The argument schema came from the type hints.

    That description is not documentation — it's the **only** thing the model
    reads when deciding whether this tool is worth calling. It is a prompt.

    ## 2 · Tell the model the tool exists

    `bind_tools` attaches the schema to the model. Then ask a question that
    needs it.
    """)
    return


@app.cell
def _(CALLS, HumanMessage, SystemMessage, get_rainfall, model):
    model_with_tools = model.bind_tools([get_rainfall])

    messages = [
        SystemMessage("You are an advisor for Sri Lankan paddy farmers."),
        HumanMessage("How much rain has Gampaha district had this week?"),
    ]

    CALLS.clear()
    reply = model_with_tools.invoke(messages)

    print("type            :", type(reply).__name__)
    print("reply.text      :", repr(reply.text))
    print("reply.tool_calls:")
    for _tc in reply.tool_calls:
        print("   ", _tc)
    print()
    print("CALLS =", len(CALLS), "   <-- read this number")
    return messages, model_with_tools, reply


@app.cell
def _(mo):
    mo.md(r"""
    **Stop. Nothing ran.**

    `reply.text` is empty — there is no answer, because it did not answer your
    question. And `CALLS` is 0: `get_rainfall` never executed.

    The model is a text service on a server somewhere else. It has no access to
    this process, your variables, or your network. It cannot run your function,
    because it cannot run *anything* at all.

    What it produced is a **request**: a name, some arguments, and an id.
    Addressed to you. If your code ignores it, nothing happens, ever.

    ## 3 · Something has to execute it — that's what a ToolNode is

    A `ToolNode` holds your tools. You hand it the conversation; it finds the
    tool calls on the last message, looks each one up by name, runs it with the
    arguments, and hands back a `ToolMessage` per call.

    ```python
    tool_node = ToolNode([get_rainfall])
    tool_node.invoke(messages)
    ```
    """)
    return


@app.cell
def _(CALLS, CONF, CONFIG_KEY_RUNTIME, DEFAULT_RUNTIME, ToolNode, get_rainfall, messages, reply):
    tool_node = ToolNode([get_rainfall])

    # ToolNode normally runs inside a graph, and the graph gives it a "runtime" —
    # the object tools use to reach shared state and context. We're calling it on
    # its own, so there is no graph to inherit one from. Hand it the default and
    # it behaves exactly the same.
    NO_GRAPH = {CONF: {CONFIG_KEY_RUNTIME: DEFAULT_RUNTIME}}

    CALLS.clear()
    observations = tool_node.invoke(messages + [reply], config=NO_GRAPH)

    print("CALLS =", len(CALLS), "   <-- now it ran")
    print()
    print("it returned a", type(observations).__name__, "of", len(observations), "message(s):")
    for _m in observations:
        print(f"   {type(_m).__name__:14s} {_m.content[:60]!r}")
    return (observations,)


@app.cell
def _(observations, send_notification):
    observation = observations[0]
    print("the ToolMessage it produced:")
    print("   content      :", observation.content)
    print("   name         :", observation.name)
    print("   tool_call_id :", observation.tool_call_id, " <- matches the request id")

    send_notification(observation.content)  # send the result to your phone
    print(" >>> Sent the result to your phone via ntfy.sh")
    return


@app.cell
def _(mo):
    mo.md(r"""
    One message in with a tool call on it, one message out with the answer on
    it. No graph, no state schema, no wiring — that's the whole executor.

    ## 4 · Feed it back and the model can finally answer

    The conversation is still just a list, and you're still the one appending
    to it: the question, what the model asked for, and what your function
    returned.
    """)
    return


@app.cell
def _(messages, observations, reply):
    conversation = messages + [reply] + observations

    for _m in conversation:
        print(f"   {type(_m).__name__:14s} {_m.text[:56]!r}")
    return (conversation,)


@app.cell
def _(conversation, model_with_tools):
    final = model_with_tools.invoke(conversation)
    print(final.text)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## That was ReAct

    ```
    REASON    the model decided it needed rainfall      -> AIMessage.tool_calls
    ACT       the ToolNode ran your function            -> ToolMessage
    OBSERVE   you appended it and called again          -> model answers
    ```

    Repeat until it stops asking. That loop is the entire idea of an agent, and
    you've now seen every piece of it as a real object.

    The Roomba senses the floor, decides, moves, and looks again. Same shape.
    The tools are its senses and its hands.

    You ran that loop once, by hand, in about four lines.

    ---
    **Next: `05_agent_calculator.py`** — you stop writing the loop
    yourself.
    """)
    return


if __name__ == "__main__":
    app.run()