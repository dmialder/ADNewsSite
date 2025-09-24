let selectedManually = false;
let manuallySelectedIndex = null;

function render(newsList, selectedNews) {
  const sidebar = document.getElementById("sidebar");
  sidebar.innerHTML = "";

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
        });
    };

    sidebar.appendChild(div);
  });

  // Показываем только если не было ручного выбора
  if (!selectedManually && selectedNews) {
    showNews(selectedNews);
  }
}

function showNews(news) {
  const content = document.getElementById("content");
  content.innerHTML = `
    <h2>
      <a href="${news.source_url}" target="_blank" style="color: #9cf; text-decoration: none;">
        ${news.title} <span style="font-size: 0.8em; color: #ccc;">(${news.datetime})</span>
      </a>
    </h2>
    <p>${news.summary}</p>
    <p style="margin-top: 1em;"><b>Совет:</b> ${news.advice}</p>
  `;
}

function updateNews() {
  fetch("/news")
    .then(res => res.json())
    .then(data => {
      // Передаём последний выбранный индекс, если пользователь уже кликал
      const selected = selectedManually ? data.news[manuallySelectedIndex] : data.selected;
      render(data.news, selected);
    });
}

setInterval(updateNews, 8000);
updateNews();
