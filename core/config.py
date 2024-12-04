import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TEMP_DIR = BASE_DIR / "temp"

# Проверяем, существует ли папка temp
TEMP_DIR.mkdir(exist_ok=True)
