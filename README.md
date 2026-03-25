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
- Claude API 驱动的中英双语 JD 结构化解析
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
| AI | Claude API · pgvector · 多语言技能归一化 |
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
│   ├── seed_skills.json        # 50 个核心 AI 技能（中英双语别名）
│   └── skill_aliases.json      # 技能同义词映射表（100+ 条）
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
# 编辑 .env 填入你的 Anthropic API Key
docker compose up -d

# 2. 安装后端依赖
cd backend
pip install -e ".[dev]"

# 3. 运行数据库迁移
alembic upgrade head

# 4. 启动后端
uvicorn app.main:app --reload
```

## 数据来源说明

- 本项目仅采集公开可访问的职位信息
- 不存储任何个人信息（HR姓名、联系方式等）
- 数据仅用于统计分析，不原文展示他人内容
- 支持手动导入 + 浏览器插件两种零风险数据获取方式

## 项目状态

积极开发中 — Phase 1 进行中

| Phase | 内容 | 状态 |
|---|---|---|
| 1 | 最小闭环（手动导入 → LLM 解析 → API） | **进行中** — 骨架 + 数据模型 + 种子数据已完成，下一步：手动导入 + JD 解析 + API |
| 2 | 多平台数据采集 + Chrome 扩展 | 待开始 |
| 3 | 分析引擎 + 跨市场对比 | 待开始 |
| 4 | 前端完善 + 数据可视化 | 待开始 |
| 5 | 产品化（用户系统、匹配评分、导出） | 待开始 |

### Phase 1 详细进度

- [x] 项目骨架初始化（全目录结构 + 占位文件）
- [x] Docker Compose（PostgreSQL 16 + pgvector + Redis 7）
- [x] 数据模型（Platform / Job / Skill） + Alembic 首次迁移
- [x] 种子数据（50 技能 + 100+ 别名映射）
- [x] 配置管理（pydantic-settings + .env.example）
- [ ] 手动导入服务（JSON 格式 JD 导入）
- [ ] JD 解析服务（Claude API 中英双语结构化解析）
- [ ] API 端点（POST /import, GET /jobs/{id}, GET /platforms）
- [ ] 前端最简 JD 详情页
- [ ] 种子 JD 数据（国内 20 条 + 国际 15 条）

## Contributing

欢迎贡献！特别欢迎以下方向：
- 新平台采集器的实现
- 种子 JD 数据的补充（`data/sample_jds/`）
- 技能同义词映射的完善（`data/skill_aliases.json`）

## License

MIT
