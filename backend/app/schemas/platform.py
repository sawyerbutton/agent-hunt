# Pydantic schemas for Platform API responses.
from __future__ import annotations

import datetime

from pydantic import BaseModel


class PlatformResponse(BaseModel):
    id: str
    name: str
    market: str
    url: str
    language: str
    tier: int
    scrape_difficulty: int
    data_quality: str
    refresh_rate: str
    has_salary_data: bool
    has_company_size: bool
    collector_class: str | None
    is_enabled: bool
    last_collected_at: datetime.datetime | None
    created_at: datetime.datetime

    model_config = {"from_attributes": True}


class PlatformListResponse(BaseModel):
    total: int
    items: list[PlatformResponse]
