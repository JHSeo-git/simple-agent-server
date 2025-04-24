from langgraph.graph import END, START, StateGraph

from .nodes import assistant_node
from .types import State


def create_graph():
    builder = StateGraph(State)

    builder.add_edge(START, "assistant")
    builder.add_node("assistant", assistant_node)
    builder.add_edge("assistant", END)

    return builder.compile()
