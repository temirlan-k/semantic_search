from fastapi import APIRouter, Depends
from src.presentation.http.rest.api.deps import get_current_user_id
from src.application.use_cases.user.user import UserUseCase
from dependency_injector.wiring import inject, Provide
from main.di.container import Container
from src.presentation.http.rest.api.v1.schemas.users import UserAuthRequest

users_router = APIRouter()


@users_router.post("/register")
@inject
async def create_user(
    data: UserAuthRequest,
    user_use_case: UserUseCase = Depends(Provide[Container.user_use_case]),
):
    result = await user_use_case.register_user(request=data)
    return result


@users_router.post("/login")
@inject
async def login_user(
    data: UserAuthRequest,
    user_use_case: UserUseCase = Depends(Provide[Container.user_use_case]),
):
    result = await user_use_case.authenticate_user(request=data)
    return result


@users_router.post("/me")
@inject
async def me(
    current_user_id: int = Depends(get_current_user_id),
    user_use_case: UserUseCase = Depends(Provide[Container.user_use_case]),
):
    result = await user_use_case.get_user(user_id=current_user_id)
    return result
