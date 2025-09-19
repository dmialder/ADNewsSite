import yaml                # импортируем парсер YAML и модуль регулярных выражений

REQUIRED_SRC_KEYS = ("name", "feed_url")  # кортеж ключей, которые обязаны быть в каждом источнике

def load_config(path: str) -> dict:       # объявление функции; тип: на вход путь (str), на выход словарь (dict)
    with open(path, "r", encoding="utf-8") as f:   # открываем YAML-файл для чтения в UTF-8
        raw = yaml.safe_load(f) or {}              # читаем YAML в dict; если пусто — подставляем {}

    defaults = raw.get("defaults", {}) or {}       # берем секцию defaults или пустой dict
    out = {                                        # формируем выходной конфиг верхнего уровня
        "period_sec": int(defaults.get("period_sec", 300)),              # период опроса с дефолтом 300
        "out_path": defaults.get("out_path"),   # путь для TXT-вывода      
        "throttle_sec": int(defaults.get("throttle_sec", 3)),            # пауза между запросами
        "headers": defaults.get("headers"),     # HTTP-заголовок
        "sources": []                                                    # список источников (пока пуст)
    }

    for s in raw.get("sources", []) or []:          # итерируемся по списку источников; если его нет — пустой список
        for k in REQUIRED_SRC_KEYS:                 # проверяем обязательные поля для каждого источника
            if k not in s or not s[k]:             # если ключ отсутствует или пустой
                raise ValueError(f"source missing {k}")  # бросаем понятную ошибку

        merged = {**defaults, **s}                  # плоское слияние dict: значения из s перекрывают defaults

        src = {                                     # нормализуем один источник в унифицированный dict
            "name": merged["name"],                 # имя источника (обязательно)
            "feed_url": merged["feed_url"],         # URL RSS-ленты (обязательно)
            "fulltext": merged.get("fulltext"),            # режим извлечения полного текста
            "force_all_if_no_category": bool(merged.get("force_all_if_no_category", True)),  # брать все, если нет категорий
            "category_include": merged.get("category_include"),             # компилируем include-regex
            "selectors": merged.get("selectors", []) or [],                                 # CSS-селекторы тела статьи
            "http_timeout": int(defaults.get("http_timeout_sec", 15))           # таймаут HTTP в секундах
        }
        out["sources"].append(src)                   # добавляем нормализованный источник в общий список

    if not out["sources"]:                           # если после парсинга источников нет
        raise ValueError("no sources in config")     # бросаем ошибку конфигурации
    return out                                       # возвращаем итоговый конфиг как dict
