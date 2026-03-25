# 🎯 Agent Hunt

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

### 📡 多平台数据采集
从国内外 10+ 招聘平台采集 AI Agent 相关 JD，统一解析为标准化格式。

| 市场 | 平台 | 状态 |
|---|---|---|
| 🇨🇳 国内 | Boss直聘、猎聘、拉勾、脉脉、智联招聘 | Tier 1-3 逐步覆盖 |
| 🌍 国际 | LinkedIn、Indeed、Wellfound、Glassdoor | Tier 1-3 逐步覆盖 |
| 🏠 远程 | RemoteOK、We Work Remotely | Tier 3 补充 |

### 🧠 AI 驱动的 JD 解析
- Claude API 驱动的中英双语 JD 结构化解析
- 自动提取：技能要求、薪资范围、经验门槛、工作模式
- 多语言技能归一化（大模型 = LLM、朗链 = LangChain）

### 📊 跨市场对比分析（核心差异化）
- **技能差异**：国内 vs 国际，哪些技能是共通的？哪些是各自独有的？
- **薪资对标**：同等级岗位在不同市场的薪资对比
- **岗位定义**：国内的"全栈型" vs 国际的"专精型"
- **Remote 机会**：不同市场的远程工作比例

### 🗺️ 技能图谱
- 高频技能排行（按平台 / 按市场）
- 技能关联网络（哪些技能经常一起出现）
- 技能趋势追踪

### 🛤️ 个性化学习路径
- 输入你的现有技能
- 选择目标市场（国内 / 国际 / 全球）
- 生成技能差距分析 + 推荐学习顺序 + 资源链接

## 技术栈

| 层 | 技术 |
|---|---|
| 后端 | Python 3.11 · FastAPI · SQLAlchemy 2.0 · Celery |
| 前端 | Next.js 14 · Tailwind · shadcn/ui · Recharts |
| AI | Claude API · pgvector · 多语言 NLP |
| 数据采集 | Playwright · Chrome Extension · 策略模式 |
| 基础设施 | PostgreSQL · Redis · Docker |

## 快速开始

```bash
git clone https://github.com/sawyerbutton/agent-hunt/edit/main/README.md
cd agent-hunt
cp .env.example .env
# 编辑 .env 填入你的 API keys
docker compose up -d
```

## 数据来源说明

- 本项目仅采集公开可访问的职位信息
- 不存储任何个人信息（HR姓名、联系方式等）
- 数据仅用于统计分析，不原文展示他人内容
- 支持手动导入 + 浏览器插件两种零风险数据获取方式

## 项目状态

🚧 积极开发中

| Phase | 内容 | 状态 |
|---|---|---|
| 1 | 最小闭环（手动导入 → LLM解析 → API） | 进行中 |
| 2 | 多平台数据采集 + Chrome 扩展 | 待开始 |
| 3 | 分析引擎 + 跨市场对比 | 待开始 |
| 4 | 前端完善 + 数据可视化 | 待开始 |
| 5 | 产品化（用户系统、匹配评分、导出） | 待开始 |

## Contributing

欢迎贡献！特别欢迎以下方向：
- 新平台采集器的实现
- 种子 JD 数据的补充（`data/sample_jds/`）
- 技能同义词映射的完善（`data/skill_aliases.json`）

## License

MIT
