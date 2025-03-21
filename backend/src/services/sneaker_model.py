from typing import Callable

from core.utils.repository import AbstractRepository
from db.models.sneakers import SneakerModel
from schemas.sneaker_model import SneakerModelCreate
from core.exceptions import ItemAlreadyExistsException


class SneakerModelService:
    def __init__(self, sneaker_model_factory: Callable[[], AbstractRepository]):
        self.sneaker_model_repo = sneaker_model_factory()

    async def create_sneakers_model(self, sneaker_model: SneakerModelCreate) -> (int, SneakerModel):
        existing_sneaker_model = await self.sneaker_model_repo.find_one_by_field('name', sneaker_model.name)
        if existing_sneaker_model:
            raise ItemAlreadyExistsException('SneakerModel', 'name', existing_sneaker_model.name)

        sneaker_model_dict = sneaker_model.model_dump()
        sneaker_id = await self.sneaker_model_repo.create_one(sneaker_model_dict)

        created_sneaker_model = SneakerModel(**sneaker_model_dict)
        created_sneaker_model.id = sneaker_id

        return sneaker_id, created_sneaker_model
