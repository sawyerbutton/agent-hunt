# Agent Hunt

> 用数据告诉你，AI Agent 工程师到底需要什么 — 国内外全平台覆盖，跨市场对比分析。

## 这是什么

Agent Hunt 采集国内外 10+ 主流招聘平台的 AI Agent 工程师 JD，通过 LLM 进行结构化解析，生成**技能图谱**、**跨市场对比**和**个性化学习路径**。

不靠猜，靠数据。不看单一市场，看全球。

## 为什么需要这个

AI Agent 工程师是 2025-2026 年最火的岗位之一，但：
- 国内和国际市场对这个岗位的定义差异巨大
- 不同平台的 JD 质量参差不齐，信息分散
- 求职者不知道该学什么，培训机构不知道该教什么

Agent Hunt 解决的问题：**用真实 JD 数据，消除信息差**。

## 核心功能

### 多平台数据采集
从国内外 10+ 招聘平台采集 AI Agent 相关 JD，统一解析为标准化格式。

| 市场 | 平台 | 优先级 |
|---|---|---|
| 国内 | Boss直聘、猎聘 | Tier 1 |
| 国际 | LinkedIn、Indeed | Tier 1 |
| 国内 | 拉勾、脉脉 | Tier 2 |
| 国际 | Wellfound、Glassdoor | Tier 2 |
| 远程 | RemoteOK、We Work Remotely | Tier 3 |

### AI 驱动的 JD 解析
- Gemini API 驱动的中英双语 JD 结构化解析
- 自动提取：技能要求、薪资范围、经验门槛、工作模式
- 多语言技能归一化（大模型 = LLM、朗链 = LangChain）

### 跨市场对比分析（核心差异化）
- **技能差异**：国内 vs 国际，哪些技能是共通的？哪些是各自独有的？
- **薪资对标**：同等级岗位在不同市场的薪资对比（含汇率换算）
- **岗位定义**：国内的"全栈型" vs 国际的"专精型"
- **Remote 机会**：不同市场的远程工作比例

### 技能图谱
- 高频技能排行（按平台 / 按市场）
- 技能关联网络（哪些技能经常一起出现）
- 技能趋势追踪

### 个性化学习路径
- 输入你的现有技能
- 选择目标市场（国内 / 国际 / 全球）
- 生成技能差距分析 + 推荐学习顺序 + 资源链接

## 技术栈

| 层 | 技术 |
|---|---|
| 后端 | Python 3.11 · FastAPI · SQLAlchemy 2.0 (async) · Celery |
| 前端 | Next.js 14 · Tailwind · shadcn/ui · Recharts |
| AI | Gemini API (gemini-2.5-flash) · pgvector · 多语言技能归一化 |
| 数据采集 | Playwright · Chrome Extension · 策略模式 + 注册表模式 |
| 基础设施 | PostgreSQL 16 · Redis 7 · Docker Compose |

## 项目结构

```
agent-hunt/
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── api/v1/             # REST API 路由
│   │   ├── collectors/         # 多平台数据采集器（策略模式）
│   │   ├── models/             # SQLAlchemy 数据模型
│   │   ├── schemas/            # Pydantic 请求/响应 schema
│   │   ├── services/           # 业务逻辑（JD解析、技能提取、跨市场分析）
│   │   ├── tasks/              # Celery 异步任务
│   │   ├── config.py           # pydantic-settings 配置
│   │   └── database.py         # 异步数据库引擎
│   ├── alembic/                # 数据库迁移
│   ├── tests/
│   └── pyproject.toml
├── frontend/                   # Next.js 前端
│   └── src/
│       ├── app/                # 页面（Dashboard、JD列表、技能图谱、跨市场对比、学习路径）
│       ├── components/         # UI + 图表 + 布局组件
│       ├── lib/                # API 客户端 + 工具函数
│       └── stores/             # Zustand 状态管理
├── extension/                  # Chrome 浏览器插件
│   ├── content_scripts/        # 各平台 JD 提取脚本
│   └── popup/                  # 插件弹窗 UI
├── data/                       # 种子数据
│   ├── sample_jds/             # JD 样本（domestic/ + international/）
│   ├── seed_platforms.json     # 10 个平台元数据
│   ├── seed_skills.json        # 50 个核心 AI 技能（中英双语别名）
│   └── skill_aliases.json      # 技能同义词映射表（100+ 条）
├── docs/
│   └── domestic-scraping-strategy.md  # 国内平台爬虫技术方案
├── docker-compose.yml          # PostgreSQL 16 (pgvector) + Redis 7
└── .env.example
```

## 数据模型

三个核心表：

- **platforms** — 招聘平台元数据（市场、Tier、采集难度、数据质量等）
- **jobs** — JD 数据（原始文本 + LLM 解析后的结构化字段），通过 `(platform_id, platform_job_id)` 联合唯一约束去重
- **skills** — 技能分类（含 JSONB 多语言别名、按市场统计计数）

## 快速开始

```bash
git clone <repo-url>
cd agent-hunt

# 1. 启动基础设施
cp .env.example .env
# 编辑 .env 填入你的 Gemini API Key
docker compose up -d

# 2. 安装后端依赖
cd backend
pip install -e ".[dev]"

# 3. 运行数据库迁移
alembic upgrade head

# 4. 启动后端（自动加载种子平台和技能数据）
uvicorn app.main:app --reload
```

启动后访问 http://localhost:8000/docs 查看 Swagger API 文档。

### API 端点

```
GET  /health                          — 健康检查
POST /api/v1/jobs/import              — 导入单条 JD
POST /api/v1/jobs/import/batch        — 批量导入（最多 100 条）
GET  /api/v1/jobs                     — 职位列表（分页 + 按平台/市场/状态筛选）
GET  /api/v1/jobs/{id}                — 职位详情
POST /api/v1/jobs/{id}/parse          — 触发 Gemini 结构化解析
GET  /api/v1/platforms                — 平台列表
GET  /api/v1/platforms/{id}           — 平台详情
```

## 数据采集策略

数据采集是本项目的**核心硬需求**。经过调研，各平台均无官方 API 直接提供 JD 批量检索，必须通过多种技术手段攻克。

> 详细技术方案见 [docs/domestic-scraping-strategy.md](docs/domestic-scraping-strategy.md)

### 国内平台（必须攻克）

国内平台是数据源的重中之重，采用**多路并进、逐层升级**策略：

```
Layer 0: 手动导入 JSON（保底）
Layer 1: Chrome 浏览器插件（浏览时自动提取）
Layer 2: Playwright 浏览器自动化（模拟真人操作）
Layer 3: API 逆向 + 请求模拟（高效批量）
Layer 4: 移动端 API 抓包（反爬可能更弱）
```

| 平台 | 主力方案 | 反爬难度 | 关键挑战 | 已验证的开源参考 |
|---|---|---|---|---|
| **Boss直聘** | Playwright + Cookie 持久化 | 最高 | 薪资字体加密、设备指纹、登录墙 | [auto-zhipin](https://github.com/ufownl/auto-zhipin) (Playwright) |
| **猎聘** | Playwright + 页面等待 | 中高 | 动态参数、搜索需手动点击 | [job-hunting-tampermonkey](https://github.com/lastsunday/job-hunting-tampermonkey) |
| **拉勾** | Playwright / POST API 模拟 | 中 | 登录墙、Cookie 依赖 | [ECommerceCrawlers](https://github.com/DropsDevopsOrg/ECommerceCrawlers) |

### 国际平台

| 平台 | 主力方案 | 备注 |
|---|---|---|
| LinkedIn / Indeed / Glassdoor | [JobSpy](https://github.com/speedyapply/JobSpy) (Python) | 同时抓取多平台，输出 CSV |
| 补充数据 | [Adzuna API](https://developer.adzuna.com/) | 多国职位聚合 API |

### 合规原则

- 仅采集公开可访问的职位信息
- 不存储任何个人信息（HR 姓名、联系方式等）
- 数据仅用于统计分析，不原文展示他人内容
- 自动化采集设置合理延迟（3-8 秒 / 请求）
- 单次会话限量（50-100 条）

## 项目状态

积极开发中 — Phase 1 进行中

| Phase | 内容 | 状态 |
|---|---|---|
| 1 | 最小闭环（手动导入 → LLM 解析 → API） | **进行中** |
| 2 | **国内平台爬虫（核心优先级）** + Chrome 扩展 | 待开始 |
| 3 | 国际平台采集（JobSpy 集成）+ 跨市场分析引擎 | 待开始 |
| 4 | 前端完善 + 数据可视化 | 待开始 |
| 5 | 产品化（用户系统、匹配评分、导出） | 待开始 |

### Phase 1 详细进度

- [x] 项目骨架初始化（全目录结构 + 占位文件）
- [x] Docker Compose（PostgreSQL 16 + pgvector + Redis 7）
- [x] 数据模型（Platform / Job / Skill）+ Alembic 首次迁移
- [x] 种子数据（50 技能 + 100+ 别名映射）
- [x] 配置管理（pydantic-settings + .env.example）
- [x] LLM 方案确定（Gemini API）+ 数据采集策略调研
- [x] 手动导入服务（JSON 导入 + 去重）
- [x] JD 解析服务（Gemini API 中英双语结构化解析）
- [x] API 端点（import / list / detail / parse / platforms）
- [x] 平台种子数据（10 个平台）+ 启动时自动加载
- [ ] 前端最简 JD 详情页
- [ ] 种子 JD 数据（国内 20 条 + 国际 15 条）

### Phase 2 预览：国内爬虫攻坚

- [ ] BaseCollector 抽象类 + CollectorRegistry 注册表
- [ ] Boss直聘 Playwright 采集器（Cookie 持久化 + 薪资字体解密）
- [ ] 猎聘 Playwright 采集器（动态参数处理）
- [ ] 拉勾 Playwright 采集器（POST API 模拟）
- [ ] Chrome 扩展 v1（三个国内平台页面 JD 提取）
- [ ] 代理 IP 池 + Cookie 池基础设施
- [ ] Boss直聘移动端 API 验证（探索性）
- [ ] Celery 任务调度（定时采集 + 去重）

## Contributing

欢迎贡献！特别欢迎以下方向：
- 新平台采集器的实现
- 种子 JD 数据的补充（`data/sample_jds/`）
- 技能同义词映射的完善（`data/skill_aliases.json`）

## License

MIT
