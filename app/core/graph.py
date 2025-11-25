from langgraph.graph import StateGraph, END
from app.core.state import AgentState
from app.core import agent
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def create_agent_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("fetch_serp", agent.fetch_serp_node)
    workflow.add_node("analyze", agent.analyze_serp_node)
    workflow.add_node("create_outline", agent.create_outline_node)
    workflow.add_node("generate", agent.generate_content_node)
    workflow.add_node("metadata", agent.generate_metadata_node)
    workflow.add_node("links", agent.generate_links_node)
    workflow.add_node("validate", agent.validate_node)
    
    workflow.set_entry_point("fetch_serp")
    workflow.add_edge("fetch_serp", "analyze")
    workflow.add_edge("analyze", "create_outline")
    workflow.add_edge("create_outline", "generate")
    workflow.add_edge("generate", "metadata")
    workflow.add_edge("metadata", "links")
    workflow.add_edge("links", "validate")
    workflow.add_edge("validate", END)
    
    logger.info("LangGraph checkpointing disabled (SQLite not thread-safe with async)")
    
    return workflow.compile()


_agent_graph = None

def get_agent_graph():
    global _agent_graph
    if _agent_graph is None:
        _agent_graph = create_agent_graph()
    return _agent_graph

