import json
from pydantic import BaseModel

class BaseModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BaseModel):
            return obj.dict()

        return super().default(obj)
