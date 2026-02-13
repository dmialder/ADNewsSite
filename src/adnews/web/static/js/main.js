let selectedManually = false;
let manuallySelectedIndex = null;
let autoIndex = 0;
const mobileQuery = window.matchMedia("(max-width: 768px)");
let heroDragInit = false;
let isDraggingHero = false;

function formatDateTime(value) {
  if (!value) return "";
  const dt = new Date(value);
  if (Number.isNaN(dt.getTime())) return value;
  return new Intl.DateTimeFormat("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    timeZone: "Europe/Moscow",
    timeZoneName: "short",
  }).format(dt);
}

function render(newsList, selectedNews) {
  const sidebar = document.getElementById("sidebar");
  sidebar.innerHTML = '<div class="sidebar-title">Главные новости</div><div id="news-list" class="news-list"></div>';
  const listContainer = sidebar.querySelector("#news-list");

  newsList.forEach((item, i) => {
    const div = document.createElement("div");
    div.className = "news-item";
    div.textContent = item.title;

    // Подсвечиваем либо вручную выбранную, либо текущую от сервера
    if ((selectedManually && manuallySelectedIndex === i) ||
        (!selectedManually && selectedNews && item.title === selectedNews.title)) {
      div.classList.add("active");
    }

    div.onclick = () => {
      selectedManually = true;
      manuallySelectedIndex = i;

      fetch(`/select/${i}`)
        .then(res => res.json())
        .then(data => {
          showNews(data);
          render(newsList, data); // Обновляем подсветку
          if (mobileQuery.matches) {
            requestAnimationFrame(() => {
              const hero = document.querySelector(".hero-grid");
              const contentCard = document.getElementById("content");
              if (hero && contentCard) {
                const maxOffset = hero.scrollWidth; // с запасом, чтобы доехать до конца
                hero.scrollTo({ left: maxOffset, behavior: "smooth" });
                setTimeout(() => hero.scrollTo({ left: maxOffset, behavior: "smooth" }), 120);
              } else {
                document.getElementById("content")?.scrollIntoView({
                  behavior: "smooth",
                  block: "nearest",
                  inline: "center",
                });
              }
            });
          }
        });
    };

    listContainer.appendChild(div);
  });

  // Показываем только если не было ручного выбора
  if (!selectedManually && selectedNews) {
    showNews(selectedNews);
  }
}

function showNews(news) {
  const content = document.getElementById("content");
  const formattedDate = formatDateTime(news.datetime);
  const backBtn = mobileQuery.matches
    ? `<button id="back-to-list" class="back-arrow" aria-label="Назад к списку">&lt;</button>`
    : "";
  content.innerHTML = `
    ${backBtn}
    <h2>
      <a href="${news.source_url}" target="_blank" style="color: #000; text-decoration: none;">
        ${news.title}
        <span style="display: block; width: 92%; height: 1px; background: #000; margin: 0.4em auto;"></span>
        <span style="display: block; font-size: 0.8em; color: #000;">${formattedDate}</span>
      </a>
    </h2>
    <p>${news.summary}</p>
    <p style="margin-top: 1em;"><b>Совет:</b> ${news.advice}</p>
  `;

  if (mobileQuery.matches) {
    const btn = document.getElementById("back-to-list");
    if (btn) {
      btn.onclick = () => {
        const hero = document.querySelector(".hero-grid");
        if (hero) {
          hero.scrollTo({ left: 0, behavior: "smooth" });
        } else {
          document.getElementById("sidebar")?.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
        }
      };
    }
  }
}

function updateNews() {
  fetch("/news")
    .then(res => res.json())
    .then(data => {
      if (!data.news || !data.news.length) {
        render([], null);
        return;
      }

      if (selectedManually) {
        if (manuallySelectedIndex >= data.news.length) {
          manuallySelectedIndex = 0;
        }
        render(data.news, data.news[manuallySelectedIndex]);
        return;
      }

      if (mobileQuery.matches) {
        const idx = manuallySelectedIndex ?? 0;
        render(data.news, data.news[idx]);
      } else {
        if (autoIndex >= data.news.length) {
          autoIndex = 0;
        }
        const selected = data.news[autoIndex];
        autoIndex = (autoIndex + 1) % data.news.length;
        render(data.news, selected);
      }
    });
}

setInterval(updateNews, mobileQuery.matches ? 30000 : 20000);
updateNews();

function initHeroDrag() {
  // Отключили кастомный drag — используем нативный скролл
}

window.addEventListener("DOMContentLoaded", initHeroDrag);
mobileQuery.addEventListener?.("change", () => {
  if (mobileQuery.matches) initHeroDrag();
});
