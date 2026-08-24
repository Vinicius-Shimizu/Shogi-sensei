from fastapi import FastAPI
from src.exercise_generator import ExerciseGenerator
import yaml
from pydantic import BaseModel

class UserProgress(BaseModel):
    lesson_score: float

app = FastAPI()

with open("/app/src/user.yml", "r") as f:
    user = yaml.safe_load(f)

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
    ex_list = ex_gen.exercises_repo.get_exercises_list(user["modules_probs"])
    return {"response": ex_list}


@app.post("/exercises/fetch_games")
def generate_games():
    ex_gen.insert_games()
    return {"response": "games inserted!"}

@app.put("/exercises/update_user_progress")
def update_user_progress(progress: UserProgress):
    user["module_progress"] = progress.lesson_score
    print(user)
    try:
        with open("/app/src/user.yml", "w") as f:
            yaml.safe_dump(user, f, default_flow_style=False, allow_unicode=True)
        return {"message": "Progress updated successfully"}
    except Exception as e:
        return {"message": f"Progress could not be updated: {e}"}