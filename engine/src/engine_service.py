from fastapi import FastAPI
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

@app.get("/analyze")
def analyze_play(move: str):
    return move
