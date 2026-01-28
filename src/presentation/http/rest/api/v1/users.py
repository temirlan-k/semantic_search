from fastapi import APIRouter
from src.domain.exceptions.users import UserNotFoundException


users_router = APIRouter()

@users_router.get("/me")
async def get_user(user_id: int):
    if user_id != 1:
        raise UserNotFoundException(f"User with id {user_id} not found")
    return {"user_id": user_id, "username": "testuser"}

