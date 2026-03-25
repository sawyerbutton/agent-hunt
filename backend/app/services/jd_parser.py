# JD structured parsing via Gemini API — bilingual (Chinese/English) support.
from __future__ import annotations

import json
import logging

from google import genai
from google.genai import types
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.job import Job
from app.schemas.job import ParsedJD

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """\
你是一个专业的 JD（职位描述）结构化解析引擎。
你的任务是将原始 JD 文本解析为标准化的 JSON 格式。

关键规则：
1. 技能名称统一使用英文标准名（例：大模型 → LLM，朗链 → LangChain，通义千问 → Qwen）
2. 薪资统一转换为人民币月薪（如遇美元年薪，按 7.25 汇率 /12 换算；欧元按 7.90/12）
3. 如果信息缺失，对应字段填 null，不要猜测
4. required_skills 只包含 JD 明确要求的技能
5. preferred_skills 包含"加分项"、"优先"、"nice to have"的技能
6. market 根据公司所在地和语言判断：中国大陆公司为 "domestic"，其他为 "international"
7. company_size: "startup"(< 50 人), "mid"(50-500), "large"(500-5000), "enterprise"(> 5000)

严格输出以下 JSON，不要添加任何额外文字：
{
  "title": "string | null",
  "company_name": "string | null",
  "company_size": "startup | mid | large | enterprise | null",
  "location": "string | null",
  "market": "domestic | international",
  "work_mode": "onsite | remote | hybrid | null",
  "salary_min_rmb": "int | null",
  "salary_max_rmb": "int | null",
  "salary_currency_original": "CNY | USD | EUR | null",
  "experience_min_years": "int | null",
  "experience_max_years": "int | null",
  "education": "bachelor | master | phd | any | null",
  "required_skills": ["string"],
  "preferred_skills": ["string"],
  "responsibilities": ["string"],
  "language": "zh | en | mixed"
}"""


def _build_client() -> genai.Client:
    return genai.Client(api_key=settings.gemini_api_key)


async def parse_jd(raw_content: str) -> ParsedJD:
    """Parse a single raw JD text into structured fields using Gemini."""
    client = _build_client()

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=raw_content,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.1,
            response_mime_type="application/json",
        ),
    )

    text = response.text.strip()
    data = json.loads(text)
    return ParsedJD(**data)


async def parse_job_by_id(db: AsyncSession, job_id) -> Job:
    """Load a job from DB, parse its raw_content, and save structured fields."""
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one()

    try:
        parsed = await parse_jd(job.raw_content)

        job.title = parsed.title
        job.company_name = parsed.company_name
        job.company_size = parsed.company_size
        job.location = parsed.location
        job.market = parsed.market
        job.work_mode = parsed.work_mode
        job.salary_min = parsed.salary_min_rmb
        job.salary_max = parsed.salary_max_rmb
        job.salary_currency = parsed.salary_currency_original
        job.experience_min = parsed.experience_min_years
        job.experience_max = parsed.experience_max_years
        job.education = parsed.education
        job.required_skills = parsed.required_skills
        job.preferred_skills = parsed.preferred_skills
        job.responsibilities = parsed.responsibilities
        job.language = parsed.language
        job.parse_status = "parsed"

        from datetime import datetime, timezone
        job.parsed_at = datetime.now(timezone.utc)

    except Exception:
        logger.exception("Failed to parse job %s", job_id)
        job.parse_status = "failed"

    await db.commit()
    await db.refresh(job)
    return job
