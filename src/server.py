from fastapi import FastAPI
from src.exercise_generator import ExerciseGenerator

app = FastAPI(port=8080)

ex_gen = ExerciseGenerator("/yaneuraou/yaneuraou")

@app.get("/exercises/checkmate_in_one")
def get_checkmate_in_one():
    response = ex_gen.checkmate_in_one()
    return {"response": response}