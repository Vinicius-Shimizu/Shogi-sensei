from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.session import get_session
from src.schemas.user import UserCreate, UserResponse, UserStatusResponse
from src.services.user_service import UserService, UserRepository, UserStatusRepository

router = APIRouter(
    prefix="/users"
)

@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    service = UserService(session)

    try:
        return service.create_user(user_data.username)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    user_repo = UserRepository(session)

    user = user_repo.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user

@router.get(
    "/{user_id}/status",
    response_model=UserStatusResponse
)
def get_user_status(
    user_id: int,
    session: Session = Depends(get_session)
):
    user_repo = UserRepository(session)
    status_repo = UserStatusRepository(session)

    user = user_repo.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user_status = status_repo.get_by_id(user_id)

    if user_status is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User status not found"
        )

    return user_status