from fastapi import APIRouter, Depends
from src.presentation.http.rest.api.deps import get_current_user_id
from src.application.use_cases.user.get_user import UserUseCase
from dependency_injector.wiring import inject, Provide
from main.di.container import Container
from src.presentation.http.rest.api.v1.schemas.users import UserAuthRequest

users_router = APIRouter()


@users_router.get("/me")
@inject
async def get_user(
    user_id: str,
    current_user_id: int = Depends(get_current_user_id),
    get_user_use_case: UserUseCase = Depends(Provide[Container.user_use_case]),
):
    user = await get_user_use_case.get_user(user_id)
    print(current_user_id)
    return {"user": user}


@users_router.post("/")
@inject
async def create_user(
    data: UserAuthRequest,
    create_user_use_case: UserUseCase = Depends(Provide[Container.user_use_case]),
):
    user = await create_user_use_case.create_user(data=data.model_dump())
    return {"user": user}
