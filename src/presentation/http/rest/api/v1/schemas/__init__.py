from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        anystr_strip_whitespace = True
        extra = "forbid"
        orm_mode = True
        use_enum_values = True
        validate_assignment = True
