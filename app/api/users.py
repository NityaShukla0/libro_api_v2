# app/api/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache

from app.crud.crud import create_user, get_user, get_users
from app.schemas.schemas import UserCreate, User
from app.db.session_manager import get_db_session
from app.config.settings import settings

router = APIRouter(prefix="/users", tags=["Users"])

# Dependency for feature flag
def users_enabled():
    if not settings.ENABLE_USERS:
        raise HTTPException(status_code=404, detail="User API is disabled")

@router.post("/", response_model=User, summary="Create a new user")
async def api_create_user(
    user: UserCreate,
    db: Session = Depends(get_db_session),
    _=Depends(users_enabled)
):
    """
    Create a new user in the system.
    """
    try:
        return create_user(db, user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=User, summary="Get user by ID")
async def api_get_user(
    user_id: int,
    db: Session = Depends(get_db_session),
    _=Depends(users_enabled)
):
    """
    Retrieve a user by their ID.
    """
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=list[User], summary="Get all users")
@cache(expire=settings.CACHE_EXPIRE if settings.ENABLE_CACHE else 0)
async def api_get_users(
    db: Session = Depends(get_db_session),
    _=Depends(users_enabled)
):
    """
    Retrieve all users.
    """
    return get_users(db)