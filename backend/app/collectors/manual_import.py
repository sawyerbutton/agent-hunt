# Manual import service — accepts raw JD data and saves to database.
from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job
from app.schemas.job import JobImportRequest, JobImportResponse


async def import_jobs(
    db: AsyncSession,
    requests: list[JobImportRequest],
) -> JobImportResponse:
    """Import one or more raw JDs into the database, skipping duplicates."""
    imported_ids: list[uuid.UUID] = []
    skipped = 0

    for req in requests:
        # Check for duplicate
        existing = await db.execute(
            select(Job.id).where(
                Job.platform_id == req.platform_id,
                Job.platform_job_id == req.platform_job_id,
            )
        )
        if existing.scalar_one_or_none() is not None:
            skipped += 1
            continue

        job = Job(
            platform_id=req.platform_id,
            platform_job_id=req.platform_job_id,
            source_url=req.source_url,
            raw_content=req.raw_content,
            language=req.language,
            parse_status="pending",
        )
        db.add(job)
        await db.flush()  # populate job.id
        imported_ids.append(job.id)

    await db.commit()

    return JobImportResponse(
        imported=len(imported_ids),
        skipped=skipped,
        job_ids=imported_ids,
    )
