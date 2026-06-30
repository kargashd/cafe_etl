import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from src.utils import get_logger

logger = get_logger(__name__)


def setup_plot_style() -> None:
    """Функция настраивает стиль графиков."""
    plt.style.use("seaborn-v0_8-darkgrid")
    sns.set_palette("husl")
    plt.rcParams["figure.figsize"] = (10, 6)
    plt.rcParams["font.size"] = 12
    plt.rcParams["axes.titlesize"] = 14
    plt.rcParams["axes.labelsize"] = 12


def ensure_output_dir(output_path: str) -> None:
    """Функция создаёт директорию для сохранения графиков."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)


def plot_revenue_by_month(df: pd.DataFrame, output_path: str = "output/plots/revenue_by_month.png") -> None:
    """Функция линейный график выручки по месяцам."""
    logger.info("Построение графика: выручка по месяцам")

    if df.empty:
        logger.error("DataFrame пуст")
        raise ValueError("DataFrame is empty")

    required = ["Month", "Total_Spent"]
    missing = set(required) - set(df.columns)
    if missing:
        logger.error(f"Отсутствуют колонки: {missing}")
        raise KeyError(f"Missing columns: {missing}")

    try:
        monthly = df.groupby("Month")["Total_Spent"].sum().reset_index()
        monthly.columns = ["Month", "Revenue"]

        setup_plot_style()
        ensure_output_dir(output_path)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(monthly["Month"], monthly["Revenue"], marker="o", linewidth=2, markersize=8)

        ax.set_title("Выручка по месяцам", fontsize=14, fontweight="bold")
        ax.set_xlabel("Месяц", fontsize=12)
        ax.set_ylabel("Выручка (₽)", fontsize=12)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        logger.info(f"График сохранён: {output_path}")
    except Exception as e:
        logger.error(f"Ошибка при построении графика выручки по месяцам: {e}")
        raise


def plot_top_items_by_revenue(df: pd.DataFrame, n: int = 5, output_path: str = "output/plots/top_items_revenue.png") -> None:
    """Функция горизонтальная столбчатая диаграмма топ-N товаров по выручке."""
    logger.info(f"Построение графика: топ-{n} товаров по выручке")

    if df.empty:
        logger.error("DataFrame пуст")
        raise ValueError("DataFrame is empty")

    required = ["Item", "Total_Spent"]
    missing = set(required) - set(df.columns)
    if missing:
        logger.error(f"Отсутствуют колонки: {missing}")
        raise KeyError(f"Missing columns: {missing}")

    try:
        top_items = df.groupby("Item")["Total_Spent"].sum().nlargest(n).sort_values()

        setup_plot_style()
        ensure_output_dir(output_path)

        fig, ax = plt.subplots(figsize=(10, 6))
        top_items.plot(kind="barh", ax=ax, color="skyblue", edgecolor="navy")

        ax.set_title(f"Топ-{n} товаров по выручке", fontsize=14, fontweight="bold")
        ax.set_xlabel("Выручка (₽)", fontsize=12)
        ax.set_ylabel("Товар", fontsize=12)
        ax.grid(True, alpha=0.3, axis="x")

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        logger.info(f"График сохранён: {output_path}")
    except Exception as e:
        logger.error(f"Ошибка при построении графика топ-{n} товаров: {e}")
        raise


def plot_payment_methods(df: pd.DataFrame, output_path: str = "output/plots/payment_methods.png") -> None:
    """Функция круговая диаграмма распределения выручки по способам оплаты."""
    logger.info("Построение графика: распределение выручки по способам оплаты")

    if df.empty:
        logger.error("DataFrame пуст")
        raise ValueError("DataFrame is empty")

    if "Payment_Method" not in df.columns or "Total_Spent" not in df.columns:
        logger.error("Отсутствуют колонки Payment_Method или Total_Spent")
        raise KeyError("Payment_Method or Total_Spent column not found")

    try:
        payment_revenue = df.groupby("Payment_Method")["Total_Spent"].sum()

        setup_plot_style()
        ensure_output_dir(output_path)

        fig, ax = plt.subplots(figsize=(8, 8))
        wedges, texts, autotexts = ax.pie(
            payment_revenue,
            labels=payment_revenue.index,
            autopct="%1.1f%%",
            startangle=90,
            explode=[0.02] * len(payment_revenue),
            textprops={"fontsize": 12}
        )

        ax.set_title("Распределение выручки по способам оплаты", fontsize=14, fontweight="bold")

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        logger.info(f"График сохранён: {output_path}")
    except Exception as e:
        logger.error(f"Ошибка при построении графика способов оплаты: {e}")
        raise


def plot_location_comparison(df: pd.DataFrame, output_path: str = "output/plots/location_revenue.png") -> None:
    """Функция столбчатая диаграмма сравнения выручки Takeaway vs In_Store."""
    logger.info("Построение графика: сравнение выручки Takeaway vs In_Store")

    if df.empty:
        logger.error("DataFrame пуст")
        raise ValueError("DataFrame is empty")

    required = ["Location", "Total_Spent"]
    missing = set(required) - set(df.columns)
    if missing:
        logger.error(f"Отсутствуют колонки: {missing}")
        raise KeyError(f"Missing columns: {missing}")

    try:
        location_revenue = df.groupby("Location")["Total_Spent"].sum()

        setup_plot_style()
        ensure_output_dir(output_path)

        colors = ["#2ecc71" if loc == "Takeaway" else "#3498db" for loc in location_revenue.index]
        fig, ax = plt.subplots(figsize=(8, 6))
        location_revenue.plot(kind="bar", ax=ax, color=colors, edgecolor="navy")

        ax.set_title("Сравнение выручки Takeaway vs In_Store", fontsize=14, fontweight="bold")
        ax.set_xlabel("Тип заказа", fontsize=12)
        ax.set_ylabel("Выручка (₽)", fontsize=12)
        ax.grid(True, alpha=0.3, axis="y")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        logger.info(f"График сохранён: {output_path}")
    except Exception as e:
        logger.error(f"Ошибка при построении графика сравнения по типам заказа: {e}")
        raise


def plot_heatmap(df: pd.DataFrame, output_path: str = "output/plots/heatmap.png") -> None:
    """Функция тепловая карта: выручка по дням недели и месяцам."""
    logger.info("Построение тепловой карты: выручка по дням недели и месяцам")

    if df.empty:
        logger.error("DataFrame пуст")
        raise ValueError("DataFrame is empty")

    required = ["Day_Name", "Month", "Total_Spent"]
    missing = set(required) - set(df.columns)
    if missing:
        logger.error(f"Отсутствуют колонки: {missing}")
        raise KeyError(f"Missing columns: {missing}")

    try:
        heatmap_data = df.groupby(["Day_Name", "Month"])["Total_Spent"].sum().unstack(fill_value=0)

        if heatmap_data.empty:
            logger.warning("Нет данных для тепловой карты")
            return

        setup_plot_style()
        ensure_output_dir(output_path)

        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(
            heatmap_data,
            annot=True,
            fmt=".0f",
            cmap="YlOrRd",
            linewidths=0.5,
            linecolor="white",
            ax=ax,
            cbar_kws={"label": "Выручка (₽)"}
        )

        ax.set_title("Выручка по дням недели и месяцам", fontsize=14, fontweight="bold")
        ax.set_xlabel("Месяц", fontsize=12)
        ax.set_ylabel("День недели", fontsize=12)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        logger.info(f"Тепловая карта сохранена: {output_path}")
    except Exception as e:
        logger.error(f"Ошибка при построении тепловой карты: {e}")
        raise


def run_visualization(df: pd.DataFrame, output_dir: str = "output/plots/") -> None:
    """Функция запускает все графики."""
    logger.info("=" * 60)
    logger.info("ЗАПУСК ВИЗУАЛИЗАЦИИ ДАННЫХ")
    logger.info("=" * 60)

    if df.empty:
        logger.error("DataFrame пуст")
        raise ValueError("DataFrame is empty")

    try:
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        plot_revenue_by_month(df)
        plot_top_items_by_revenue(df)
        plot_payment_methods(df)
        plot_location_comparison(df)
        plot_heatmap(df)

        logger.info(f"Все графики сохранены в {output_dir}")
    except Exception as e:
        logger.error(f"Ошибка при визуализации данных: {e}")
        raise

    logger.info("=" * 60)
    logger.info("ВИЗУАЛИЗАЦИЯ ЗАВЕРШЕНА")
    logger.info("=" * 60)