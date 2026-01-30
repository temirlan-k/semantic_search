from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from src.presentation.http.rest.api.v1.deps import get_current_user_id
from src.presentation.http.rest.api.v1.schemas.req.users import UserAuthRequest
from src.presentation.http.rest.api.v1.schemas.res.users import (
    UserLoginResponse,
    UserMeResponse,
    UserRegisterResponse,
)
from src.application.use_cases.user.user import UserUseCase
from main.di.container import Container

users_router = APIRouter()


@users_router.post("/register", response_model=UserRegisterResponse)
@inject
async def create_user(
    data: UserAuthRequest,
    user_use_case: UserUseCase = Depends(Provide[Container.user_use_case]),
):
    result = await user_use_case.register_user(request=data.model_dump())
    return result


@users_router.post("/login", response_model=UserLoginResponse)
@inject
async def login_user(
    data: UserAuthRequest,
    user_use_case: UserUseCase = Depends(Provide[Container.user_use_case]),
):
    result = await user_use_case.authenticate_user(request=data.model_dump())
    return result


@users_router.post("/me", response_model=UserMeResponse)
@inject
async def me(
    current_user_id: int = Depends(get_current_user_id),
    user_use_case: UserUseCase = Depends(Provide[Container.user_use_case]),
):
    result = await user_use_case.get_user(user_id=current_user_id)
    return result
