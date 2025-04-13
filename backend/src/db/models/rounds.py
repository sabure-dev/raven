from datetime import datetime, timedelta

from sqlalchemy import Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.session.base import Base
from schemas.rounds.rounds import RoundStatus, RoundOut


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
        DateTime(timezone=True), nullable=True, default=None, onupdate=func.now()
    )

    bets: Mapped[list["Bet"]] = relationship(
        "Bet",
        back_populates="round",
        lazy="raise",
        cascade="all, delete-orphan"
    )
    model: Mapped["SneakerModel"] = relationship(
        "SneakerModel",
        lazy="joined",
    )

    def to_read_model(self, include_bets: bool = False) -> RoundOut:
        return RoundOut(
            id=self.id,
            status=self.status,
            winner_id=self.winner_id,
            model=self.model.to_read_model(),
            planned_time=self.planned_time,
            created_at=self.created_at,
            closed_at=self.closed_at,
            bets=[bet.to_read_model() for bet in self.bets]
            if include_bets and self.bets is not None
            else None,
        )
