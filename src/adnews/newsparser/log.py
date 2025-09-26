# src/adnews/newsparser/log.py
import logging
import json
from datetime import datetime
import os

def setup_logging():
    """Настройка логирования с проверками"""
    
    # Получаем абсолютный путь к файлу логов
    log_path = os.path.abspath('/var/www/u3198937/data/www/neuro-express.ru/src/adnews/newsparser/parser_simple.log')
    print(f"Файл логов будет создан: {log_path}")
    
    # Очищаем существующие обработчики
    logging.root.handlers.clear()
    
    # Настраиваем логирование
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format='%(message)s',
        encoding='utf-8',
        force=True  # Принудительно перенастроить
    )
    
    # Тестовое сообщение для проверки
    logging.info("=== ЛОГИРОВАНИЕ НАСТРОЕНО ===")
    print(f"Логирование настроено. Проверьте файл: {log_path}")

def log_article_parsing(source, url, status_code, message="Article processed"):
    """Функция для логирования информации о статье"""
    
    # Проверяем, настроено ли логирование
    if not logging.root.handlers:
        setup_logging()
    
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'news_source': source,
        'article_url': url,
        'response_status_code': status_code,
        'message': message
    }
    
    logger = logging.getLogger('news_parser')
    logger.info(json.dumps(log_data, ensure_ascii=False))
    
    # Дополнительная проверка
    print(f"LOG: {source} - {status_code} - {message}")

# Настройка при импорте модуля
setup_logging()
