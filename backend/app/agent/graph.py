from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

class CuraState(TypedDict):
    query: str
    role: str
    intent: Optional[str]
    agent_output: Optional[str]

def triage_node(state: CuraState) -> dict:
    query = state["query"].lower()
    emergency_flags = ["chest pain", "can't breathe", "stroke", "unconscious"]

    if any(word in query for word in emergency_flags):
        return {
            "intent": "EMERGENCY",
            "agent_output": "EMERGENCY DETECTED: Call emergency services (112 or local emergency care) immediately."
        }
    if any(word in query for word in ["pill", "medicine", "dosage"]):
        return {"intent": "MEDICATION"}
    return {"intent": "GENERAL"}

def response_node(state: CuraState) -> dict:
    if state.get("intent") == "EMERGENCY":
        return state

    output = (
        f"[Cura Health Assistant] Processing inquiry under role '{state.get('role', 'PATIENT')}': "
        f"'{state['query']}'. (Track B Health Monitoring Agent Active)\n\n"
        "Disclaimer: Cura provides wellness insights and does not replace professional medical diagnosis."
    )
    return {"agent_output": output}

def route_flow(state: CuraState) -> str:
    if state.get("intent") == "EMERGENCY":
        return END
    return "generate_response"

builder = StateGraph(CuraState)
builder.add_node("triage", triage_node)
builder.add_node("generate_response", response_node)

builder.set_entry_point("triage")
builder.add_conditional_edges("triage", route_flow, {
    END: END,
    "generate_response": "generate_response"
})
builder.add_edge("generate_response", END)

cura_agent = builder.compile()