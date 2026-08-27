from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from .engine import Engine

engine = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global engine
    engine = Engine("/app/yaneuraou")
    yield
    engine.close()

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/checkmate_in_one_answers")
def get_checkmate_in_one_answers(sfen: str, solution, n: int = 4, depth: int = 1):
    try:
        return engine.get_alternatives(sfen, solution, n, depth)
    except (BrokenPipeError, RuntimeError):
        raise HTTPException(
            status_code=503,
            detail="Engine unavailable"
        )