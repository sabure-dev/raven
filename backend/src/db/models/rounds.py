from datetime import datetime, timedelta

from sqlalchemy import Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.session.base import Base
from schemas.rounds.rounds import RoundStatus


class Round(Base):
    __tablename__ = 'rounds'

    id: Mapped[int] = mapped_column(primary_key=True)

    status: Mapped[RoundStatus] = mapped_column(Enum(RoundStatus), default=RoundStatus.PLANNED)
    winner_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'), nullable=True, default=None)
    model_id: Mapped[int] = mapped_column(ForeignKey("sneaker_models.id", ondelete="CASCADE"), index=True)

    planned_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now() + timedelta(days=1)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    closed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    bets: Mapped[list["Bet"]] = relationship(
        "Bet",
        back_populates="round",
        lazy="raise",
        cascade="all, delete-orphan"
    )
    model: Mapped["SneakerModel"] = relationship(
        "SneakerModel",
        back_populates="variants",
        lazy="raise"
    )
