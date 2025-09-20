#!/usr/bin/env python3

import sys
from pathlib import Path

script_dir = Path(__file__).parent
project_root = script_dir.parent

# Добавляем корень проекта в Python path
sys.path.insert(0, str(project_root))


# Импортируем и запускаем парсер
from src.adnews.web.app import main
main()

