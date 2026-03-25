# Skill model — multi-language skill taxonomy with aliases and stats.
from sqlalchemy import Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)  # e.g. "langchain"
    canonical_name: Mapped[str] = mapped_column(String(100))  # e.g. "LangChain"
    category: Mapped[str] = mapped_column(
        String(50)
    )  # "framework" | "concept" | "language" | "tool" | "cloud"
    subcategory: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # [{"name": "langchain", "lang": "en"}, {"name": "朗链", "lang": "zh"}]
    aliases: Mapped[list | None] = mapped_column(JSONB, nullable=True)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Aggregated stats (updated periodically)
    domestic_count: Mapped[int] = mapped_column(Integer, default=0)
    international_count: Mapped[int] = mapped_column(Integer, default=0)
    total_count: Mapped[int] = mapped_column(Integer, default=0)
    avg_salary_with: Mapped[int | None] = mapped_column(Integer, nullable=True)
