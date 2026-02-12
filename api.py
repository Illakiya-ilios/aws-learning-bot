from fastapi import FastAPI
from pydantic import BaseModel
from orchestrator import Orchestrator

app = FastAPI()
orch = Orchestrator()

class StartReq(BaseModel):
    user_id: str
    certification: str

class TeachReq(BaseModel):
    user_id: str

class ScoreReq(BaseModel):
    user_id: str
    score: int


@app.post("/start")
def start(req: StartReq):
    return orch.start(req.user_id, req.certification)


@app.post("/teach")
def teach(req: TeachReq):
    return {"lesson": orch.teach(req.user_id)}


@app.post("/assess")
def assess(req: TeachReq):
    return {"quiz": orch.assess(req.user_id)}


@app.post("/submit-score")
def submit_score(req: ScoreReq):
    return orch.submit_score(req.user_id, req.score)


@app.get("/progress/{user_id}")
def progress(user_id: str):
    return orch.get_progress(user_id)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting AWS Agentic Learning API...")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
