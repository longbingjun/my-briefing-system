# My Briefing System

一个 makino-distilled 风格的个人简报系统 MVP。

它完成 1-4 阶段：

1. 配置信源和关注实体
2. GitHub Actions 定时抓取 RSS
3. 生成结构化 `watchlist.json` 和可读 `digest-latest.md`
4. 用静态网页展示简报

## 目录结构

```text
my-briefing-system/
├── sources.yaml
├── entities.yaml
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

## 输出格式

`watchlist.json` 是机器可读结构，适合网页、Skill、机器人复用。

`digest-latest.md` 是人可读简报，适合终端、邮件、Obsidian、Notion。

