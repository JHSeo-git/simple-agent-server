from langgraph.graph import END, START, StateGraph

from .nodes import emoji_translate_node
from .types import State


def create_graph():
    builder = StateGraph(State)

    builder.add_edge(START, "emoji_translate")
    builder.add_node("emoji_translate", emoji_translate_node)
    builder.add_edge("emoji_translate", END)

    return builder.compile()
