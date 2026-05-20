from langgraph.graph import StateGraph, END
from app.graph.state import GraphState
from app.graph.nodes import (
    pii_node,
    rag_node,
    optimize_node,
    verify_node,
    pdf_node
)


def build_graph():
    graph = StateGraph(GraphState)

    # Add nodes
    graph.add_node("pii", pii_node)
    graph.add_node("rag", rag_node)
    graph.add_node("optimize", optimize_node)
    graph.add_node("verify", verify_node)
    graph.add_node("pdf", pdf_node)

    # Edges
    graph.set_entry_point("pii")
    graph.add_edge("pii", "rag")
    graph.add_edge("rag", "optimize")
    graph.add_edge("optimize", "verify")
    graph.add_edge("verify", "pdf")
    graph.add_edge("pdf", END)

    return graph.compile()
