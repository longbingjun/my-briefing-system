# My Briefing System

一个参考 Distilled 思路搭建的个人中文 AI 简报系统。

它不是简单 RSS 列表，而是把信息处理成三层结构：

```text
长期关注领域
-> 领域下的实体/主题
-> 每期文章主题分组
```

## 当前能力

1. 定时抓取 RSS 信源。
2. 按长期领域和实体主题打分、聚合。
3. 英文内容可自动翻译成中文标题和摘要。
4. 可用 OpenAI-compatible 接口接入 Qwen、DeepSeek 或 OpenAI。
5. 生成今日漏斗、实体追踪、内容分栏、信源画像。
6. 输出公开 JSON、Markdown、llms.txt。
7. 通过 GitHub Pages 发布成静态网站。

## 公开数据文件

GitHub Actions 每次运行后会在 `public/` 下生成：

```text
public/lists/today.json
public/lists/watchlist.json
public/lists/boards.json
public/lists/article_details.json
public/lists/sources.json
public/digest-latest.md
public/llms.txt
public/llms-full.txt
```

页面本身只读取这些静态文件，所以不需要后端服务器。

## 页面结构

```text
#today    今日导读、蒸馏漏斗、今日值得看
#watch    实体追踪、30 天热度曲线、今日增量
#content  学啥 / 读啥 / 做啥 / 忽略
#sources  信源画像、质量指数、活跃度
#api      公开 JSON 与 Markdown 入口
#story    项目背后的处理链路
```

## 本地运行

```bash
pip install -r requirements.txt
python scripts/run_pipeline.py
```

然后直接打开：

```text
public/index.html
```

## 使用 Qwen 或 DeepSeek

不一定要使用 OpenAI API。只要服务商提供 OpenAI-compatible `/chat/completions` 接口，就可以这样配置：

```text
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL=qwen-plus
LLM_API_KEY=你的 DashScope Key
```

或者：

```text
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-chat
LLM_API_KEY=你的 DeepSeek Key
```

GitHub 仓库里推荐这样设置：

```text
Settings
-> Secrets and variables
-> Actions
```

Secret:

```text
LLM_API_KEY
```

Variables:

```text
LLM_BASE_URL
LLM_MODEL
TRANSLATE_MAX_PER_RUN
```

如果没有配置 LLM，系统仍然可以运行，只是英文内容不会真正翻译，实体摘要会退化成规则生成。

## 信源维护

信源在 `sources.yaml`，长期关注实体在 `entities.yaml`，个人偏好在 `feedback.yaml`。

当前默认覆盖：

```text
AI 研究前沿
AI 产品与 Agent
AI 改造传统领域
官方信号与科技圈动态
财务数字化与成本管理
```

## X/Twitter 来源

`sources.yaml` 已预留：

```text
X / Anthropic
X / OpenAI
X / Zara Zhang
```

这些默认关闭。更稳的接入方式是：

```text
自建 RSSHub
-> 把 X/Twitter 账号转成 RSS
-> 修改 sources.yaml 的 url
-> enabled: true
```

不建议在 GitHub Actions 里直接爬 X 页面，稳定性和合规风险都比较高。

## GitHub Pages

仓库推到 GitHub 后：

```text
Settings
-> Pages
-> Source: GitHub Actions
```

然后到：

```text
Actions
-> Briefing
-> Run workflow
```

运行成功后，Pages 会发布 `public/` 目录。
