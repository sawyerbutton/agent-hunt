# Platform metadata model — each recruitment platform as a first-class entity.
import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Platform(Base):
    __tablename__ = "platforms"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)  # e.g. "boss_zhipin"
    name: Mapped[str] = mapped_column(String(100))  # e.g. "Boss直聘"
    market: Mapped[str] = mapped_column(String(20))  # "domestic" | "international" | "both"
    url: Mapped[str] = mapped_column(String(255))
    language: Mapped[str] = mapped_column(String(10))  # "zh" | "en" | "both"
    tier: Mapped[int] = mapped_column(Integer)  # 1, 2, 3
    scrape_difficulty: Mapped[int] = mapped_column(Integer)  # 1-5
    data_quality: Mapped[str] = mapped_column(String(10))  # "high" | "medium" | "low"
    refresh_rate: Mapped[str] = mapped_column(String(20))  # "realtime" | "daily" | "weekly"
    has_salary_data: Mapped[bool] = mapped_column(Boolean, default=True)
    has_company_size: Mapped[bool] = mapped_column(Boolean, default=False)
    collector_class: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    last_collected_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
