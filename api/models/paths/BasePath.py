from urllib.parse import unquote
from pydantic import BaseModel, validator

class BasePath(BaseModel):
    @validator('*', pre=True)
    def unescapeQueryString(cls, value):
        if isinstance(value, str):
            return unquote(value)

        return value
