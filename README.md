# My Briefing System

一个 makino-distilled 风格的个人中文 AI 简报与知识库入口 MVP。

它完成 1-4 阶段：

1. 配置信源和长期关注实体
2. GitHub Actions 定时抓取 RSS
3. 按长期领域、实体主题、每期主题分组生成结构化 `watchlist.json` 和可读 `digest-latest.md`
4. 用静态网页展示简报

## 目录结构

```text
my-briefing-system/
├── sources.yaml
├── entities.yaml
├── feedback.yaml
├── requirements.txt
├── scripts/
│   └── run_pipeline.py
├── data/
│   └── articles.json
├── public/
│   ├── index.html
│   ├── app.js
│   ├── styles.css
│   ├── digest-latest.md
│   └── watchlist.json
└── .github/
    └── workflows/
        └── briefing.yml
```

## 本地运行

```bash
pip install -r requirements.txt
python scripts/run_pipeline.py
```

运行后会生成：

```text
public/digest-latest.md
public/watchlist.json
data/articles.json
```

然后直接打开 `public/index.html` 即可查看网页。

## GitHub Actions

把整个目录推到 GitHub 仓库后，Actions 会每天北京时间 09:25 和 20:25 自动运行。

如果需要 AI 摘要，在 GitHub 仓库中添加 Secret：

```text
OPENAI_API_KEY
```

没有 API key 也能运行，只是摘要会使用规则生成。

## 关注结构

本项目采用三层结构：

```text
长期关注领域
-> 领域下的实体/主题
-> 每期文章主题分组
```

当前默认领域包括：

```text
AI 研究前沿
AI 产品与 Agent
AI 改造传统领域
官方信号与科技圈动态
财务数字化与成本管理
```

## 配置信源

编辑 `sources.yaml`：

```yaml
sources:
  - id: openai_blog
    name: OpenAI Blog
    type: rss
    url: https://openai.com/news/rss.xml
    weight: 0.95
```

## 配置关注实体

编辑 `entities.yaml`：

```yaml
entities:
  - id: ai_agents
    name: AI Agents
    type: Concept
    keywords:
      - agent
      - agents
      - tool use
```

## 反馈与中文偏好

编辑 `feedback.yaml` 可以调整个人偏好：

```yaml
language_preference:
  preferred: zh
  zh_bonus: 10

boost_keywords:
  - 预训练
  - 后训练
  - 推理训练
  - 成本数据库
```

中文优先采用加权方式，不会丢弃 OpenAI、Anthropic、Google DeepMind 等官方英文一手信源。

## Twitter/X 来源

X/Twitter 来源已预留在 `sources.yaml`，但默认 `enabled: false`。

建议后续使用以下方式之一接入：

```text
自建 RSSHub
官方 X API
手动维护高价值账号链接
```

不建议直接在 GitHub Actions 中硬爬 X 页面，稳定性和合规风险都比较高。

## 输出格式

`watchlist.json` 是机器可读结构，适合网页、Skill、机器人复用。

`digest-latest.md` 是人可读简报，适合终端、邮件、Obsidian、Notion。
