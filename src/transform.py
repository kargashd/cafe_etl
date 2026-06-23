import pandas as pd
from typing import Dict, Any

from src.utils import get_logger

logger = get_logger(__name__)


def clean_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Преобразует Transaction_Date в datetime. Удаляет некорректные. Добавляет Month, Month_Name, Day_Of_Week, Day_Name"""
    logger.info("Преобразование дат...")

    if "Transaction_Date" not in df.columns:
        logger.error("Колонка Transaction_Date отсутствует")
        raise KeyError("Transaction_Date column not found")


    try:
        df['Transaction_Date'] = df['Transaction_Date'].astype(str).str.strip()
        df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'], dayfirst=True, errors='coerce')
    except Exception as e:
        logger.error(f"Ошибка при преобразовании дат: {e}")

        raise

    invalid_count = df['Transaction_Date'].isna().sum()

    if invalid_count > 0:
        logger.warning(f"Найдено {invalid_count} некорректных дат. Удаляем...")
        try:
            df = df.dropna(subset=['Transaction_Date'])
        except Exception as e:
            logger.error(f"Ошибка при удалении некорректных дат: {e}")
            raise
            logger.info(f"Осталось {len(df)} строк")

    try:
        df['Month'] = df['Transaction_Date'].dt.month
        df['Month_Name'] = df['Transaction_Date'].dt.strftime('%B')
        df['Day_Of_Week'] = df['Transaction_Date'].dt.dayofweek
        df['Day_Name'] = df['Transaction_Date'].dt.strftime('%a')
    except Exception as e:
        logger.error(f"Ошибка при создании колонок с датой: {e}")

        raise

    logger.info(f"Диапазон дат: {df['Transaction_Date'].min()} - {df['Transaction_Date'].max()}")
    return df


def fix_total_spent(df: pd.DataFrame) -> pd.DataFrame:
    """Функция исправляет Total_Spent = Quantity * Price_Per_Unit"""
    logger.info("Проверка целостности Total_Spent")

    required = ['Quantity', 'Price_Per_Unit', 'Total_Spent']
    missing = set(required) - set(df.columns)

    if missing:
        logger.error(f"Отсутствуют колонки {missing}")
        raise KeyError(f"Missing columns: {missing}")

    try:
        calculated = df['Quantity'] * df['Price_Per_Unit']
        mismatches = (df['Total_Spent'] != calculated).sum()
    except Exception as e:
        logger.error(f"Ошибка при расчёте Total_Spent: {e}")

        raise

    if mismatches > 0:
        logger.warning(f"Найдено {mismatches} несоответствий. Исправляем...")
        try:
            df['Total_Spent'] = calculated
        except Exception as e:
            logger.error(f"Ошибка при исправлении Total_Spent: {e}")

            raise
    else:
        logger.info(f"Все суммы корректны")

    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Функция удаляет дубликаты, если такие есть"""
    logger.info("Проверка дубликатов...")

    if 'Transaction_Id' not in df:
        logger.error("Transaction_Id нет в df")
        raise KeyError("Transaction_Id column not found")

    try:
        before = len(df)
        df = df.drop_duplicates(subset=['Transaction_Id'], keep='first')
        removed = before - len(df)
    except Exception as e:
        logger.error(f"Ошибка при удалении дубликатов: {e}")
        raise

    if removed > 0:
        logger.info(f"Удалено {removed} дубликатов")
    else:
        logger.info(f"Дубликатов не найдено")

    return df


def handle_negative_values(df: pd.DataFrame) -> pd.DataFrame:
    """Функция удаляет строки с отрицательными значениями в Quantity, Price_Per_Unit, Total_Spent"""
    logger.info("Проверка отрицательных значений")

    numeric_cols = ['Quantity', 'Price_Per_Unit', 'Total_Spent']
    missing = set(numeric_cols) - set(df.columns)

    if missing:
        logger.error(f"Потеряны колонки {missing}")
        raise KeyError(f"Missing columns: {missing}")

    try:
        before = len(df)
        mask = (df['Quantity'] < 0) | (df['Price_Per_Unit'] < 0) | (df['Total_Spent'] < 0)
        negative_count = mask.sum()
    except Exception as e:
        logger.error(f"Ошибка при проверке отрицательных значений: {e}")
        raise

    if negative_count > 0:
        logger.warning(f"Найдено {negative_count} строк с отрицательными значениями. Удаляем...")
        try:
            df = df[~mask]
        except Exception as e:
            logger.error(f"Ошибка при удалении отрицательных значений: {e}")
            raise
        logger.info(f"Удалено {before - len(df)} строк")
    else:
        logger.info("Отрицательных значений не найдено")

    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Удаляет строки с пропусками в критических колонках"""
    critical_cols = ['Transaction_Id', "Item", "Quantity", "Price_Per_Unit", "Total_Spent"]

    logger.info("Проверка пропусков...")

    try:
        before = len(df)
        df = df.dropna(subset=critical_cols)
        removed = before - len(df)
    except Exception as e:
        logger.error(f"Ошибка при удалении пропусков: {e}")
        raise

    if removed > 0:
        logger.warning(f"Удалено {removed} строк с пропусками")
    else:
        logger.info("Пропусков не найдено")

    return df


def add_price_category(df: pd.DataFrame) -> pd.DataFrame:
    """Функция добавляет категории цен (Low/Medium/High)"""

    logger.info("Добавление категорий цен...")

    if "Price_Per_Unit" not in df.columns:
        logger.error("Price_Per_Unit отсутствует в df")
        raise KeyError("Price_Per_Unit column not found")

    def categorize(price: float) -> str:
        if price < 5:
            return "Low"
        elif price < 8:
            return "Medium"
        return "High"

    try:
        df["Price_Category"] = df["Price_Per_Unit"].apply(categorize)

    except Exception as e:
        logger.error(f"Ошибка при добавлении категорий цен: {e}")
        raise

    try:
        counts = df["Price_Category"].value_counts()
        logger.info(f"Категории: Low={counts.get('Low', 0)}, Medium={counts.get('Medium', 0)}, High={counts.get('High', 0)}")
    except Exception as e:
        logger.error(f"Ошибка при подсчёте категорий: {e}")
        raise

    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Функция запускает все шаги очистки по порядку"""
    logger.info("=" * 60)
    logger.info("ЗАПУСК ТРАНСФОРМАЦИИ ДАННЫХ")
    logger.info("=" * 60)

    if df.empty:
        logger.error("DataFrame пуст")
        raise ValueError("DataFrame is empty")

    try:
        df = clean_dates(df)
        df = fix_total_spent(df)
        df = remove_duplicates(df)
        df = handle_negative_values(df)
        df = handle_missing_values(df)
        df = add_price_category(df)
    except Exception as e:
        logger.error(f"Ошибка в процессе трансформации: {e}")
        raise

    logger.info(f"Итоговое количество строк: {len(df)}")
    logger.info("=" * 60)

    return df
