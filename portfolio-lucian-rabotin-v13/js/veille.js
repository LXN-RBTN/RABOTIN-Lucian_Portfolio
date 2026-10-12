/* =========================================================
   veille.js : recherche, filtres et affichage des articles.
   Les images sont chargées progressivement pour éviter un
   gros pic de chargement lorsque la page de veille s'ouvre.
   ========================================================= */
document.addEventListener('DOMContentLoaded', () => {
  const grid = document.querySelector('#articleGrid');
  if (!grid) return;

  const search = document.querySelector('#search');
  const category = document.querySelector('#category');
  const year = document.querySelector('#year');
  const count = document.querySelector('#articleCount');
  const dataNode = document.querySelector('#veilleData');
  if (!search || !category || !year || !count || !dataNode) return;

  let articles = [];
  try {
    articles = (JSON.parse(dataNode.textContent).articles || []).slice().sort((a, b) => String(b.date || '').localeCompare(String(a.date || '')) || String(a.title || '').localeCompare(String(b.title || ''), 'fr'));
  } catch (error) {
    grid.innerHTML = '<div class="empty">Impossible de charger les articles.</div>';
    console.error(error);
    return;
  }

  const esc = (value) => String(value ?? '')
    .replaceAll('&', '&amp;').replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;').replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');

  [...new Set(articles.map(a => a.category).filter(Boolean))]
    .sort((a, b) => a.localeCompare(b, 'fr'))
    .forEach(value => category.insertAdjacentHTML(
      'beforeend', `<option value="${esc(value)}">${esc(value)}</option>`
    ));

  [...new Set(articles.map(a => a.date?.slice(0, 4)).filter(Boolean))]
    .sort().reverse()
    .forEach(value => year.insertAdjacentHTML(
      'beforeend', `<option value="${esc(value)}">${esc(value)}</option>`
    ));

  const formatDate = (value) => {
    const date = new Date(`${value}T12:00:00`);
    return Number.isNaN(date.getTime()) ? value : new Intl.DateTimeFormat('fr-FR').format(date);
  };

  function render() {
    const query = search.value.trim().toLowerCase();
    const selectedCategory = category.value;
    const selectedYear = year.value;

    const filtered = articles.filter(article => {
      const text = [article.title, article.summary, article.source, article.category]
        .join(' ').toLowerCase();
      return (!query || text.includes(query))
        && (!selectedCategory || article.category === selectedCategory)
        && (!selectedYear || article.date?.startsWith(selectedYear));
    });

    count.textContent = `${filtered.length} article${filtered.length > 1 ? 's' : ''}`;

    if (!filtered.length) {
      grid.innerHTML = '<div class="empty">Aucun article ne correspond à ta recherche.</div>';
      return;
    }

    grid.innerHTML = filtered.map(article => `
      <article class="article-card reveal visible">
        <a class="article-image" href="${esc(article.url)}" target="_blank" rel="noopener noreferrer" aria-label="Lire ${esc(article.title)}">
          <img src="${esc(article.image)}" alt="" loading="lazy" decoding="async" width="1200" height="800">
        </a>
        <div class="meta">
          <span>${esc(formatDate(article.date))}</span>
          <span>${esc(article.category)}</span>
        </div>
        <h3>${esc(article.title)}</h3>
        <p>${esc(article.summary)}</p>
        <div class="meta article-source">
          <span>${esc(article.source)}</span>
          <a class="read" href="${esc(article.url)}" target="_blank" rel="noopener noreferrer">Lire ↗</a>
        </div>
      </article>
    `).join('');
  }

  [search, category, year].forEach(element => {
    element.addEventListener('input', render);
    element.addEventListener('change', render);
  });

  render();
});
