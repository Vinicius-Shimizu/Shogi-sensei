from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from src.database.session import get_session
from src.services.exercise_service import ExerciseService
from src.schemas.exercises import ExerciseResponse, ExerciseListResult, ExerciseListSubmission
from src.schemas.user import UserResponse
from src.auth.dependencies import get_current_user

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

@router.post("/recon", status_code=status.HTTP_201_CREATED)
def generate_recon(session: Session = Depends(get_session)):
    service = ExerciseService(session)

    exercises = service.generate_recon()

    return {
        "message": "Exercises generated successfully",
        "count": len(exercises)
    }

@router.post("/movement1", status_code=status.HTTP_201_CREATED)
def generate_movement1(session: Session = Depends(get_session)):
    service = ExerciseService(session)
    exercises = service.generate_movement1()

    return {
        "message": "Exercises generated successfully",
        "count": len(exercises)
    }

@router.post("/movement2", status_code=status.HTTP_201_CREATED)
def generate_movement2(session: Session = Depends(get_session)):
    service = ExerciseService(session)
    exercises = service.generate_movement2()

    return {
        "message": "Exercises generated successfully",
        "count": len(exercises)
    }

@router.post("/promotion", status_code=status.HTTP_201_CREATED)
def generate_promotion(session: Session = Depends(get_session)):
    service = ExerciseService(session)
    exercises = service.generate_promotion()
    return {
        "message": "Exercises generated successfully",
        "count": len(exercises)
    }

@router.post("/drop", status_code=status.HTTP_201_CREATED)
def generate_promotion(session: Session = Depends(get_session)):
    service = ExerciseService(session)
    exercises = service.generate_drop()
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


@router.post("/submit", response_model=ExerciseListResult)
def submit_answers(submission: ExerciseListSubmission, current_user: Annotated[UserResponse, Depends(get_current_user)], session: Session = Depends(get_session)):
    service = ExerciseService(session)
    user_id = current_user.id
    result = service.submit_answers(user_id, submission.answers)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No valid answers submitted"
        )

    return result


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
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    session: Session = Depends(get_session),

):
    service = ExerciseService(session)
    user_id = current_user.id
    print("USER ID", user_id)
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