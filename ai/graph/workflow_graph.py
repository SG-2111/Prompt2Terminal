from langgraph.graph import StateGraph, END

from agents.planner import generate_workflow
from agents.safety import analyze_risk


class State(dict):
    pass


def planner_node(state):
    workflow = generate_workflow(state["goal"])
    return {"workflow": workflow}


def safety_node(state):
    safety = analyze_risk(state["workflow"])
    return {"safety": safety}


def route(state):
    if state["safety"]["blocked"]:
        return END
    return END


graph = StateGraph(State)

graph.add_node("planner", planner_node)
graph.add_node("safety", safety_node)

graph.set_entry_point("planner")
graph.add_edge("planner", "safety")
graph.add_conditional_edges("safety", route)

app = graph.compile()