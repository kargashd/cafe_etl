import pandas as pd
from pathlib import Path
from typing import Dict, Any, List

from src.utils import get_logger

logger = get_logger(__name__)

REQUIRED_COLUMNS = [
    "Transaction_Id",
    "Item",
    "Quantity",
    "Price_Per_Unit",
    "Total_Spent",
    "Payment_Method",
    "Location",
    "Transaction_Date",
]


def validate_columns(df: pd.DataFrame, required_columns: List[str]) -> None:
    """Функция проверяет совпадение колонок"""
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Отсутствуют колонки: {missing_columns}")
    logger.info("Все колонки на месте")


def load_data(file_path: str) -> pd.DataFrame:
    """Функция загрузки данных из файлы CSV"""
    path = Path(file_path)

    if not path.exists():
        logger.error(f"Файл не найден: {file_path}")
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    try:
        logger.info(f"Загрузка из {file_path}")
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError as e:
        logger.error(f"Файл пуст: {file_path}")
        raise ValueError(f"Файл пуст: {file_path}") from e
    except Exception as e:
        logger.error("Ошибка загрузки")
        raise

    if df.empty:
        logger.error(f"DataFrame пуст")
        raise ValueError("DataFrame пуст")

    validate_columns(df, REQUIRED_COLUMNS)

    logger.info(f"Загружено {len(df)} строк и {len(df.columns)} колонок")
    return df


def get_data_info(df: pd.DataFrame) -> Dict[str, Any]:
    """Функция создания списка с информацие о DataFrame"""

    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": df.dtypes.to_dict(),
        "null_counts": df.isnull().sum().to_dict(),
        "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024**2,
    }


def print_extract_report(df: pd.DataFrame) -> None:
    """Функция выводит отчёт: df.head(), df.info(), df.describe(), пропуски"""
    logger.info("=" * 60)
    logger.info("ОТЧЁТ EXTRACT")
    logger.info("=" * 60)

    logger.info(f"Количество строк: {df.shape[0]}\nКоличество колонок: {df.shape[1]}")
    logger.info(f"Память: {df.memory_usage(deep=True).sum() / 1024 ** 2:.2f} MB")

    logger.info("\nПервые 5 строк:")
    print(df.head())

    logger.info("\nИнформация о данных:")
    print(df.info())

    logger.info("\nСтатистика по числовым колонкам:")
    print(df.describe())

    logger.info("\nПропуски")
    print(df.isnull().sum())
