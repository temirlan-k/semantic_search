from pydantic import Field
from src.presentation.http.rest.api.v1.schemas import BaseSchema


class UserRegisterResponse(BaseSchema):
    message: str
    user_id: int


class UserLoginResponse(BaseSchema):
    access_token: str
    token_type: str = Field(default="Bearer")
    expires_in: int


class UserMeResponse(BaseSchema):
    user_id: int
    username: str
