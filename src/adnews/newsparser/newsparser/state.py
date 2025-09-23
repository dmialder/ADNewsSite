# Глобальное хранилище чекпойнтов в памяти процесса
_LAST_PUBLISHED: dict[str, str] = {}  # source_name -> ISO-строка

def get_last_published(source_name: str):
    return _LAST_PUBLISHED.get(source_name)

def set_last_published(source_name: str, last_pub_iso: str, _checked_iso: str) -> None:
    _LAST_PUBLISHED[source_name] = last_pub_iso
