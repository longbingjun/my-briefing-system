from __future__ import annotations

import email.utils
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import feedparser
import requests
import yaml


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
PUBLIC_DIR = ROOT / "public"
LISTS_DIR = PUBLIC_DIR / "lists"
ARTICLES_PATH = DATA_DIR / "articles.json"
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
    LISTS_DIR.mkdir(exist_ok=True)

    config = load_yaml(ROOT / "entities.yaml")
    sources = load_yaml(ROOT / "sources.yaml").get("sources", [])
    feedback = load_yaml(ROOT / "feedback.yaml")
    existing_articles = load_json(ARTICLES_PATH, [])

    fetched_articles = fetch_sources(sources)
    articles = keep_recent_articles(merge_articles(existing_articles, fetched_articles))
    articles = enrich_articles_with_chinese(articles)

    entities = build_entities(config.get("entities", []), articles, feedback)
    domains = build_domains(config.get("domains", []), entities)
    all_public_articles = collect_public_articles(entities)
    boards = build_boards(all_public_articles)
    today = build_today_payload(articles, entities, boards)
    watchlist = build_watchlist_payload(config, domains, entities)
    sources_payload = build_sources_payload(sources, articles, all_public_articles)
    article_details = build_article_details(all_public_articles)

    write_json(ARTICLES_PATH, articles)
    write_json(LISTS_DIR / "today.json", today)
    write_json(LISTS_DIR / "watchlist.json", watchlist)
    write_json(LISTS_DIR / "boards.json", boards)
    write_json(LISTS_DIR / "sources.json", sources_payload)
    write_json(LISTS_DIR / "article_details.json", article_details)

    # Compatibility with the first version of this project.
    write_json(PUBLIC_DIR / "watchlist.json", watchlist)
    DIGEST_PATH.write_text(render_digest(today, watchlist, boards), encoding="utf-8")
    (PUBLIC_DIR / "llms.txt").write_text(render_llms(today, watchlist, compact=True), encoding="utf-8")
    (PUBLIC_DIR / "llms-full.txt").write_text(render_llms(today, watchlist, compact=False), encoding="utf-8")


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
        if source.get("enabled", True) is False or source.get("type") != "rss":
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
            articles.append(
                {
                    "id": make_article_id(url, title),
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
        published = parse_iso(article.get("published_at"))
        if published and (now - published).days <= MAX_ARTICLE_AGE_DAYS:
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

    translations = translate_articles(candidates)
    for article in candidates:
        translated = translations.get(article["id"])
        article["title_zh"] = clean_text((translated or {}).get("title_zh") or article.get("title", ""))
        article["summary_zh"] = clean_text((translated or {}).get("summary_zh") or article.get("summary", ""))
    return articles


def translate_articles(articles: list[dict[str, Any]]) -> dict[str, dict[str, str]]:
    if not llm_enabled():
        return {}

    translated: dict[str, dict[str, str]] = {}
    for index in range(0, len(articles), TRANSLATION_BATCH_SIZE):
        batch = articles[index : index + TRANSLATION_BATCH_SIZE]
        items = [
            {"id": article["id"], "title": article.get("title", ""), "summary": article.get("summary", "")[:700]}
            for article in batch
        ]
        prompt = (
            "你是中文 AI 简报编辑。请把下面英文科技资讯翻译成自然、准确、适合中文简报阅读的中文。"
            "标题保留常用英文技术名词，摘要控制在 80 字以内。只返回 JSON 数组，不要 Markdown。"
            "每项格式为 {\"id\":\"...\",\"title_zh\":\"...\",\"summary_zh\":\"...\"}。\n\n"
            f"{json.dumps(items, ensure_ascii=False)}"
        )
        try:
            content = call_llm_text(prompt, max_tokens=2200)
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
                matched.append({**article, "score": score, "entity_id": entity["id"], "entity": entity["name"]})
        if not matched:
            continue

        matched = sorted(matched, key=lambda item: (item["score"], item.get("published_at", "")), reverse=True)
        sections = build_sections(entity, matched)
        today_count = count_since(matched, days=1)
        last7 = count_since(matched, days=7)
        prev7 = count_between(matched, start_days=14, end_days=7)
        payloads.append(
            {
                "entity_id": entity["id"],
                "display": entity["name"],
                "domain": entity.get("domain", "uncategorized"),
                "type": entity.get("type", "Concept"),
                "pinned": bool(entity.get("pinned")),
                "article_count": len(matched),
                "articles_7d": last7,
                "prev_7d": prev7,
                "today_count": today_count,
                "direction": trend_direction(last7, prev7),
                "history_30d": history_30d(matched),
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "narrative": {
                    "summary": summarize_entity(entity, matched, sections),
                    "sections": sections,
                },
            }
        )
    return sorted(payloads, key=lambda item: (item["pinned"], item["articles_7d"], item["article_count"]), reverse=True)


def score_article(entity: dict[str, Any], article: dict[str, Any], feedback: dict[str, Any]) -> int:
    haystack = article_text(article).lower()
    keywords = [str(keyword).lower() for keyword in entity.get("keywords", [])]
    hits = sum(1 for keyword in keywords if keyword in haystack)
    if hits == 0:
        return 0

    keyword_score = min(62, 30 + hits * 10)
    source_score = int(float(article.get("source_weight", 0.7)) * 18)
    score = keyword_score + source_score + freshness_points(article.get("published_at", "")) + feedback_points(article, haystack, feedback)
    return max(0, min(100, score))


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
    published = parse_iso(published_at)
    if not published:
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
    return sorted(sections, key=lambda item: max(article["score"] for article in item["articles"]), reverse=True)


def infer_topic(entity: dict[str, Any], article: dict[str, Any]) -> str:
    text = article_text(article).lower()
    rules = [
        ("预训练/模型架构", ["pretraining", "pre-training", "scaling law", "architecture", "moe", "预训练", "模型架构"]),
        ("后训练/对齐", ["post-training", "alignment", "rlhf", "dpo", "sft", "后训练", "对齐", "微调"]),
        ("推理训练/测试时计算", ["reasoning", "test-time", "inference-time", "grpo", "verifier", "推理训练", "强化学习"]),
        ("评测/安全", ["benchmark", "eval", "safety", "red team", "jailbreak", "system card", "评测", "安全", "红队"]),
        ("Agent 工作流", ["agent", "tool use", "workflow", "claude code", "codex", "mcp", "智能体", "工具调用", "工作流"]),
        ("AI 基础设施", ["gpu", "inference", "serving", "quantization", "distillation", "cuda", "算力", "推理服务", "量化", "蒸馏"]),
        ("产品发布", ["release", "launch", "announce", "beta", "发布", "上线", "推出"]),
        ("开源动态", ["open source", "github", "license", "model weights", "开源"]),
        ("成本与效率", ["cost", "pricing", "token", "budget", "finops", "成本", "预算", "效率"]),
        ("数据与指标", ["data", "analytics", "metric", "dashboard", "kpi", "数据", "指标", "看板"]),
        ("官方/科技圈信号", ["twitter", "x.com", "official", "founder", "researcher", "官方", "科技圈", "融资"]),
        ("行业改造", ["enterprise", "automation", "finance", "manufacturing", "supply chain", "企业", "自动化", "制造", "供应链"]),
    ]
    for topic, terms in rules:
        if any(term in text for term in terms):
            return topic
    return entity["name"]


def article_to_public(article: dict[str, Any]) -> dict[str, Any]:
    title = article.get("title_zh") or article["title"]
    summary = article.get("summary_zh") or article.get("summary", "")
    return {
        "id": article["id"],
        "title": title,
        "title_original": article["title"],
        "summary": summary,
        "url": article["url"],
        "link": article["url"],
        "source": article["source"],
        "source_id": article.get("source_id", ""),
        "source_group": article.get("source_group", "general"),
        "language": article.get("language", "unknown"),
        "date": format_date(article.get("published_at", "")),
        "published_at": article.get("published_at", ""),
        "score": article["score"],
        "entity_id": article.get("entity_id"),
        "entity": article.get("entity"),
        "kind": infer_kind(article),
        "actionability": infer_actionability(article),
        "minutes": estimate_minutes(article),
    }


def collect_public_articles(entities: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for entity in entities:
        for section in entity.get("narrative", {}).get("sections", []):
            for article in section.get("articles", []):
                current = by_id.get(article["id"])
                if not current or article["score"] > current["score"]:
                    by_id[article["id"]] = {**article, "topic": section.get("topic", "")}
    return sorted(by_id.values(), key=lambda item: (item["score"], item.get("published_at", "")), reverse=True)


def build_today_payload(
    raw_articles: list[dict[str, Any]],
    entities: list[dict[str, Any]],
    boards: dict[str, Any],
) -> dict[str, Any]:
    picks = [item for item in boards["boards"]["read"]["items"] if item["score"] >= 60][:7]
    if len(picks) < 7:
        extras = [item for item in boards["boards"]["learn"]["items"] if item["id"] not in {pick["id"] for pick in picks}]
        picks.extend(extras[: 7 - len(picks)])

    source_count = len({article.get("source_id") or article.get("source") for article in raw_articles})
    total_scanned = len(raw_articles)
    est_read_minutes = max(1, sum(item.get("minutes", 3) for item in picks))
    saved_hours = round(max(0, total_scanned * 2.5 / 60 - est_read_minutes / 60), 1)

    paragraphs = build_daily_paragraphs(entities, picks)
    entity_moves = [
        {
            "entity_id": entity["entity_id"],
            "display": entity["display"],
            "articles_7d": entity["articles_7d"],
            "direction": entity["direction"],
            "today_count": entity["today_count"],
        }
        for entity in entities[:8]
    ]

    return {
        "version": 1,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "edition": os.environ.get("BRIEFING_EDITION", "daily"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "funnel": {
            "sources_active": source_count,
            "total_scanned": total_scanned,
            "picks_count": len(picks),
            "est_read_minutes": est_read_minutes,
            "est_saved_hours": saved_hours,
        },
        "daily_brief": paragraphs[0]["text"] if paragraphs else "今天还没有足够内容生成导读。",
        "daily_digest": {
            "paragraphs": paragraphs,
            "citations": build_citations(picks),
            "entity_moves": entity_moves,
            "skip_note": "低分、重复或与长期关注领域弱相关的内容会进入忽略，不展示在今日导读里。",
            "word_count": sum(len(item["text"]) for item in paragraphs),
        },
        "picks": picks,
        "trending": build_trending(raw_articles),
        "quality": {
            "scored": len(boards.get("_all_articles", [])),
            "must_read_count": len([item for item in boards.get("_all_articles", []) if item["score"] >= 70]),
            "avg_score": round(avg([item["score"] for item in boards.get("_all_articles", [])]), 1),
        },
    }


def build_daily_paragraphs(entities: list[dict[str, Any]], picks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    paragraphs = []
    for entity in entities[:3]:
        summary = entity.get("narrative", {}).get("summary", "")
        if not summary:
            continue
        paragraphs.append(
            {
                "lead": entity["display"],
                "entity": entity["entity_id"],
                "text": summary,
                "xhs_caption": {
                    "title": f"{entity['display']} 本期值得关注",
                    "body": f"{summary}\n\n我会继续追踪这个方向的官方信源、技术文章和产品变化。",
                    "tags": ["AI简报", entity["display"], "科技趋势"],
                },
            }
        )
    if not paragraphs and picks:
        paragraphs.append({"lead": "今日导读", "text": picks[0].get("summary") or picks[0]["title"]})
    return paragraphs


def build_citations(picks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "n": index + 1,
            "link": item["url"],
            "title": item["title"],
            "source": item["source"],
            "score": item["score"],
            "minutes": item.get("minutes", 3),
        }
        for index, item in enumerate(picks)
    ]


def build_boards(articles: list[dict[str, Any]]) -> dict[str, Any]:
    boards = {
        "learn": {"label": "学啥", "items": []},
        "read": {"label": "读啥", "items": []},
        "do": {"label": "做啥", "items": []},
        "skip": {"label": "忽略", "items": []},
    }
    for article in articles:
        board = article["kind"]
        boards[board]["items"].append(article)
    for board in boards.values():
        board["items"] = sorted(board["items"], key=lambda item: item["score"], reverse=True)[:80]
        board["count"] = len(board["items"])
    return {
        "version": 1,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "window": "30d",
        "total_articles": len(articles),
        "source_count": len({article["source_id"] or article["source"] for article in articles}),
        "boards": boards,
        "_all_articles": articles,
    }


def build_watchlist_payload(config: dict[str, Any], domains: list[dict[str, Any]], entities: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "version": 1,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "window": "30d",
        "meta": {
            "article_total": sum(entity["article_count"] for entity in entities),
            "entity_curated": len(entities),
            "domain_total": len(domains),
            "translation_enabled": llm_enabled(),
            "llm_model": llm_model(),
        },
        "domains": domains,
        "default_pins": [entity["id"] for entity in config.get("entities", []) if entity.get("pinned")],
        "curated_ids": [entity["entity_id"] for entity in entities],
        "entities": entities,
    }


def build_sources_payload(
    configured_sources: list[dict[str, Any]],
    raw_articles: list[dict[str, Any]],
    public_articles: list[dict[str, Any]],
) -> dict[str, Any]:
    raw_by_source = Counter(article.get("source_id") for article in raw_articles)
    public_by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for article in public_articles:
        public_by_source[article.get("source_id")].append(article)

    all_sources = []
    for source in configured_sources:
        sid = source["id"]
        selected = public_by_source.get(sid, [])
        scores = [item["score"] for item in selected]
        all_sources.append(
            {
                "id": sid,
                "name": source.get("name", sid),
                "group": source.get("group", "general"),
                "language": source.get("language", "unknown"),
                "enabled": source.get("enabled", True) is not False,
                "url": source.get("url", ""),
                "weight": source.get("weight", 0.7),
                "scanned_30d": raw_by_source.get(sid, 0),
                "selected_30d": len(selected),
                "today_count": count_since(selected, days=1),
                "avg_score": round(avg(scores), 1),
                "quality_index": round(avg(scores) * 0.7 + min(30, len(selected) * 2), 1) if selected else 0,
                "style_tags": infer_source_tags(source),
                "top_articles": selected[:3],
            }
        )
    all_sources = sorted(all_sources, key=lambda item: (item["enabled"], item["quality_index"], item["selected_30d"]), reverse=True)
    return {
        "version": 1,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "today": {
            "articles": len([article for article in raw_articles if is_since(article, 1)]),
            "active_sources": len([source for source in all_sources if source["enabled"] and source["scanned_30d"] > 0]),
            "avg_score": round(avg([source["avg_score"] for source in all_sources if source["avg_score"]]), 1),
        },
        "pinned_sources": [source for source in all_sources if source["group"] in {"official", "x_official"}][:10],
        "highlights": all_sources[:8],
        "fun_facts": [
            f"当前启用 {len([source for source in all_sources if source['enabled']])} 个信源。",
            "X/Twitter 信源建议通过自建 RSSHub 或官方 API 接入，避免 GitHub Actions 直接爬页面。",
        ],
        "all_sources": all_sources,
    }


def build_article_details(articles: list[dict[str, Any]]) -> dict[str, Any]:
    details = {}
    for article in articles:
        if article["score"] < 60:
            continue
        details[article["id"]] = {
            **article,
            "why_important": infer_why_important(article),
            "highlights": infer_highlights(article),
            "get_started": infer_get_started(article),
        }
    return {
        "version": 1,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(details),
        "articles": details,
    }


def build_trending(articles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    stopwords = {"the", "and", "for", "with", "from", "this", "that", "your", "into", "about", "using"}
    words: Counter[str] = Counter()
    sources: dict[str, set[str]] = defaultdict(set)
    for article in articles:
        text = article_text(article).lower()
        for word in re.findall(r"[a-zA-Z][a-zA-Z0-9\-]{2,}|[\u4e00-\u9fff]{2,}", text):
            if word in stopwords or len(word) > 30:
                continue
            words[word] += 1
            sources[word].add(article.get("source_id") or article.get("source", ""))
    return [
        {"keyword": word, "mention_count": count, "source_count": len(sources[word])}
        for word, count in words.most_common(20)
    ]


def summarize_entity(entity: dict[str, Any], articles: list[dict[str, Any]], sections: list[dict[str, Any]]) -> str:
    ai_summary = summarize_with_llm(entity, articles, sections)
    if ai_summary:
        return ai_summary

    top_topics = "、".join(section["topic"] for section in sections[:3])
    top_article = articles[0].get("title_zh") or articles[0]["title"]
    return f"{entity['name']} 本期匹配 {len(articles)} 篇文章，重点集中在 {top_topics}。建议先看《{top_article}》。"


def summarize_with_llm(entity: dict[str, Any], articles: list[dict[str, Any]], sections: list[dict[str, Any]]) -> str | None:
    if not llm_enabled():
        return None
    titles = "\n".join(f"- [{item['score']}] {item.get('title_zh') or item['title']}" for item in articles[:12])
    topics = ", ".join(section["topic"] for section in sections[:5])
    prompt = (
        "你是中文 AI 情报简报编辑。请基于文章标题，用一句中文总结该实体最近值得关注的趋势。"
        "不要泛泛而谈，要指出具体技术阶段、产品方向或应用场景。控制在 90 字以内。\n\n"
        f"实体：{entity['name']}\n主题：{topics}\n文章：\n{titles}"
    )
    try:
        return call_llm_text(prompt, max_tokens=220).strip()
    except Exception as error:
        print(f"LLM summary failed for {entity['id']}: {error}")
        return None


def call_llm_text(prompt: str, max_tokens: int) -> str:
    base_url = os.environ.get("LLM_BASE_URL", os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")).rstrip("/")
    api_key = os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("LLM_API_KEY or OPENAI_API_KEY is required")
    response = requests.post(
        f"{base_url}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": llm_model(),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "max_tokens": max_tokens,
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def llm_enabled() -> bool:
    return bool(os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY"))


def llm_model() -> str:
    return os.environ.get("LLM_MODEL") or os.environ.get("OPENAI_MODEL") or "gpt-4o-mini"


def infer_kind(article: dict[str, Any]) -> str:
    text = article_text(article).lower()
    actionability = infer_actionability(article)
    if article["score"] < 50:
        return "skip"
    if actionability >= 70:
        return "do"
    if any(term in text for term in ["paper", "arxiv", "research", "benchmark", "eval", "预训练", "后训练", "推理训练", "评测"]):
        return "learn"
    return "read"


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


def infer_why_important(article: dict[str, Any]) -> str:
    if article.get("entity"):
        return f"这篇内容被归入「{article['entity']}」，分数 {article['score']}，与当前长期关注领域相关度较高。"
    return f"这篇内容分数 {article['score']}，适合作为本期 AI 情报的补充阅读。"


def infer_highlights(article: dict[str, Any]) -> list[str]:
    summary = article.get("summary", "")
    if not summary:
        return [article["title"]]
    chunks = re.split(r"[。.!?；;]", summary)
    return [chunk.strip() for chunk in chunks if chunk.strip()][:3] or [summary[:120]]


def infer_get_started(article: dict[str, Any]) -> str:
    if article["kind"] == "do":
        return "先打开原文，提取可复用步骤、工具链接或配置方法，再记录到你的个人流程库。"
    if article["kind"] == "learn":
        return "先读摘要和结论，再把关键概念补进对应实体卡片。"
    return "先判断它是否影响你的长期关注领域，再决定是否加入下一期选题。"


def infer_source_tags(source: dict[str, Any]) -> list[str]:
    tags = [source.get("group", "general"), source.get("language", "unknown")]
    if source.get("weight", 0) >= 0.9:
        tags.append("high-signal")
    if source.get("enabled", True) is False:
        tags.append("disabled")
    return tags


def estimate_minutes(article: dict[str, Any]) -> int:
    words = len(re.findall(r"\w+|[\u4e00-\u9fff]", article_text(article)))
    return max(1, min(8, round(words / 350) + 1))


def render_digest(today: dict[str, Any], watchlist: dict[str, Any], boards: dict[str, Any]) -> str:
    lines = [
        f"# My Briefing · {today['date']}",
        "",
        f"{today['funnel']['sources_active']} 个活跃信源 -> {today['funnel']['total_scanned']} 条扫描 -> {today['funnel']['picks_count']} 条今日值得看",
        f"预计阅读 {today['funnel']['est_read_minutes']} 分钟，节省约 {today['funnel']['est_saved_hours']} 小时。",
        "",
        "## 今日导读",
        "",
    ]
    for paragraph in today["daily_digest"]["paragraphs"]:
        lines.append(f"- **{paragraph['lead']}**：{paragraph['text']}")
    lines.extend(["", "## 今日值得看", ""])
    for item in today["picks"]:
        lines.append(f"- [{item['score']}] [{item['title']}]({item['url']}) · {item['source']} · {item['minutes']} min")
        if item.get("summary"):
            lines.append(f"  {item['summary']}")
    lines.extend(["", "## 实体追踪", ""])
    for entity in watchlist["entities"][:12]:
        lines.append(f"- {entity['display']}：本周 {entity['articles_7d']}，今日 +{entity['today_count']}，{entity['narrative']['summary']}")
    lines.extend(["", "## 内容分栏", ""])
    for board_id, board in boards["boards"].items():
        lines.append(f"- {board['label']}：{board['count']} 篇")
    return "\n".join(lines)


def render_llms(today: dict[str, Any], watchlist: dict[str, Any], compact: bool) -> str:
    lines = [
        "# My Briefing for LLMs",
        "",
        f"Date: {today['date']}",
        f"Funnel: {today['funnel']['sources_active']} sources, {today['funnel']['total_scanned']} scanned, {today['funnel']['picks_count']} picks",
        "",
        "## Daily Brief",
        today.get("daily_brief", ""),
        "",
        "## Top Picks",
    ]
    for item in today["picks"][: 5 if compact else 20]:
        lines.append(f"- [{item['score']}] {item['title']} ({item['source']}) {item['url']}")
        if not compact and item.get("summary"):
            lines.append(f"  Summary: {item['summary']}")
    lines.extend(["", "## Entities"])
    for entity in watchlist["entities"][: 8 if compact else 30]:
        lines.append(f"- {entity['display']}: {entity['narrative']['summary']}")
    return "\n".join(lines)


def extract_json_array(value: str) -> str:
    value = value.strip()
    if value.startswith("```"):
        value = re.sub(r"^```(?:json)?", "", value).strip()
        value = re.sub(r"```$", "", value).strip()
    start = value.find("[")
    end = value.rfind("]")
    if start == -1 or end == -1 or end < start:
        raise ValueError("LLM response does not contain a JSON array")
    return value[start : end + 1]


def clean_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", str(value))
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def article_text(article: dict[str, Any]) -> str:
    return " ".join([article.get("title", ""), article.get("summary", ""), article.get("title_zh", ""), article.get("summary_zh", "")])


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url:
        return ""
    return re.sub(r"([?&])utm_[^=&]+=[^&]+&?", r"\1", url).rstrip("?&")


def make_article_id(url: str, title: str) -> str:
    return hashlib.sha256(f"{url}|{title}".encode("utf-8")).hexdigest()[:16]


def format_date(value: str) -> str:
    parsed = parse_iso(value)
    return parsed.strftime("%Y-%m-%d") if parsed else ""


def parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except ValueError:
        return None


def is_since(article: dict[str, Any], days: int) -> bool:
    published = parse_iso(article.get("published_at"))
    return bool(published and datetime.now(timezone.utc) - published <= timedelta(days=days))


def count_since(articles: list[dict[str, Any]], days: int) -> int:
    return sum(1 for article in articles if is_since(article, days))


def count_between(articles: list[dict[str, Any]], start_days: int, end_days: int) -> int:
    now = datetime.now(timezone.utc)
    count = 0
    for article in articles:
        published = parse_iso(article.get("published_at"))
        if published and timedelta(days=end_days) < now - published <= timedelta(days=start_days):
            count += 1
    return count


def trend_direction(current: int, previous: int) -> str:
    if current > previous:
        return "up"
    if current < previous:
        return "down"
    return "flat"


def history_30d(articles: list[dict[str, Any]]) -> list[int]:
    today = datetime.now(timezone.utc).date()
    buckets = {today - timedelta(days=offset): 0 for offset in range(29, -1, -1)}
    for article in articles:
        published = parse_iso(article.get("published_at"))
        if published and published.date() in buckets:
            buckets[published.date()] += 1
    return list(buckets.values())


def avg(values: list[float | int]) -> float:
    return sum(values) / len(values) if values else 0


if __name__ == "__main__":
    main()
