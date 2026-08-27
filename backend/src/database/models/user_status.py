from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, ForeignKey, Float, func
from sqlalchemy.dialects.postgresql import JSONB


from src.database.connection import Base

class UserStatus(Base):
    __tablename__ = "user_status"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    current_module: Mapped[str] = mapped_column(String(50), nullable=False, default="recon")
    module_progress: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    modules_probs: Mapped[dict] = mapped_column(JSONB, nullable=False, default={"recon": 1.0,
                                                                                "movement": 0.0,
                                                                                "drop": 0.0,
                                                                                "mate": 0.0,
                                                                                "promotion": 0.0,
                                                                                "checkmate-in-one": 0.0,
                                                                                })
    recent_performances: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())