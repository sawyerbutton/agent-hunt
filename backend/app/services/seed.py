# Load seed data (platforms + skills) into database on startup.
from __future__ import annotations

import json
import logging
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.platform import Platform
from app.models.skill import Skill

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"


async def seed_platforms(db: AsyncSession) -> None:
    """Insert platform records if they don't already exist."""
    path = DATA_DIR / "seed_platforms.json"
    if not path.exists():
        logger.warning("seed_platforms.json not found at %s", path)
        return

    platforms = json.loads(path.read_text(encoding="utf-8"))
    inserted = 0

    for p in platforms:
        existing = await db.execute(select(Platform.id).where(Platform.id == p["id"]))
        if existing.scalar_one_or_none() is not None:
            continue
        db.add(Platform(**p))
        inserted += 1

    if inserted:
        await db.commit()
        logger.info("Seeded %d platforms", inserted)


async def seed_skills(db: AsyncSession) -> None:
    """Insert skill records if they don't already exist."""
    path = DATA_DIR / "seed_skills.json"
    if not path.exists():
        logger.warning("seed_skills.json not found at %s", path)
        return

    skills = json.loads(path.read_text(encoding="utf-8"))
    inserted = 0

    for s in skills:
        existing = await db.execute(select(Skill.id).where(Skill.id == s["id"]))
        if existing.scalar_one_or_none() is not None:
            continue
        db.add(Skill(
            id=s["id"],
            canonical_name=s["canonical_name"],
            category=s["category"],
            subcategory=s.get("subcategory"),
            aliases=s.get("aliases"),
        ))
        inserted += 1

    if inserted:
        await db.commit()
        logger.info("Seeded %d skills", inserted)


async def run_all_seeds(db: AsyncSession) -> None:
    await seed_platforms(db)
    await seed_skills(db)
