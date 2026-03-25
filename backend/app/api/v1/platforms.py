# Platform API endpoints — list and detail.
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.platform import Platform
from app.schemas.platform import PlatformListResponse, PlatformResponse

router = APIRouter(prefix="/platforms", tags=["platforms"])


@router.get("", response_model=PlatformListResponse)
async def list_platforms(db: AsyncSession = Depends(get_db)):
    """List all registered platforms."""
    total = (await db.execute(select(func.count(Platform.id)))).scalar_one()
    result = await db.execute(select(Platform).order_by(Platform.tier, Platform.id))
    platforms = result.scalars().all()
    return PlatformListResponse(
        total=total,
        items=[PlatformResponse.model_validate(p) for p in platforms],
    )


@router.get("/{platform_id}", response_model=PlatformResponse)
async def get_platform(platform_id: str, db: AsyncSession = Depends(get_db)):
    """Get a single platform by ID."""
    result = await db.execute(select(Platform).where(Platform.id == platform_id))
    platform = result.scalar_one_or_none()
    if platform is None:
        raise HTTPException(status_code=404, detail="Platform not found")
    return PlatformResponse.model_validate(platform)
