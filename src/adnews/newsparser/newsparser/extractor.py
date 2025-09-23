from bs4 import BeautifulSoup
from readability import Document          # эвристическое извлечение основного текста
from .http_fetcher import fetch_html      # загрузка HTML по URL


def extract_fulltext(e: dict, src: dict) -> str:
    print(e["link"])
    """Возвращает кортеж (извлечённый текст, сырой HTML или None)."""
    html = fetch_html(e["link"], src)  # HTTP GET статьи
    if not html:
        return "", None
    text = _try_selectors(html, src)
    if not text:
        text = _readability_text(html)
    return text


def _try_selectors(html: str, src: dict):
    """Пытается извлечь текст по CSS-селекторам из конфига."""
    selectors = src.get("selectors") or []
    if not selectors:
        return None

    soup = BeautifulSoup(html, "lxml")
    parts: list[str] = []

    for sel in selectors:                       # идём по приоритету
        nodes = soup.select(sel)
        if not nodes:
            continue
        for el in nodes:
            parts.append(el.get_text(separator="\n", strip=True))
        text = "\n".join(parts)
        if text:
            return text                         # первый успешный селектор — стоп

    return None


def _readability_text(html: str) -> str:
    """Fallback: извлекает основное содержимое через readability и чистит HTML."""
    doc = Document(html)                                                          # строим модель документа
    summary = doc.summary(html_partial=True)                                      # HTML основного блока
    return _html_to_text(summary)                                                 # чистим до текста

def _html_to_text(html: str) -> str:
    """Удаляет шум и возвращает плейнтекст."""
    soup = BeautifulSoup(html, "lxml")                                            # парсим HTML
    for bad in soup(["script", "style", "nav", "aside", "footer", "header"]):     # шумовые элементы
        bad.decompose()                                                           # удаляем из дерева
    return soup.get_text(separator="\n", strip=True)                              # плоский текст с переносами
