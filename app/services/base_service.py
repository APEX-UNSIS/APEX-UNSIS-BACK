from typing import Generic, TypeVar, List, Optional
from app.repositories.base_repository import BaseRepository

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    def get(self, id: str) -> Optional[ModelType]:
        return self.repository.get_by_id(id)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return self.repository.get_all(skip, limit)

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        return self.repository.create(obj_in)

    def update(self, id: str, obj_in: UpdateSchemaType) -> Optional[ModelType]:
        return self.repository.update(id, obj_in)

    def delete(self, id: str) -> Optional[ModelType]:
        return self.repository.delete(id)

    def count(self) -> int:
        return self.repository.count()