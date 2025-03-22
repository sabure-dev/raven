from sqlalchemy import ForeignKey, CheckConstraint, Float

from db.session.base import Base

from sqlalchemy.orm import mapped_column, Mapped, relationship

from schemas.sneaker_model.sneaker_model import SneakerModelOut
from schemas.sneaker_variant.sneaker_variant import SneakerVariantOut


class SneakerModel(Base):
    __tablename__ = 'sneaker_models'
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(unique=True)
    brand: Mapped[str] = mapped_column(index=True)
    type: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column(Float(precision=4), CheckConstraint('price >= 0'), default=0)

    variants: Mapped[list["SneakerVariant"]] = relationship("SneakerVariant", back_populates="model")

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

    model_id: Mapped[int] = mapped_column(ForeignKey('sneaker_models.id'), index=True)
    size: Mapped[float] = mapped_column(index=True)
    quantity: Mapped[int] = mapped_column(CheckConstraint('quantity >= 0'), default=0)

    model: Mapped["SneakerModel"] = relationship("SneakerModel", back_populates="variants")

    def to_read_model(self) -> SneakerVariantOut:
        return SneakerVariantOut(
            id=self.id,

            model_id=self.model_id,
            size=self.size,
            quantity=self.quantity,
        )
