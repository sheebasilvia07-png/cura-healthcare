from fastapi import FastAPI
from pydantic import BaseModel
from app.db.database import init_db
from app.agent.graph import cura_agent

app = FastAPI(
    title="Cura AI Health Agent API",
    version="1.0.0",
    description="Track B Platform: Health data monitoring, role-based workflows, and agentic assistant."
)

@app.on_event("startup")
def on_startup():
    init_db()

class QueryRequest(BaseModel):
    query: str
    role: str = "PATIENT"

@app.get("/health")
def health_check():
    return {"status": "healthy", "platform": "Cura Health Agent"}

@app.post("/api/v1/chat")
def chat_with_cura(req: QueryRequest):
    result = cura_agent.invoke({
        "query": req.query,
        "role": req.role,
        "intent": None,
        "agent_output": None
    })
    return {"response": result.get("agent_output"), "intent": result.get("intent")}