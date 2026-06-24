"""Модуль аналитики данных (Analyze)."""

import pandas as pd
from typing import Dict, Any

from src.utils import get_logger

logger = get_logger(__name__)


def top_items_by_revenue(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Топ N товаров по выручке."""
    logger.info(f"Топ-{n} товаров по выручке")

    if df.empty:
        logger.error("DataFrame пуст")
        raise ValueError("DataFrame is empty")

    required = ["Item", "Total_Spent"]
    missing = set(required) - set(df.columns)
    if missing:
        logger.error(f"Отсутствуют колонки: {missing}")
        raise KeyError(f"Missing columns: {missing}")

    try:
        result = df.groupby("Item")["Total_Spent"].sum().sort_values(ascending=False).head(n).reset_index()
        result.columns = ["Item", "Total_Revenue"]
    except Exception as e:
        logger.error(f"Ошибка при расчёте топ-{n} по выручке: {e}")
        raise

    logger.info(f"Найдено {len(result)} товаров")
    return result


def top_items_by_quantity(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Топ N товаров по количеству продаж."""
    logger.info(f"Топ-{n} товаров по количеству продаж")

    if df.empty:
        logger.error("DataFrame пуст")
        raise ValueError("DataFrame is empty")

    required = ["Item", "Quantity"]
    missing = set(required) - set(df.columns)
    if missing:
        logger.error(f"Отсутствуют колонки: {missing}")
        raise KeyError(f"Missing columns: {missing}")

    try:
        result = df.groupby("Item")["Quantity"].sum().sort_values(ascending=False).head(n).reset_index()
        result.columns = ["Item", "Total_Quantity"]
    except Exception as e:
        logger.error(f"Ошибка при расчёте топ-{n} по количеству: {e}")
        raise

    logger.info(f"Найдено {len(result)} товаров")
    return result


def popular_method_by_count(df: pd.DataFrame) -> pd.Series:
    """Самый популярный способ оплаты по количеству транзакций."""
    logger.info("Расчёт способов оплаты по количеству транзакций")

    if df.empty:
        logger.error("DataFrame пуст")
        raise ValueError("DataFrame is empty")

    if "Payment_Method" not in df.columns:
        logger.error("Колонка Payment_Method отсутствует")
        raise KeyError("Payment_Method column not found")

    try:
        result = df["Payment_Method"].value_counts()
    except Exception as e:
        logger.error(f"Ошибка при расчёте способов оплаты: {e}")
        raise

    logger.info(f"Найдено {len(result)} способов оплаты")
    return result


def popular_method_by_revenue(df: pd.DataFrame) -> pd.Series:
    """Самый популярный способ оплаты по сумме выручки."""
    logger.info("Расчёт способов оплаты по выручке")

    if df.empty:
        logger.error("DataFrame пуст")
        raise ValueError("DataFrame is empty")

    required = ["Payment_Method", "Total_Spent"]
    missing = set(required) - set(df.columns)
    if missing:
        logger.error(f"Отсутствуют колонки: {missing}")
        raise KeyError(f"Missing columns: {missing}")

    try:
        result = df.groupby("Payment_Method")["Total_Spent"].sum().sort_values(ascending=False)
    except Exception as e:
        logger.error(f"Ошибка при расчёте выручки по способам оплаты: {e}")
        raise

    return result


def revenue_by_location(df: pd.DataFrame) -> pd.Series:
    """Сравнение выручки Takeaway vs In_Store."""
    logger.info("Сравнение выручки по типам заказа")

    if df.empty:
        logger.error("DataFrame пуст")
        raise ValueError("DataFrame is empty")

    required = ["Location", "Total_Spent"]
    missing = set(required) - set(df.columns)
    if missing:
        logger.error(f"Отсутствуют колонки: {missing}")
        raise KeyError(f"Missing columns: {missing}")

    try:
        result = df.groupby("Location")["Total_Spent"].sum().sort_values(ascending=False)
    except Exception as e:
        logger.error(f"Ошибка при сравнении выручки по типам заказа: {e}")
        raise

    return result


def revenue_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """Выручка по месяцам (сортировка по убыванию)."""
    logger.info("Расчёт выручки по месяцам")

    if df.empty:
        logger.error("DataFrame пуст")
        raise ValueError("DataFrame is empty")

    required = ["Month", "Total_Spent"]
    missing = set(required) - set(df.columns)
    if missing:
        logger.error(f"Отсутствуют колонки: {missing}")
        raise KeyError(f"Missing columns: {missing}")

    try:
        result = df.groupby("Month")["Total_Spent"].sum().sort_values(ascending=False).reset_index()
        result.columns = ["Month", "Total_Revenue"]
    except Exception as e:
        logger.error(f"Ошибка при расчёте выручки по месяцам: {e}")
        raise

    return result


def avg_check_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """Средний чек по месяцам."""
    logger.info("Расчёт среднего чека по месяцам")

    if df.empty:
        logger.error("DataFrame пуст")
        raise ValueError("DataFrame is empty")

    required = ["Month", "Total_Spent"]
    missing = set(required) - set(df.columns)
    if missing:
        logger.error(f"Отсутствуют колонки: {missing}")
        raise KeyError(f"Missing columns: {missing}")

    try:
        result = df.groupby("Month")["Total_Spent"].mean().sort_values(ascending=False).reset_index()
        result.columns = ["Month", "Avg_Check"]
    except Exception as e:
        logger.error(f"Ошибка при расчёте среднего чека по месяцам: {e}")
        raise

    return result


def best_day_by_revenue(df: pd.DataFrame) -> pd.Series:
    """День недели с максимальной выручкой."""
    logger.info("Расчёт дня недели с максимальной выручкой")

    if df.empty:
        logger.error("DataFrame пуст")
        raise ValueError("DataFrame is empty")

    required = ["Day_Name", "Total_Spent"]
    missing = set(required) - set(df.columns)
    if missing:
        logger.error(f"Отсутствуют колонки: {missing}")
        raise KeyError(f"Missing columns: {missing}")

    try:
        result = df.groupby("Day_Name")["Total_Spent"].sum().sort_values(ascending=False)
    except Exception as e:
        logger.error(f"Ошибка при расчёте дня недели с максимальной выручкой: {e}")
        raise

    return result


def item_preference_by_location(df: pd.DataFrame) -> Dict[str, Any]:
    """Предпочтения по товарам в зависимости от типа заказа."""
    logger.info("Расчёт предпочтений по товарам")

    if df.empty:
        logger.error("DataFrame пуст")
        raise ValueError("DataFrame is empty")

    required = ["Item", "Location", "Quantity"]
    missing = set(required) - set(df.columns)
    if missing:
        logger.error(f"Отсутствуют колонки: {missing}")
        raise KeyError(f"Missing columns: {missing}")

    try:
        cross = pd.crosstab(df["Item"], df["Location"], values=df["Quantity"], aggfunc="sum")
        cross = cross.fillna(0)

        cross["Preference"] = cross.apply(
            lambda row: "Takeaway" if row.get("Takeaway", 0) > row.get("In_Store", 0)
            else ("In_Store" if row.get("In_Store", 0) > row.get("Takeaway", 0) else "Equal"),
            axis=1
        )

        top_takeaway = cross.nlargest(5, "Takeaway")[["Takeaway", "Preference"]]
        top_in_store = cross.nlargest(5, "In_Store")[["In_Store", "Preference"]]
    except Exception as e:
        logger.error(f"Ошибка при расчёте предпочтений по товарам: {e}")
        raise

    return {
        "cross_table": cross,
        "top_takeaway": top_takeaway,
        "top_in_store": top_in_store,
    }


def run_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """Запускает все аналитические функции."""
    logger.info("=" * 60)
    logger.info("ЗАПУСК АНАЛИТИКИ ДАННЫХ")
    logger.info("=" * 60)

    if df.empty:
        logger.error("DataFrame пуст")
        raise ValueError("DataFrame is empty")

    try:
        results = {
            "top_items_by_revenue": top_items_by_revenue(df),
            "top_items_by_quantity": top_items_by_quantity(df),
            "popular_method_by_count": popular_method_by_count(df),
            "popular_method_by_revenue": popular_method_by_revenue(df),
            "revenue_by_location": revenue_by_location(df),
            "revenue_by_month": revenue_by_month(df),
            "avg_check_by_month": avg_check_by_month(df),
            "best_day_by_revenue": best_day_by_revenue(df),
            "item_preference": item_preference_by_location(df),
        }
    except Exception as e:
        logger.error(f"Ошибка при выполнении аналитики: {e}")
        raise

    logger.info("Аналитика завершена")
    logger.info("=" * 60)
    return results


def print_analysis_results(results: Dict[str, Any]) -> None:
    """Выводит результаты анализа в читаемом формате."""
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ АНАЛИЗА")
    print("=" * 60)

    print("\n1. Топ-5 товаров по выручке:")
    print(results["top_items_by_revenue"].to_string(index=False))

    print("\n2. Топ-5 товаров по количеству продаж:")
    print(results["top_items_by_quantity"].to_string(index=False))

    print("\n3. Способы оплаты (по количеству транзакций):")
    print(results["popular_method_by_count"])

    print("\n4. Способы оплаты (по сумме выручки):")
    print(results["popular_method_by_revenue"])

    print("\n5. Сравнение выручки Takeaway vs In_Store:")
    print(results["revenue_by_location"])

    print("\n6. Выручка по месяцам (от большего к меньшему):")
    print(results["revenue_by_month"].to_string(index=False))

    print("\n7. Средний чек по месяцам:")
    print(results["avg_check_by_month"].to_string(index=False))

    print("\n8. День недели с максимальной выручкой:")
    print(results["best_day_by_revenue"])

    print("\n9. Предпочтения по товарам:")
    print("Топ-5 товаров, которые чаще берут с собой (Takeaway):")
    print(results["item_preference"]["top_takeaway"].to_string())
    print("\nТоп-5 товаров, которые чаще берут в зале (In_Store):")
    print(results["item_preference"]["top_in_store"].to_string())

    print("\n" + "=" * 60)
