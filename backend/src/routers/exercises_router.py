from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src.database.session import get_session
from src.services.exercise_service import ExerciseService
from src.schemas.exercises import ExerciseResponse

router = APIRouter(
    prefix="/exercises",
)

@router.post("/checkmate-in-one", status_code=status.HTTP_201_CREATED)
def generate_checkmate_in_one(session: Session = Depends(get_session)):
    service = ExerciseService(session)

    exercises = service.generate_checkmate_in_one()

    return {
        "message": "Exercises generated successfully",
        "count": len(exercises)
    }

@router.post("/fetch-games",status_code=status.HTTP_201_CREATED)
def fetch_games(session: Session = Depends(get_session)):
    service = ExerciseService(session)

    count = service.fetch_games()

    return {
        "message": "Games fetched successfully",
        "count": count
    }


@router.get("/random", response_model=ExerciseResponse)
def get_random_exercise(session: Session = Depends(get_session)):
    service = ExerciseService(session)

    exercise = service.get_random_exercise()

    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No exercises available"
        )

    return exercise 


@router.get("/list", response_model=list[ExerciseResponse])
def get_exercise_list(
    user_id: int,
    session: Session = Depends(get_session),
):
    service = ExerciseService(session)

    exercises = service.get_exercise_list(user_id)
    print("Exercise fetched")
    if exercises is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User status not found",
        )

    return exercises


@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise_by_id(exercise_id: int, session: Session = Depends(get_session)):
    service = ExerciseService(session)

    exercise = service.get_exercise_by_id(exercise_id)

    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found"
        )

    return exercise



# @router.get("/exercises/checkmate_in_one/{id}")
# def get_checkmate_in_one(id: int):
#     exercise = ex_gen.exercises_repo.get_by_id(id)
#     return {"response": exercise}

# @router.get("/exercises/checkmate_in_one")
# def get_random_checkmate_in_one():
#     exercise = ex_gen.exercises_repo.get_random()
#     return {"response": exercise}

# @router.get("/exercises/exercise_list")
# def get_exercises_list():
#     ex_list = ex_gen.exercises_repo.get_exercises_list(user["modules_probs"])
#     return {"response": ex_list}


# @router.post("/exercises/fetch_games")
# def generate_games():
#     ex_gen.insert_games()
#     return {"response": "games inserted!"}