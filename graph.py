from langgraph.graph import StateGraph, END

from state import ResearchState

from agents.pdf_agent import pdf_agent
from agents.summary_agent import summary_agent
from agents.qa_agent import qa_agent
from agents.keyword_agent import keyword_agent
from agents.evaluation_agent import evaluation_agent

builder = StateGraph(ResearchState)

builder.add_node("pdf", pdf_agent)
builder.add_node("summary_node", summary_agent)
builder.add_node("qa_node", qa_agent)
builder.add_node("keywords_node", keyword_agent)
builder.add_node("evaluation_node", evaluation_agent)


def router(state: ResearchState):
    action = state["action"]

    if action == "summary":
        return "summary_node"

    elif action == "qa":
        return "qa_node"

    elif action == "keywords":
        return "keywords_node"

    return END


builder.set_entry_point("pdf")

builder.add_conditional_edges(
    "pdf",
    router,
    {
        "summary_node": "summary_node",
        "qa_node": "qa_node",
        "keywords_node": "keywords_node",
    },
)

builder.add_edge("summary_node", "evaluation_node")
builder.add_edge("qa_node", "evaluation_node")
builder.add_edge("keywords_node", "evaluation_node")
builder.add_edge("evaluation_node", END)

graph = builder.compile()