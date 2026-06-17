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

    df['Transaction_Date'] = df['Transaction_Date'].astype(str).str.strip()
    df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'], dayfirst=True, errors='coerce')

    invalid_count = df['Transaction_Date'].isna().sum()

    if invalid_count > 0:
        logger.warning(f"Найдено {invalid_count} некорректных дат. Удаляем...")
        df = df.dropna(subset=['Transaction_Date'])
        logger.info(f"Осталось {len(df)} строк")

    df['Month'] = df['Transaction_Date'].dt.month
    df['Month_Name'] = df['Transaction_Date'].dt.strftime('%B')
    df['Day_Of_Week'] = df['Transaction_Date'].dt.dayofweek
    df['Day_Name'] = df['Transaction_Date'].dt.strftime('%a')

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

    calculated = df['Quantity'] * df['Price_Per_Unit']
    mismatches = (df['Total_Spent'] != calculated).sum()

    if mismatches > 0:
        logger.warning(f"Найдено {mismatches} несоответствий. Исправляем...")
        df['Total_Spent'] = calculated
    else:
        logger.info(f"Все суммы корректны")

    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Функция удаляет дубликаты, если такие есть"""
    logger.info("Проверка дубликатов...")

    if 'Transaction_Id' not in df:
        logger.error("Transaction_Id нет в df")
        raise KeyError("Transaction_Id column not found")

    before = len(df)
    df = df.drop_duplicates(subset=['Transaction_Id'], keep='first')
    removed = before - len(df)

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

    before = len(df)
    mask = (df['Quantity'] < 0) | (df['Price_Per_Unit'] < 0) | (df['Total_Spent'] < 0)
    negative_count = mask.sum()

    if negative_count > 0:
        logger.warning(f"Найдено {negative_count} строк с отрицательными значениями. Удаляем...")
        df = df[~mask]
        logger.info(f"Удалено {before - len(df)} строк")
    else:
        logger.info("Отрицательных значений не найдено")

    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Удаляет строки с пропусками в критических колонках"""
    critical_cols = ['Transaction_Id', "Item", "Quantity", "Price_Per_Unit", "Total_Spent"]

    logger.info("Проверка пропусков...")

    before = len(df)
    df = df.dropna(subset=critical_cols)
    removed = before - len(df)

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

    df["Price_Category"] = df["Price_Per_Unit"].apply(categorize)

    counts = df["Price_Category"].value_counts()
    logger.info(f"Категории: Low={counts.get('Low', 0)}, Medium={counts.get('Medium', 0)}, High={counts.get('High', 0)}")

    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Функция запускает все шаги очистки по порядку"""
    logger.info("=" * 60)
    logger.info("ЗАПУСК ТРАНСФОРМАЦИИ ДАННЫХ")
    logger.info("=" * 60)

    if df.empty:
        logger.error("DataFrame пуст")
        raise ValueError("DataFrame is empty")

    df = clean_dates(df)
    df = fix_total_spent(df)
    df = remove_duplicates(df)
    df = handle_negative_values(df)
    df = handle_missing_values(df)
    df = add_price_category(df)

    logger.info(f"Итоговое количество строк: {len(df)}")
    logger.info("=" * 60)

    return df
