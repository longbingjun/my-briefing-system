# My Briefing System

一个 makino-distilled 风格的个人中文 AI 简报与知识库入口。

系统目标不是简单聚合 RSS，而是把信息处理成三层结构：

```text
长期关注领域
-> 领域下的实体/主题
-> 每期文章主题分组
```

## 当前能力

1. 定时抓取 RSS 信源。
2. 按长期领域和实体主题分类。
3. 对英文标题和摘要生成中文译文。
4. 为每个实体生成中文趋势摘要。
5. 输出机器可读的 `watchlist.json`。
6. 输出人可读的 `digest-latest.md`。
7. 用 GitHub Pages 展示网页。

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

## GitHub Actions 配置

仓库推到 GitHub 后，Actions 会每天北京时间 09:25 和 20:25 自动运行。

如果需要英文内容翻译成中文、实体级中文摘要，请在 GitHub 仓库添加 Secret：

```text
OPENAI_API_KEY
```

路径：

```text
Settings
-> Secrets and variables
-> Actions
-> New repository secret
```

可选变量：

```text
OPENAI_MODEL=gpt-4o-mini
TRANSLATE_MAX_PER_RUN=80
```

没有 `OPENAI_API_KEY` 时，系统仍能运行，但只会使用原始标题和规则摘要，不会真正翻译英文内容。

## 本地运行

```bash
pip install -r requirements.txt
python scripts/run_pipeline.py
```

如果要在本地测试翻译和摘要，需要先设置环境变量：

```bash
export OPENAI_API_KEY=你的密钥
```

Windows PowerShell：

```powershell
$env:OPENAI_API_KEY="你的密钥"
python scripts/run_pipeline.py
```

## 长期关注领域

默认领域包括：

```text
AI 研究前沿
AI 产品与 Agent
AI 改造传统领域
官方信号与科技圈动态
财务数字化与成本管理
```

## 研究主题覆盖

`entities.yaml` 已覆盖：

```text
预训练
后训练与对齐
推理训练与强化学习
AI 评测与安全
AI 基础设施与算力
AI Agents
编程 Agent
AI 产品化
AI 改造传统领域
数据分析与指标体系
官方 AI 实验室与公司信号
科技圈动态
成本管理与 FinOps
成本数据库与项目财务
```

## 中文优先与个人偏好

`feedback.yaml` 用来调整你的偏好：

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

中文优先采用加权方式，不会丢弃 OpenAI、Anthropic、Google DeepMind 等英文一手信源。

## Twitter/X 来源

`sources.yaml` 已预留以下来源，但默认关闭：

```text
X / Anthropic
X / OpenAI
X / Zara Zhang
```

不建议在 GitHub Actions 里直接硬爬 X 页面。更稳的方式是：

```text
自建 RSSHub
官方 X API
手动维护高价值账号链接
```

等有稳定 RSSHub 地址后，把对应 source 的 `enabled` 改成 `true` 即可。

