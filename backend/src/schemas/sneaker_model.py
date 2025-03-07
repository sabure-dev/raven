from pydantic import BaseModel


class SneakerModelBase(BaseModel):
    name: str
    brand: str
    type: str
    description: str
    price: float


class SneakerModelCreate(SneakerModelBase):
    pass


class SneakerModelOut(SneakerModelBase):
    id: int
    