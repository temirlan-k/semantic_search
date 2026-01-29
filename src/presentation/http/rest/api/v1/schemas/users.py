
from pydantic import Field, UUID4
from src.presentation.http.rest.api.v1.schemas.base import BaseSchema

class UserAuthRequest(BaseSchema):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)


class UserRegisterResponse(BaseSchema):
    message: str
    user_id: str


class UserLoginResponse(BaseSchema):
    access_token: str
    token_type: str = Field(default="Bearer")
    expires_in: int


class GetUserRequest(BaseSchema):
    user_id: int
    