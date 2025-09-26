#!/usr/bin/env python3

import sys
from pathlib import Path

# Получаем абсолютный путь к корню проекта
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent

# Добавляем корень проекта и src в Python path
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from src.adnews.newsparser.app import main

main()
