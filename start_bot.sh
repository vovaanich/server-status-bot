#!/bin/bash
# Скрипт запуска бота через виртуальное окружение
BASE_DIR=$(dirname "$0")
source "$BASE_DIR/.venv/bin/activate"
python "$BASE_DIR/server_status_bot.py"
