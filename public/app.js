async function loadWatchlist() {
  const response = await fetch("./watchlist.json", { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Failed to load watchlist: ${response.status}`);
  }
  return response.json();
}

function renderEntityList(data, selectedId) {
  const list = document.getElementById("entityList");
  list.innerHTML = "";

  data.entities.forEach((entity) => {
    const button = document.createElement("button");
    button.className = `entity-button${entity.entity_id === selectedId ? " active" : ""}`;
    button.type = "button";
    button.innerHTML = `${entity.display}<span>${entity.domain || "general"} · ${entity.article_count || 0} articles</span>`;
    button.addEventListener("click", () => renderEntity(data, entity.entity_id));
    list.appendChild(button);
  });
}

function renderEntity(data, entityId) {
  const entity = data.entities.find((item) => item.entity_id === entityId) || data.entities[0];
  renderEntityList(data, entity.entity_id);

  document.getElementById("entityTitle").textContent = entity.display;
  document.getElementById("summary").textContent = entity.narrative?.summary || "No summary yet.";

  const sections = document.getElementById("sections");
  sections.innerHTML = "";

  (entity.narrative?.sections || []).forEach((section) => {
    const sectionEl = document.createElement("section");
    sectionEl.className = "section";

    const articles = (section.articles || [])
      .map((article) => {
        const title = escapeHtml(article.title || "Untitled");
        const url = article.url || article.link || "#";
        const score = article.score ?? "-";
        const source = escapeHtml(article.source || "Unknown");
        const language = escapeHtml(article.language || "unknown");
        const date = escapeHtml(article.date || "");
        const actionability = article.actionability ?? "-";
        return `
          <article class="article">
            <a href="${url}" target="_blank" rel="noreferrer">${title}</a>
            <div class="article-meta">${source} · ${language} · ${date} · score ${score} · actionability ${actionability}</div>
          </article>
        `;
      })
      .join("");

    sectionEl.innerHTML = `
      <h3>${escapeHtml(section.topic || "Other")}</h3>
      <div class="article-list">${articles}</div>
    `;
    sections.appendChild(sectionEl);
  });
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

loadWatchlist()
  .then((data) => {
    const generated = data.generated_at ? new Date(data.generated_at).toLocaleString() : "not generated";
    document.getElementById("meta").textContent =
      `${data.meta?.article_total || 0} articles · ${data.meta?.entity_curated || 0} entities · ${generated}`;

    if (!data.entities?.length) {
      document.getElementById("entityTitle").textContent = "No entities";
      document.getElementById("summary").textContent = "Run the pipeline to generate briefing data.";
      return;
    }

    renderEntity(data, data.entities[0].entity_id);
  })
  .catch((error) => {
    document.getElementById("meta").textContent = "Load failed";
    document.getElementById("entityTitle").textContent = "Unable to load data";
    document.getElementById("summary").textContent = error.message;
  });
