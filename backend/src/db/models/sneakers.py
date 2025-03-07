from sqlalchemy import ForeignKey, CheckConstraint, Float, Integer

from db.session.base import Base

from sqlalchemy.orm import mapped_column, Mapped

from schemas.sneaker_model import SneakerModelOut
from schemas.sneaker_variant import SneakerVariantOut


class SneakerModel(Base):
    __tablename__ = 'sneaker_models'
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column()
    brand: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column(Float(precision=4), CheckConstraint('price >= 0'), default=0)

    def to_read_model(self) -> SneakerModelOut:
        return SneakerModelOut(
            id=self.id,

            name=self.name,
            brand=self.brand,
            type=self.type,
            description=self.description,
            price=self.price,
        )


class SneakerVariant(Base):
    __tablename__ = 'sneaker_variants'
    id: Mapped[int] = mapped_column(primary_key=True)

    model_id: Mapped[int] = mapped_column(ForeignKey('sneaker_models.id'))
    size: Mapped[float] = mapped_column()
    quantity: Mapped[int] = mapped_column(Integer(), CheckConstraint('quantity >= 0'), default=0)

    def to_read_model(self) -> SneakerVariantOut:
        return SneakerVariantOut(
            id=self.id,

            model_id=self.model_id,
            size=self.size,
            quantity=self.quantity,
        )
