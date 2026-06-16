import logging
import logging.config
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


def setup_logging(config_path: str = 'config/logging.conf') -> None:
    """Функция настривает логирование из файла или basicConfig"""
    config_file = Path(config_path)

    if config_file.exists():
        try:
            logging.config.fileConfig(config_path)
            logging.getLogger(__name__).info(f"Логирование настроено из {config_path}")
        except Exception as e:
            logging.basicConfig(level=logging.INFO)
            logging.getLogger(__name__).error(f"Ошибка загрузки {config_path}, использую basicConfig")

    else:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger(__name__).warning(f"Файл {config_path} не найден. Использую basicConfig")


def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """Загружает конфигурацию из Yaml-файла"""
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Файл конфигурации не найден {config_path}")

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        get_logger(__name__).info(f"Конфигурация загружена из {config_path}")
        return config
    except yaml.YAMLError as e:
        get_logger(__name__).error(f"Ошибка парсинга YAML: {e}")
        raise ValueError(f"Ошибка парасинга {config_path}: {e}") from e
    except Exception as e:
        get_logger(__name__).error(f"Ошибка чтения файла: {e}")
        raise


def get_logger(name: str) -> logging.Logger:
    """Возвращает логгер с указанным именем"""
    return logging.getLogger(name)
