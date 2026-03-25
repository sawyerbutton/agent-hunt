# 国内招聘平台爬虫技术方案

> 国内平台爬虫是本项目的**硬需求**，必须实现。本文档详细列出每个平台的多层攻克方案。

## 总体策略：多路并进，逐层升级

不依赖单一方案。每个平台同时准备多条路径，按风险从低到高逐层尝试：

```
Layer 0: 手动导入（保底，100%可用）
Layer 1: Chrome 浏览器插件（零风险，用户主动触发）
Layer 2: Playwright 浏览器自动化（中风险，模拟真人操作）
Layer 3: API 逆向 + 请求模拟（高技术门槛，高效率）
Layer 4: 移动端 API 抓包（备选，反爬可能更弱）
```

---

## 平台一：Boss直聘（zhipin.com）

### 反爬机制分析

Boss直聘是三个平台中反爬**最严格**的：

| 防护层 | 具体措施 |
|---|---|
| 登录墙 | 必须登录才能查看完整 JD |
| 薪资加密 | 使用自定义字体（Unicode 映射），页面上的薪资数字是自定义 codepoint |
| 设备指纹 | 检测 `navigator.webdriver` 等自动化特征 |
| IP 频率限制 | 高频请求直接封 IP |
| Cookie 校验 | Cookie 中包含加密 token，有效期短 |
| AJAX 动态加载 | 职位列表通过滚动触发 AJAX 加载，无传统翻页 |

### 方案 A：Playwright 浏览器自动化（主力方案）

基于 [ufownl/auto-zhipin](https://github.com/ufownl/auto-zhipin) 的验证过的方案：

**核心思路**：
1. Playwright 启动 Chromium，禁用自动化检测特征
2. 加载预存的 Cookie 实现免登录（Cookie 通过手动登录一次获取）
3. 模拟滚动加载更多职位
4. 点击每个职位卡片进入详情页提取完整 JD
5. 薪资字段通过字体映射表解密

**关键技术点**：
```python
# 1. 反检测启动
browser = await p.chromium.launch(
    args=["--disable-blink-features=AutomationControlled"]
)

# 2. Cookie 持久化（手动登录一次，后续复用）
async def load_cookies(context, cookies_path):
    if cookies_path.exists():
        data = json.load(open(cookies_path))
        await context.add_cookies(data["cookies"])

# 3. 薪资字体解密映射
salary_mapping = {
    chr(0xE031): "0", chr(0xE032): "1", chr(0xE033): "2",
    chr(0xE034): "3", chr(0xE035): "4", chr(0xE036): "5",
    chr(0xE037): "6", chr(0xE038): "7", chr(0xE039): "8",
    chr(0xE03a): "9",
}

# 4. 滚动加载
container = page.locator(".job-list-container")
await container.hover()
for _ in range(scroll_n):
    bbox = await container.bounding_box()
    await page.mouse.wheel(0, bbox["height"])
    await page.wait_for_timeout(random.randint(2000, 5000))
```

**实施步骤**：
1. 用户手动登录一次 Boss直聘，导出 Cookie（插件辅助或手动）
2. Playwright 加载 Cookie，搜索 "AI Agent" / "大模型" 等关键词
3. 滚动翻页采集职位列表（公司名、职位名、薪资、链接）
4. 逐个进入详情页提取完整 JD 文本
5. 随机延迟 3-8 秒，单次会话限制 50-100 条

### 方案 B：Chrome 浏览器插件（辅助方案）

用户正常浏览 Boss直聘时，插件自动提取当前页面 JD 数据。

**技术实现**：
```javascript
// content_scripts/boss_zhipin.js
// 监听职位详情页
if (location.href.match(/zhipin\.com\/job_detail/)) {
    const jd = {
        title: document.querySelector('.job-title .name')?.textContent,
        salary: document.querySelector('.job-title .salary')?.textContent,
        company: document.querySelector('.company-info .name')?.textContent,
        description: document.querySelector('.job-detail-section .text')?.textContent,
        location: document.querySelector('.job-title .location')?.textContent,
        experience: document.querySelector('.job-title .text-desc')?.textContent,
    };
    // 发送到后端 API
    chrome.runtime.sendMessage({ type: 'JD_CAPTURED', data: jd });
}
```

**优点**：零风险，用户主动操作，数据质量高
**缺点**：效率低，依赖用户手动浏览

### 方案 C：移动端 API（探索方案）

Boss直聘早期有移动端接口 `/mobile/jobs.json`，验证较弱：

```python
# 旧版移动端接口（可能已失效，需要验证）
base_url = "https://www.zhipin.com/mobile/jobs.json"
params = {"query": "AI Agent", "page": 1, "city": city_code}
response = requests.get(url=base_url, params=params, headers=mobile_headers)
```

**城市代码获取**：
```python
# 公开接口，无需认证
city_api = "https://www.zhipin.com/wapi/zpCommon/data/city.json"
```

**风险**：此接口可能已加固或下线，需要实际验证。如可用则效率最高。

### 方案 D：API 逆向（高级方案）

使用 Charles / mitmproxy 抓包分析 Web 端请求：
1. 抓取 `/wapi/zpgeek/search/joblist.json` 等搜索接口
2. 分析 `zpData` 加密参数（通常是 AES + Base64）
3. 通过 Frida hook 或 JS 逆向还原加密算法
4. 模拟请求直接获取 JSON 数据

**工具链**：mitmproxy / Charles → Chrome DevTools → AST 分析 JS → 还原加密

**风险**：技术门槛最高，平台更新后可能失效

---

## 平台二：猎聘（liepin.com）

### 反爬机制分析

猎聘反爬**中等偏严格**：

| 防护层 | 具体措施 |
|---|---|
| 动态加载 | JS 渲染，需等待 DOM 加载完成 |
| 搜索交互 | 搜索按钮需要手动点击触发 |
| 动态参数 | `d_ckId`、`siTag` 等动态生成的请求参数 |
| 频率限制 | IP 级别限流 |
| 验证码 | 高频操作触发图形验证码 |

### 方案 A：Playwright 自动化（主力方案）

```python
from playwright.async_api import async_playwright
import random, asyncio

async def scrape_liepin(keyword: str, pages: int = 5):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,  # 猎聘对 headless 检测较严，建议 headed
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ..."
        )
        page = await context.new_page()

        for page_num in range(1, pages + 1):
            url = f"https://www.liepin.com/zhaopin/?key={keyword}&curPage={page_num - 1}"
            await page.goto(url, wait_until="networkidle")
            await page.wait_for_selector(".job-list-item", timeout=10000)

            # 提取职位列表
            jobs = await page.query_selector_all(".job-list-item")
            for job in jobs:
                title = await job.query_selector(".job-title-box .ellipsis-1")
                company = await job.query_selector(".company-name .ellipsis-1")
                salary = await job.query_selector(".job-salary")
                # ... 提取更多字段

                # 点击进入详情页
                await job.click()
                await page.wait_for_timeout(random.randint(2000, 4000))
                # 提取完整 JD
                detail = await page.query_selector(".job-intro-container")
                # ...

            await page.wait_for_timeout(random.randint(3000, 6000))

        await browser.close()
```

**关键点**：
- URL 格式清晰：`/zhaopin/?key=关键词&curPage=页码`
- 需要等待 JS 渲染完成（`wait_for_selector`）
- 建议使用非 headless 模式降低检测概率
- 随机延迟 3-6 秒

### 方案 B：API 逆向 + Requests

1. 使用 Charles/Fiddler 抓取搜索接口
2. 提取 `d_ckId`、`siTag` 等动态参数的生成逻辑
3. 如参数为前端 JS 生成，可能需要 JS 逆向或用 Playwright 预获取
4. 直接 requests 模拟请求，效率更高

### 方案 C：Chrome 插件

与 Boss直聘类似，监听职位详情页 DOM：

```javascript
// content_scripts/liepin.js
if (location.href.match(/liepin\.com\/job\/\d+/)) {
    const jd = {
        title: document.querySelector('.name')?.textContent,
        salary: document.querySelector('.job-salary')?.textContent,
        company: document.querySelector('.company-name')?.textContent,
        description: document.querySelector('.job-intro-container')?.textContent,
        tags: [...document.querySelectorAll('.labels-tag')].map(t => t.textContent),
    };
    chrome.runtime.sendMessage({ type: 'JD_CAPTURED', data: jd });
}
```

---

## 平台三：拉勾（lagou.com）

### 反爬机制分析

拉勾反爬**中等**：

| 防护层 | 具体措施 |
|---|---|
| 登录墙 | 查看 JD 详情需要登录 |
| AJAX 接口 | 搜索结果通过 POST 接口返回 JSON |
| 频率限制 | 中等频率限制 |
| 反爬 JS | 有基本的浏览器指纹检测 |

### 方案 A：Playwright 自动化

```python
async def scrape_lagou(keyword: str, pages: int = 5):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # 拉勾需要先访问首页获取 Cookie
        await page.goto("https://www.lagou.com")
        await page.wait_for_timeout(3000)

        # 搜索
        await page.goto(f"https://www.lagou.com/wn/zhaopin?kd={keyword}")
        await page.wait_for_selector(".item__10RTO", timeout=10000)

        for page_num in range(pages):
            items = await page.query_selector_all(".item__10RTO")
            for item in items:
                # 提取列表信息
                title = await item.query_selector(".p-top__1F7CL a")
                company = await item.query_selector(".company-name__2-SjF")
                # ...

            # 翻页
            next_btn = await page.query_selector(".lg-pagination-next")
            if next_btn:
                await next_btn.click()
                await page.wait_for_timeout(random.randint(3000, 5000))

        await browser.close()
```

### 方案 B：POST API 模拟

拉勾的搜索接口为 POST 请求，可直接模拟：

```python
url = "https://www.lagou.com/jobs/positionAjax.json"
headers = {
    "Referer": f"https://www.lagou.com/jobs/list_{keyword}",
    "Cookie": "从浏览器获取",
}
data = {
    "first": "true",
    "pn": 1,
    "kd": keyword,
}
response = requests.post(url, headers=headers, data=data)
```

**注意**：需要先访问搜索页获取有效 Cookie（`user_trace_token`、`LGUID` 等）。

---

## 通用基础设施

### 代理 IP 池

国内平台必备，推荐方案：

| 方案 | 成本 | 适用场景 |
|---|---|---|
| 免费代理 (快代理等) | 免费 | 测试阶段 |
| 付费短效代理 (芝麻代理、蘑菇代理) | 低 | 日常小规模采集 |
| 付费独享代理 | 中 | 稳定大规模采集 |
| 自建代理池 | 高 | 长期运营 |

### Cookie 池

```python
class CookiePool:
    """维护多个有效 Cookie，轮换使用"""
    def __init__(self):
        self.cookies = []  # List[dict]
        self.current = 0

    async def refresh(self, platform: str):
        """通过 Playwright 手动登录获取新 Cookie"""
        pass

    def get(self) -> dict:
        cookie = self.cookies[self.current]
        self.current = (self.current + 1) % len(self.cookies)
        return cookie
```

### 请求指纹随机化

```python
import random

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ...",
    # ... 20+ UA
]

VIEWPORTS = [
    {"width": 1920, "height": 1080},
    {"width": 1440, "height": 900},
    {"width": 1366, "height": 768},
]

def random_delay(min_sec=2, max_sec=8):
    return random.uniform(min_sec, max_sec)
```

### 数据去重

```python
# 通过 platform_id + platform_job_id 联合唯一约束
# 已在数据模型中实现（uq_job_platform_dedup）
```

---

## 实施优先级

```
Phase 1（当前）: 手动导入 JSON → 跑通解析+存储闭环
Phase 2-A:      Chrome 插件 v1（Boss直聘 + 猎聘 + 拉勾）
Phase 2-B:      Playwright 自动化（三个平台同步推进）
Phase 2-C:      移动端 API 验证（Boss直聘）
Phase 3:        API 逆向 + 代理池 + Cookie 池（规模化）
```

## 参考项目

| 项目 | 地址 | 方案 | 状态 |
|---|---|---|---|
| auto-zhipin | github.com/ufownl/auto-zhipin | Playwright + Cookie + 字体解密 | 活跃维护 |
| ECommerceCrawlers | github.com/DropsDevopsOrg/ECommerceCrawlers | Requests + 移动端 API | 参考价值 |
| job-hunting-tampermonkey | github.com/lastsunday/job-hunting-tampermonkey | 油猴脚本 + 本地存储 | 活跃维护 |
| JobSpy | github.com/speedyapply/JobSpy | Python 多平台爬虫 | 仅国际平台 |
