"""Initial schema — platforms, jobs, skills tables.

Revision ID: 001
Revises: None
Create Date: 2026-03-25
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enable pgvector extension for future semantic search
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "platforms",
        sa.Column("id", sa.String(50), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("market", sa.String(20), nullable=False),
        sa.Column("url", sa.String(255), nullable=False),
        sa.Column("language", sa.String(10), nullable=False),
        sa.Column("tier", sa.Integer, nullable=False),
        sa.Column("scrape_difficulty", sa.Integer, nullable=False),
        sa.Column("data_quality", sa.String(10), nullable=False),
        sa.Column("refresh_rate", sa.String(20), nullable=False),
        sa.Column("has_salary_data", sa.Boolean, default=True),
        sa.Column("has_company_size", sa.Boolean, default=False),
        sa.Column("collector_class", sa.String(100), nullable=True),
        sa.Column("is_enabled", sa.Boolean, default=True),
        sa.Column("last_collected_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "jobs",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("platform_id", sa.String(50), sa.ForeignKey("platforms.id"), nullable=False, index=True),
        sa.Column("platform_job_id", sa.String(255), nullable=False),
        sa.Column("source_url", sa.String(1024), nullable=True),
        sa.Column("raw_content", sa.Text, nullable=False),
        sa.Column("language", sa.String(10), nullable=False),
        # Structured fields
        sa.Column("title", sa.String(255), nullable=True),
        sa.Column("company_name", sa.String(255), nullable=True),
        sa.Column("company_size", sa.String(20), nullable=True),
        sa.Column("location", sa.String(255), nullable=True),
        sa.Column("market", sa.String(20), nullable=True, index=True),
        sa.Column("work_mode", sa.String(10), nullable=True),
        sa.Column("salary_min", sa.Integer, nullable=True),
        sa.Column("salary_max", sa.Integer, nullable=True),
        sa.Column("salary_currency", sa.String(5), nullable=True),
        sa.Column("experience_min", sa.Integer, nullable=True),
        sa.Column("experience_max", sa.Integer, nullable=True),
        sa.Column("education", sa.String(20), nullable=True),
        sa.Column("required_skills", ARRAY(sa.String), nullable=True),
        sa.Column("preferred_skills", ARRAY(sa.String), nullable=True),
        sa.Column("responsibilities", ARRAY(sa.String), nullable=True),
        # Metadata
        sa.Column("collected_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("parsed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("parse_status", sa.String(20), nullable=False, server_default="pending"),
        # Dedup constraint
        sa.UniqueConstraint("platform_id", "platform_job_id", name="uq_job_platform_dedup"),
    )

    op.create_table(
        "skills",
        sa.Column("id", sa.String(100), primary_key=True),
        sa.Column("canonical_name", sa.String(100), nullable=False),
        sa.Column("category", sa.String(50), nullable=False),
        sa.Column("subcategory", sa.String(50), nullable=True),
        sa.Column("aliases", JSONB, nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("domestic_count", sa.Integer, server_default="0"),
        sa.Column("international_count", sa.Integer, server_default="0"),
        sa.Column("total_count", sa.Integer, server_default="0"),
        sa.Column("avg_salary_with", sa.Integer, nullable=True),
    )


def downgrade() -> None:
    op.drop_table("skills")
    op.drop_table("jobs")
    op.drop_table("platforms")
