from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.session.base import Base


class Bet(Base):
    __tablename__ = 'bets'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    round_id: Mapped[int] = mapped_column(ForeignKey('rounds.id', ondelete="CASCADE"), index=True)
    amount: Mapped[float]

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    is_winner: Mapped[bool] = mapped_column(default=False)

    user: Mapped["User"] = relationship(
        "User",
        back_populates="bets",
        lazy="raise"
    )
    round: Mapped["Round"] = relationship(
        "Round",
        back_populates="bets",
        lazy="raise"
    )

