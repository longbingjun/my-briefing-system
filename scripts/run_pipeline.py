from __future__ import annotations

import email.utils
import hashlib
import json
import os
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import feedparser
import requests
import yaml


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
PUBLIC_DIR = ROOT / "public"
ARTICLES_PATH = DATA_DIR / "articles.json"
WATCHLIST_PATH = PUBLIC_DIR / "watchlist.json"
DIGEST_PATH = PUBLIC_DIR / "digest-latest.md"

MAX_ARTICLE_AGE_DAYS = 30
MAX_ARTICLES_PER_SOURCE = 30
MAX_ARTICLES_PER_SECTION = 6
MATCH_THRESHOLD = 40
TRANSLATION_BATCH_SIZE = 10
TRANSLATE_MAX_PER_RUN = int(os.environ.get("TRANSLATE_MAX_PER_RUN", "80"))


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    PUBLIC_DIR.mkdir(exist_ok=True)

    config = load_yaml(ROOT / "entities.yaml")
    sources = load_yaml(ROOT / "sources.yaml").get("sources", [])
    feedback = load_yaml(ROOT / "feedback.yaml")
    existing_articles = load_json(ARTICLES_PATH, [])

    fetched_articles = fetch_sources(sources)
    articles = merge_articles(existing_articles, fetched_articles)
    articles = keep_recent_articles(articles)
    articles = enrich_articles_with_chinese(articles)

    entity_payloads = build_entities(config.get("entities", []), articles, feedback)
    domain_payloads = build_domains(config.get("domains", []), entity_payloads)
    watchlist = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "meta": {
            "article_total": len(articles),
            "entity_curated": len(entity_payloads),
            "domain_total": len(domain_payloads),
            "translation_enabled": bool(os.environ.get("OPENAI_API_KEY")),
        },
        "domains": domain_payloads,
        "curated_ids": [entity["entity_id"] for entity in entity_payloads],
        "entities": entity_payloads,
    }

    write_json(ARTICLES_PATH, articles)
    write_json(WATCHLIST_PATH, watchlist)
    DIGEST_PATH.write_text(render_digest(watchlist), encoding="utf-8")


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def fetch_sources(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    articles: list[dict[str, Any]] = []
    for source in sources:
        if source.get("enabled", True) is False:
            continue
        if source.get("type") != "rss":
            continue

        feed = feedparser.parse(source["url"])
        if getattr(feed, "bozo", False):
            print(f"Feed warning: {source.get('name', source['id'])} may be unavailable")

        for entry in feed.entries[:MAX_ARTICLES_PER_SOURCE]:
            title = clean_text(entry.get("title", "Untitled"))
            url = normalize_url(entry.get("link", ""))
            if not url:
                continue

            summary = clean_text(entry.get("summary", "") or entry.get("description", ""))
            article_id = make_article_id(url, title)
            articles.append(
                {
                    "id": article_id,
                    "title": title,
                    "url": url,
                    "source": source.get("name", source["id"]),
                    "source_id": source["id"],
                    "source_group": source.get("group", "general"),
                    "language": source.get("language", "unknown"),
                    "source_weight": float(source.get("weight", 0.7)),
                    "summary": summary,
                    "published_at": parse_entry_date(entry),
                    "fetched_at": datetime.now(timezone.utc).isoformat(),
                }
            )
    return articles


def parse_entry_date(entry: Any) -> str:
    for candidate in [entry.get("published"), entry.get("updated"), entry.get("created")]:
        if not candidate:
            continue
        try:
            parsed = email.utils.parsedate_to_datetime(candidate)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed.astimezone(timezone.utc).isoformat()
        except (TypeError, ValueError):
            continue
    return datetime.now(timezone.utc).isoformat()


def merge_articles(existing: list[dict[str, Any]], fetched: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for article in existing + fetched:
        merged[article["id"]] = article
    return sorted(merged.values(), key=lambda item: item.get("published_at", ""), reverse=True)


def keep_recent_articles(articles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    now = datetime.now(timezone.utc)
    recent = []
    for article in articles:
        try:
            published = datetime.fromisoformat(article["published_at"].replace("Z", "+00:00"))
        except (KeyError, ValueError):
            continue
        if (now - published).days <= MAX_ARTICLE_AGE_DAYS:
            recent.append(article)
    return recent


def enrich_articles_with_chinese(articles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for article in articles:
        if article.get("language") == "zh":
            article["title_zh"] = article.get("title", "")
            article["summary_zh"] = article.get("summary", "")

    candidates = [
        article
        for article in articles
        if article.get("language") != "zh" and not article.get("title_zh")
    ][:TRANSLATE_MAX_PER_RUN]

    if not candidates:
        return articles

    translations = translate_articles_with_openai(candidates)
    for article in candidates:
        translated = translations.get(article["id"])
        if translated:
            article["title_zh"] = translated.get("title_zh") or article.get("title", "")
            article["summary_zh"] = translated.get("summary_zh") or article.get("summary", "")
        else:
            article["title_zh"] = article.get("title", "")
            article["summary_zh"] = article.get("summary", "")
    return articles


def translate_articles_with_openai(articles: list[dict[str, Any]]) -> dict[str, dict[str, str]]:
    if not os.environ.get("OPENAI_API_KEY"):
        return {}

    translated: dict[str, dict[str, str]] = {}
    for index in range(0, len(articles), TRANSLATION_BATCH_SIZE):
        batch = articles[index : index + TRANSLATION_BATCH_SIZE]
        items = [
            {
                "id": article["id"],
                "title": article.get("title", ""),
                "summary": article.get("summary", "")[:700],
            }
            for article in batch
        ]
        prompt = (
            "你是中文 AI 情报编辑。请把下面英文科技资讯翻译成自然、准确、适合中文简报阅读的中文。"
            "标题保留常用英文技术名词，摘要控制在 80 字以内。只返回 JSON 数组，不要 Markdown。"
            "每项格式为 {\"id\":\"...\",\"title_zh\":\"...\",\"summary_zh\":\"...\"}。\n\n"
            f"{json.dumps(items, ensure_ascii=False)}"
        )
        try:
            content = call_openai_text(prompt, max_tokens=2200)
            parsed = json.loads(extract_json_array(content))
            for item in parsed:
                if isinstance(item, dict) and item.get("id"):
                    translated[item["id"]] = {
                        "title_zh": clean_text(item.get("title_zh", "")),
                        "summary_zh": clean_text(item.get("summary_zh", "")),
                    }
        except Exception as error:
            print(f"Translation batch failed: {error}")
    return translated


def build_domains(domains: list[dict[str, Any]], entities: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_domain: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entity in entities:
        by_domain[entity.get("domain", "uncategorized")].append(entity)

    payloads = []
    for domain in domains:
        domain_entities = by_domain.get(domain["id"], [])
        payloads.append(
            {
                "domain_id": domain["id"],
                "name": domain["name"],
                "description": domain.get("description", ""),
                "entity_count": len(domain_entities),
                "article_count": sum(entity["article_count"] for entity in domain_entities),
            }
        )
    return payloads


def build_entities(
    entities: list[dict[str, Any]],
    articles: list[dict[str, Any]],
    feedback: dict[str, Any],
) -> list[dict[str, Any]]:
    payloads = []
    for entity in entities:
        matched = []
        for article in articles:
            score = score_article(entity, article, feedback)
            if score >= MATCH_THRESHOLD:
                matched.append({**article, "score": score})

        matched = sorted(matched, key=lambda item: item["score"], reverse=True)
        if not matched:
            continue

        sections = build_sections(entity, matched)
        payloads.append(
            {
                "entity_id": entity["id"],
                "display": entity["name"],
                "domain": entity.get("domain", "uncategorized"),
                "type": entity.get("type", "Concept"),
                "article_count": len(matched),
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "narrative": {
                    "summary": summarize_entity(entity, matched, sections),
                    "sections": sections,
                },
            }
        )
    return sorted(payloads, key=lambda item: item["article_count"], reverse=True)


def score_article(entity: dict[str, Any], article: dict[str, Any], feedback: dict[str, Any]) -> int:
    haystack = article_text(article).lower()
    keywords = [str(keyword).lower() for keyword in entity.get("keywords", [])]
    hits = sum(1 for keyword in keywords if keyword in haystack)
    if hits == 0:
        return 0

    keyword_score = min(62, 30 + hits * 10)
    source_score = int(float(article.get("source_weight", 0.7)) * 18)
    return max(0, min(100, keyword_score + source_score + freshness_points(article.get("published_at", "")) + feedback_points(article, haystack, feedback)))


def feedback_points(article: dict[str, Any], haystack: str, feedback: dict[str, Any]) -> int:
    points = 0
    language_pref = feedback.get("language_preference", {})
    if article.get("language") == language_pref.get("preferred"):
        points += int(language_pref.get("zh_bonus", 0))

    if article.get("source") in set(feedback.get("favorite_sources", [])):
        points += 8

    boost_hits = sum(1 for keyword in feedback.get("boost_keywords", []) if str(keyword).lower() in haystack)
    mute_hits = sum(1 for keyword in feedback.get("mute_keywords", []) if str(keyword).lower() in haystack)
    points += min(16, boost_hits * 4)
    points -= min(30, mute_hits * 12)
    return points


def freshness_points(published_at: str) -> int:
    try:
        published = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
    except ValueError:
        return 0
    age_days = (datetime.now(timezone.utc) - published).days
    if age_days <= 2:
        return 10
    if age_days <= 7:
        return 6
    if age_days <= 14:
        return 3
    return 0


def build_sections(entity: dict[str, Any], articles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for article in articles:
        buckets[infer_topic(entity, article)].append(article_to_public(article))

    sections = []
    for topic, topic_articles in buckets.items():
        topic_articles = sorted(topic_articles, key=lambda item: item["score"], reverse=True)
        sections.append({"topic": topic, "articles": topic_articles[:MAX_ARTICLES_PER_SECTION]})
    return sorted(sections, key=lambda item: len(item["articles"]), reverse=True)


def infer_topic(entity: dict[str, Any], article: dict[str, Any]) -> str:
    text = article_text(article).lower()
    rules = [
        ("预训练/模型架构", ["pretraining", "pre-training", "scaling law", "architecture", "moe", "预训练", "模型架构"]),
        ("后训练/对齐", ["post-training", "alignment", "rlhf", "dpo", "sft", "后训练", "对齐", "微调"]),
        ("推理训练/测试时计算", ["reasoning", "test-time", "inference-time", "grpo", "verifier", "推理训练", "强化学习", "测试时计算"]),
        ("评测/安全", ["benchmark", "eval", "safety", "red team", "jailbreak", "system card", "评测", "安全", "红队"]),
        ("Agent 工作流", ["agent", "tool use", "workflow", "claude code", "codex", "mcp", "智能体", "工具调用", "工作流"]),
        ("AI 基础设施", ["gpu", "inference", "serving", "quantization", "distillation", "cuda", "算力", "推理服务", "量化", "蒸馏"]),
        ("产品发布", ["release", "launch", "announce", "beta", "发布", "上线", "推出"]),
        ("开源动态", ["open source", "github", "license", "model weights", "开源"]),
        ("成本与效率", ["cost", "pricing", "token", "budget", "finops", "成本", "预算", "效率"]),
        ("数据与指标", ["data", "analytics", "metric", "dashboard", "kpi", "数据", "指标", "看板"]),
        ("官方/科技圈信号", ["twitter", "x.com", "official", "founder", "researcher", "官方", "科技圈", "融资"]),
        ("行业改造", ["enterprise", "workflow", "automation", "finance", "manufacturing", "supply chain", "企业", "自动化", "制造", "供应链"]),
    ]
    for topic, terms in rules:
        if any(term in text for term in terms):
            return topic
    return entity["name"]


def article_to_public(article: dict[str, Any]) -> dict[str, Any]:
    title = article.get("title_zh") or article["title"]
    summary = article.get("summary_zh") or article.get("summary", "")
    return {
        "title": title,
        "title_original": article["title"],
        "summary": summary,
        "url": article["url"],
        "link": article["url"],
        "source": article["source"],
        "source_group": article.get("source_group", "general"),
        "language": article.get("language", "unknown"),
        "date": format_date(article.get("published_at", "")),
        "score": article["score"],
        "actionability": infer_actionability(article),
    }


def infer_actionability(article: dict[str, Any]) -> int:
    text = article_text(article).lower()
    score = 35
    if any(term in text for term in ["how to", "guide", "tutorial", "cookbook", "framework", "方法", "教程", "实践", "框架"]):
        score += 30
    if any(term in text for term in ["github", "open source", "api", "sdk", "release", "开源", "工具", "模板"]):
        score += 20
    if any(term in text for term in ["funding", "融资", "估值"]):
        score -= 15
    return max(0, min(100, score))


def summarize_entity(entity: dict[str, Any], articles: list[dict[str, Any]], sections: list[dict[str, Any]]) -> str:
    ai_summary = summarize_with_openai(entity, articles, sections)
    if ai_summary:
        return ai_summary

    top_topics = "、".join(section["topic"] for section in sections[:3])
    top_article = articles[0].get("title_zh") or articles[0]["title"]
    return f"{entity['name']} 本期匹配 {len(articles)} 篇文章，重点集中在 {top_topics}。建议先看「{top_article}」。"


def summarize_with_openai(
    entity: dict[str, Any],
    articles: list[dict[str, Any]],
    sections: list[dict[str, Any]],
) -> str | None:
    if not os.environ.get("OPENAI_API_KEY"):
        return None

    titles = "\n".join(f"- [{item['score']}] {item.get('title_zh') or item['title']}" for item in articles[:12])
    topics = ", ".join(section["topic"] for section in sections[:5])
    prompt = (
        "你是中文 AI 情报简报编辑。请基于文章标题，用一句中文总结该实体最近值得关注的趋势。"
        "不要泛泛而谈，要指出具体方向、技术阶段或应用场景。控制在 90 字以内。\n\n"
        f"实体：{entity['name']}\n主题：{topics}\n文章：\n{titles}"
    )

    try:
        return call_openai_text(prompt, max_tokens=220).strip()
    except Exception as error:
        print(f"OpenAI summary failed for {entity['id']}: {error}")
        return None


def call_openai_text(prompt: str, max_tokens: int) -> str:
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={
            "model": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "max_tokens": max_tokens,
        },
        timeout=45,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def extract_json_array(value: str) -> str:
    value = value.strip()
    if value.startswith("```"):
        value = re.sub(r"^```(?:json)?", "", value).strip()
        value = re.sub(r"```$", "", value).strip()
    start = value.find("[")
    end = value.rfind("]")
    if start == -1 or end == -1 or end < start:
        raise ValueError("OpenAI response does not contain a JSON array")
    return value[start : end + 1]


def render_digest(watchlist: dict[str, Any]) -> str:
    date_label = datetime.now().strftime("%m-%d")
    translation_status = "已启用" if watchlist["meta"].get("translation_enabled") else "未启用"
    lines = [
        f"# DISTILLED · {date_label}",
        "",
        f"中文优先 · 研究前沿 · 官方信号 · 行业改造 · 翻译摘要：{translation_status}",
        "",
        f"{watchlist['meta']['article_total']} articles · {watchlist['meta']['entity_curated']} entities · {watchlist['meta']['domain_total']} domains",
        "",
        "━━━ DOMAINS ━━━",
        "",
    ]

    for domain in watchlist.get("domains", []):
        lines.append(f"- {domain['name']}：{domain['article_count']} articles / {domain['entity_count']} entities")

    lines.extend(["", "━━━ WATCHING ━━━", ""])

    for entity in watchlist["entities"]:
        lines.extend(
            [
                f"## ◆ {entity['display']} [{entity['type']}] {entity['article_count']} articles",
                "",
                entity["narrative"]["summary"],
                "",
            ]
        )
        for section in entity["narrative"]["sections"]:
            lines.extend([f"### ── {section['topic']} ({len(section['articles'])}) ──", ""])
            for article in section["articles"]:
                lines.extend(
                    [
                        f"- [{article['score']}] [{article['title']}]({article['url']})",
                        f"  {article['source']} · {article['date']} · actionability {article['actionability']}",
                    ]
                )
                if article.get("title_original") and article["title_original"] != article["title"]:
                    lines.append(f"  原题：{article['title_original']}")
                if article.get("summary"):
                    lines.append(f"  摘要：{article['summary']}")
            lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def clean_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def article_text(article: dict[str, Any]) -> str:
    return " ".join(
        [
            article.get("title", ""),
            article.get("summary", ""),
            article.get("title_zh", ""),
            article.get("summary_zh", ""),
        ]
    )


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url:
        return ""
    return re.sub(r"([?&])utm_[^=&]+=[^&]+&?", r"\1", url).rstrip("?&")


def make_article_id(url: str, title: str) -> str:
    return hashlib.sha256(f"{url}|{title}".encode("utf-8")).hexdigest()[:16]


def format_date(value: str) -> str:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%Y-%m-%d")
    except ValueError:
        return ""


if __name__ == "__main__":
    main()
