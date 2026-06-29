const state = {
  today: null,
  watchlist: null,
  boards: null,
  sources: null,
  articleDetails: null,
  board: "all",
};

const routeTitles = {
  today: "今日",
  watch: "实体",
  content: "内容",
  sources: "信源",
  api: "开放数据 API",
  story: "项目背后",
};

async function fetchJson(path) {
  const response = await fetch(path, { cache: "no-store" });
  if (!response.ok) throw new Error(`${path} ${response.status}`);
  return response.json();
}

async function loadData() {
  const [today, watchlist, boards, sources, articleDetails] = await Promise.all([
    fetchJson("./lists/today.json"),
    fetchJson("./lists/watchlist.json"),
    fetchJson("./lists/boards.json"),
    fetchJson("./lists/sources.json"),
    fetchJson("./lists/article_details.json"),
  ]);
  Object.assign(state, { today, watchlist, boards, sources, articleDetails });
}

function currentRoute() {
  return (location.hash || "#today").replace("#", "") || "today";
}

function setHeader(route) {
  document.getElementById("pageTitle").textContent = routeTitles[route] || "My Briefing";
  const generated = state.today?.generated_at ? new Date(state.today.generated_at).toLocaleString("zh-CN") : "";
  const funnel = state.today?.funnel;
  document.getElementById("pageMeta").textContent = funnel
    ? `${state.today.date} · ${funnel.sources_active} 信源 · ${funnel.total_scanned} 扫描 · ${funnel.picks_count} 值得看 · ${generated} 更新`
    : "正在加载...";
  document.querySelectorAll("[data-route]").forEach((item) => {
    item.classList.toggle("active", item.dataset.route === route);
  });
}

function render() {
  const route = currentRoute();
  setHeader(route);
  const view = document.getElementById("view");
  if (route === "watch") view.innerHTML = renderWatch();
  else if (route === "content") view.innerHTML = renderContent();
  else if (route === "sources") view.innerHTML = renderSources();
  else if (route === "api") view.innerHTML = renderApi();
  else if (route === "story") view.innerHTML = renderStory();
  else view.innerHTML = renderToday();
  bindContentTabs();
  bindCopyButtons();
}

function renderToday() {
  const { today } = state;
  const f = today.funnel;
  return `
    <section class="hero-grid">
      <div class="intro">
        <p class="eyebrow">每天替你读完 AI 信息，只保留值得看的几条</p>
        <h2>${escapeHtml(today.daily_brief || "今日简报")}</h2>
        <p>当前版本按长期关注领域、实体主题、文章主题三层组织信息，并优先生成中文标题与摘要。</p>
      </div>
      <aside class="funnel">
        <div><strong>${f.sources_active}</strong><span>信源</span></div>
        <div><strong>${f.total_scanned}</strong><span>累计扫描</span></div>
        <div><strong>${f.picks_count}</strong><span>今日值得看</span></div>
        <div class="bar"><span style="width:${Math.min(100, f.picks_count * 12)}%"></span></div>
        <p>读完约 ${f.est_read_minutes} 分钟，预计节省 ${f.est_saved_hours} 小时。</p>
      </aside>
    </section>

    <section class="content-grid">
      <div>
        <section class="panel">
          <header class="panel-head"><h3>今日导读</h3><span>${today.daily_digest.word_count || 0} 字</span></header>
          ${today.daily_digest.paragraphs.map(renderDigestParagraph).join("")}
        </section>
      </div>
      <aside class="side-stack">
        <section class="panel">
          <header class="panel-head"><h3>今日值得看</h3><span>${today.picks.length}</span></header>
          ${today.picks.map(renderCompactArticle).join("")}
        </section>
        <section class="panel">
          <header class="panel-head"><h3>实体动向</h3><span>30 天窗口</span></header>
          ${today.daily_digest.entity_moves.map(renderMove).join("")}
        </section>
      </aside>
    </section>
  `;
}

function renderDigestParagraph(item) {
  const caption = item.xhs_caption
    ? `<button class="copy-btn" data-copy="${escapeAttr(`${item.xhs_caption.title}\n\n${item.xhs_caption.body}\n\n#${item.xhs_caption.tags.join(" #")}`)}">复制小红书文案</button>`
    : "";
  return `<article class="digest-block"><h4>${escapeHtml(item.lead)}</h4><p>${escapeHtml(item.text)}</p>${caption}</article>`;
}

function renderWatch() {
  const pinned = state.watchlist.entities.filter((item) => item.pinned);
  const others = state.watchlist.entities.filter((item) => !item.pinned);
  return `
    <section class="panel">
      <header class="panel-head"><h3>我的关注 · ${pinned.length}</h3><span>${state.watchlist.window}</span></header>
      ${pinned.map(renderEntityRow).join("")}
    </section>
    <section class="panel">
      <header class="panel-head"><h3>其他追踪 · ${others.length}</h3><span>自动匹配</span></header>
      ${others.map(renderEntityRow).join("")}
    </section>
  `;
}

function renderEntityRow(entity) {
  return `
    <article class="entity-row">
      <div class="entity-title">
        <strong>${escapeHtml(entity.display)}</strong>
        <span>${escapeHtml(entity.type)}</span>
      </div>
      <div class="entity-numbers">本周 ${entity.articles_7d} · 今日 +${entity.today_count}</div>
      <div class="spark">${(entity.history_30d || []).map((value) => `<i style="height:${Math.max(3, value * 7)}px"></i>`).join("")}</div>
      <p>${escapeHtml(entity.narrative?.summary || "")}</p>
    </article>
  `;
}

function renderContent() {
  const all = state.boards._all_articles || [];
  const boardItems = state.board === "all" ? all : state.boards.boards[state.board]?.items || [];
  return `
    <div class="tabs">
      ${renderTab("all", `全部 ${all.length}`)}
      ${renderTab("learn", `学啥 ${state.boards.boards.learn.count}`)}
      ${renderTab("read", `读啥 ${state.boards.boards.read.count}`)}
      ${renderTab("do", `做啥 ${state.boards.boards.do.count}`)}
      ${renderTab("skip", `忽略 ${state.boards.boards.skip.count}`)}
    </div>
    <section class="content-grid">
      <div class="panel article-panel">
        ${boardItems.map(renderArticle).join("") || "<p class='empty'>暂无内容。</p>"}
      </div>
      <aside class="side-stack">
        <section class="panel">
          <header class="panel-head"><h3>筛选</h3><span>规则生成</span></header>
          <p class="muted">分栏由分数、行动性、研究关键词和来源质量自动决定。60 分以上会进入文章详情 JSON。</p>
        </section>
        <section class="panel">
          <header class="panel-head"><h3>本页统计</h3><span>${state.boards.window}</span></header>
          <p>近 30 天 ${state.boards.total_articles} 篇，覆盖 ${state.boards.source_count} 个信源。</p>
        </section>
      </aside>
    </section>
  `;
}

function renderTab(id, label) {
  return `<button class="${state.board === id ? "active" : ""}" data-board="${id}" type="button">${escapeHtml(label)}</button>`;
}

function renderArticle(article) {
  return `
    <article class="article">
      <a href="${escapeAttr(article.url)}" target="_blank" rel="noreferrer">
        <span class="score">${article.score}</span>
        <strong>${escapeHtml(article.title)}</strong>
      </a>
      ${article.title_original && article.title_original !== article.title ? `<p class="original">原题：${escapeHtml(article.title_original)}</p>` : ""}
      <p>${escapeHtml(article.summary || "暂无摘要")}</p>
      <footer>${escapeHtml(article.source)} · ${escapeHtml(article.entity || article.topic || "")} · ${article.minutes} min · ${escapeHtml(article.date || "")}</footer>
    </article>
  `;
}

function renderSources() {
  const sources = state.sources.all_sources || [];
  const active = sources.filter((item) => item.enabled);
  const disabled = sources.filter((item) => !item.enabled);
  return `
    <section class="stats-line">
      <div><strong>${state.sources.today.active_sources}</strong><span>今日活跃</span></div>
      <div><strong>${state.sources.today.articles}</strong><span>今日文章</span></div>
      <div><strong>${state.sources.today.avg_score}</strong><span>均分</span></div>
    </section>
    <section class="source-grid">
      ${active.map(renderSourceCard).join("")}
      ${disabled.map(renderSourceCard).join("")}
    </section>
  `;
}

function renderSourceCard(source) {
  return `
    <article class="source-card ${source.enabled ? "" : "disabled"}">
      <header>
        <h3>${escapeHtml(source.name)}</h3>
        <span>${source.quality_index}</span>
      </header>
      <p>${escapeHtml(source.group)} · ${escapeHtml(source.language)} · 扫描 ${source.scanned_30d} · 入选 ${source.selected_30d}</p>
      <div class="tag-row">${source.style_tags.map((tag) => `<span>${escapeHtml(tag)}</span>`).join("")}</div>
    </article>
  `;
}

function renderApi() {
  const endpoints = [
    ["GET", "/lists/today.json", "今日导读、蒸馏漏斗、实体动向、热词"],
    ["GET", "/lists/watchlist.json", "实体卡片、30 天热度曲线、主题文章组"],
    ["GET", "/lists/boards.json", "学啥/读啥/做啥/忽略四个内容板"],
    ["GET", "/lists/article_details.json", "60 分以上文章详情、为什么重要、上手建议"],
    ["GET", "/lists/sources.json", "信源画像、质量指数、活跃度"],
    ["GET", "/digest-latest.md", "面向人读的 Markdown 简报"],
    ["GET", "/llms.txt", "给 Claude、Cursor、Codex 等 AI 工具读的精简版"],
    ["GET", "/llms-full.txt", "给 AI 工具读的完整版"],
  ];
  return `
    <section class="api-layout">
      <div class="intro">
        <h2>你在这里看到的一切，都是公开静态文件。</h2>
        <p>GitHub Actions 生成 JSON 和 Markdown，GitHub Pages 负责托管。没有服务端，也不需要 API key 才能读取。</p>
      </div>
      <div class="terminal">
        <p>curl -s ./lists/today.json</p>
        <p>curl -s ./llms.txt</p>
      </div>
    </section>
    <section class="panel">
      ${endpoints.map(([method, path, desc]) => `<div class="endpoint"><span>${method}</span><strong>${path}</strong><p>${desc}</p></div>`).join("")}
    </section>
  `;
}

function renderStory() {
  return `
    <section class="story">
      <h2>这个项目的结构</h2>
      <div class="flow">
        <div>RSS / RSSHub / 官方信源</div>
        <div>GitHub Actions 定时运行 pipeline</div>
        <div>实体匹配、打分、中文翻译、摘要生成</div>
        <div>输出 JSON / Markdown / llms.txt</div>
        <div>GitHub Pages 发布为静态网站</div>
      </div>
      <p>下一步如果要继续接近 Distilled，可以继续补：过刊早晚刊、周洞察、搜索、PWA 离线缓存、X/Twitter 自建 RSSHub。</p>
    </section>
  `;
}

function renderCompactArticle(article) {
  return `<article class="compact-article"><a href="${escapeAttr(article.url)}" target="_blank" rel="noreferrer">${escapeHtml(article.title)}</a><p><span>${article.score}</span> · ${escapeHtml(article.source)} · ${article.minutes} min</p></article>`;
}

function renderMove(move) {
  const arrow = move.direction === "up" ? "↑" : move.direction === "down" ? "↓" : "→";
  return `<div class="move"><strong>${escapeHtml(move.display)}</strong><span>本周 ${move.articles_7d} · 今日 +${move.today_count} ${arrow}</span></div>`;
}

function bindContentTabs() {
  document.querySelectorAll("[data-board]").forEach((button) => {
    button.addEventListener("click", () => {
      state.board = button.dataset.board;
      render();
    });
  });
}

function bindCopyButtons() {
  document.querySelectorAll("[data-copy]").forEach((button) => {
    button.addEventListener("click", async () => {
      await navigator.clipboard.writeText(button.dataset.copy || "");
      button.textContent = "已复制";
    });
  });
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeAttr(value) {
  return escapeHtml(value).replaceAll("\n", "&#10;");
}

loadData()
  .then(() => {
    render();
    window.addEventListener("hashchange", render);
  })
  .catch((error) => {
    document.getElementById("pageMeta").textContent = "加载失败";
    document.getElementById("view").innerHTML = `<section class="panel"><h2>无法加载情报数据</h2><p>${escapeHtml(error.message)}</p></section>`;
  });
