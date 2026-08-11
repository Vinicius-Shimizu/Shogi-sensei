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

@app.post("/exercises/checkmate_in_one")
def generate_checkmate_in_one():
    ex_gen.checkmate_in_one()
    return {"response": "checkmate exercise generated succesfully!"}

@app.get("/exercises/checkmate_in_one/{id}")
def get_checkmate_in_one(id: int):
    exercise = ex_gen.exercises_repo.get_by_id(id)
    return {"response": exercise}

@app.get("/exercises/checkmate_in_one")
def get_random_checkmate_in_one():
    exercise = ex_gen.exercises_repo.get_random()
    return {"response": exercise}

@app.get("/exercises/exercise_list")
def get_exercises_list():
    ex_list = ex_gen.exercises_repo.get_exercises_list()
    return {"response": ex_list}


@app.post("/exercises/fetch_games")
def generate_games():
    ex_gen.insert_games()
    return {"response": "games inserted!"}

