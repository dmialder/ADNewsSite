import time
from datetime import datetime, timezone

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def run_forever(cfg: dict, process_source) -> None:  # главная функция цикла
    """
    cfg: dict из load_config()
    storage: объект хранилища (Storage)
    process_source: callable(storage, src_dict, cycle_iso) -> dict/None
    """
    period = int(cfg["period_sec"])           # период опроса в секундах
    sources = cfg["sources"]                  # список источников
    throttle_sec = int(cfg["throttle_sec"])

    while True:                               # бесконечный цикл
        cycle_t0 = time.monotonic()           # старт цикла по монотонным часам
        cycle_iso = utc_now_iso()             # метка времени цикла в ISO

        for src in sources:                   # перебор источников
            try:                              # ловим ошибки на источник
                stats = process_source(src, cycle_iso)  # запускаем обработку одного источника
            except KeyboardInterrupt:         # корректный выход по Ctrl+C
                raise
            #except Exception as e:            # прочие ошибки не роняют цикл
                #print(f"{cycle_iso} source={src['name']} error={e!r}")

            time.sleep(throttle_sec)  # пауза между источниками

        elapsed = time.monotonic() - cycle_t0 # длительность цикла
        sleep_s = period - elapsed            # сколько спать до выравнивания периода
        if sleep_s > 0:                       # если цикл короче периода
            time.sleep(sleep_s)               # спим оставшееся время
        # если elapsed >= period, идем сразу в следующий цикл


def run_once(cfg: dict, process_source) -> None:  # однократный проход
    """Один проход по всем источникам. Удобно для теста/отладки."""
    cycle_iso = utc_now_iso()              # общая метка времени для прохода
    for src in cfg["sources"]:             # перебор источников
        try:
            stats = process_source(src, cycle_iso)   # обработка источника
            print(f"{cycle_iso} source={src['name']} stats={stats}")  # лог
        except Exception as e:
            print(f"{cycle_iso} source={src['name']} error={e!r}")    # лог ошибки
        time.sleep(max(0, int(cfg["throttle_sec"])))  # пауза между источниками