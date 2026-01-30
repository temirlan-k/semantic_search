from pydantic import Field
from src.presentation.http.rest.api.v1.schemas import BaseSchema


class UserAuthRequest(BaseSchema):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
