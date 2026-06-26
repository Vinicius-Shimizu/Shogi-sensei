from fastapi import FastAPI
from src.exercise_generator import ExerciseGenerator

app = FastAPI()


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ex_gen = ExerciseGenerator("/yaneuraou/yaneuraou")

@app.get("/exercises/checkmate_in_one")
def get_checkmate_in_one():
    response = ex_gen.checkmate_in_one()
    return {"response": response}

@app.post("/exercises/fetch_games")
def get_games():
    ex_gen.insert_games()
    return {"response": "games inserted!"}