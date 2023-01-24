from typing import Generic, TypeVar
from pydantic.generics import GenericModel

T = TypeVar('T')

class List(GenericModel, Generic[T]):
    __root__: list[T]
