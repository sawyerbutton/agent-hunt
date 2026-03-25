# Re-export all models so Alembic can discover them.
from app.models.job import Job
from app.models.platform import Platform
from app.models.skill import Skill

__all__ = ["Platform", "Job", "Skill"]
