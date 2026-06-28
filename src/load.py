import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from src.utils import get_logger

logger = get_logger(__name__)

load_dotenv()


def get_db_connection():
    """Функция создаёт подключение к PostgreSQL"""
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "cafe_db")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "")

    if not password:
        logger.warning("Пароль не задан в переменной DB_PASSWORD")

    db_url = f"postgresql://{user}:{password}@{host}:{port}/{name}" #postgresql://postgres:1234@host:5432/cafedb

    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Подключение к PostgreSQL успешно")
        return engine
    except Exception as e:
        logger.error(f"Ошибка подключения к PostgreSQL: {e}")
        raise


def create_table(engine, table_name: str = "sales") -> None:
    """Функция создаёт таблицу sales, если её нет"""
    logger.info(f"Создаёт таблицу {table_name}...")

    create_query = text(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        transaction_id VARCHAR(50) PRIMARY KEY,
        item VARCHAR(100),
        quantity INTEGER,
        price_per_unit DECIMAL(10,2),
        total_spent DECIMAL(10,2),
        payment_method VARCHAR(50),
        location VARCHAR(50),
        transaction_date DATE,
        month INTEGER,
        month_name VARCHAR(20),
        day_of_week INTEGER,
        day_name VARCHAR(10),
        price_category VARCHAR(10)
        );
    """)

    try:
        with engine.connect() as conn:
            conn.execute(create_query)
            conn.commit()
        logger.info(f"Таблица {table_name} уже создана или уже существует...")
    except Exception as e:
        logger.error(f"Ошибка при создании таблицы {table_name}: {e}")
        raise


def load_data_to_postgres(df: pd.DataFrame, table_name: str = 'sales') -> None:
    """Функция загружает DataFrame в PostgreSQL"""
    logger.info(f"Загружаем DataFrame в {table_name}")
    logger.info(f"Количество строк: {len(df)}")

    if df.empty:
        logger.error("DataFrame пуст")
        raise ValueError("DataFrame is empty")

    engine = get_db_connection()
    try:
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",
            index=False,
            method="multi"
        )
        logger.info(f"Данные успешно загружены, в sales {len(df)} строк")
    except Exception as e:
        logger.error(f"Ошибка при загрузке данных в PostgreSQL: {e}")
        raise


def run_sql_query(query: str) -> pd.DataFrame:
    """Функция запускает запросы из queris.sql"""
    logger.info(f"Выполнение SQL-запросов...")
    try:
        engine = get_db_connection()
        df = pd.read_sql(query, engine)
        logger.info(f"Запрос выполнены. Получено {len(df)} строк")

        return df
    except Exception as e:
        logger.error(f"Ошибка при выполнении SQL-запроса: {e}")
        raise


def compare_results(df_pandas: pd.DataFrame, df_sql: pd.DataFrame, name: str) -> None:
    """Функция сравнивает результат pandas и SQL"""
    logger.info(f"Сравнивает результаты для {name}")

    try:
        if df_pandas.equals(df_sql):
            logger.info(f"{name}: результаты совпадают")
        else:
            logger.warning(f"{name}: результаты не совпадают")

            diff = df_pandas.compare(df_sql)
            logger.warning(f"Различия:\n{diff}")
    except Exception as e:
        logger.error(f"Ошибка при сравнении результатов {name}: {e}")
        raise


def run_load_pipeline(df_clean: pd.DataFrame) -> None:
    """Функция запускает полный pipeline загрузки в PostgreSQL и валидацию"""
    logger.info("=" * 60)
    logger.info("ЗАПУСК ЗАГРУЗКИ В POSTGRESQL")
    logger.info("=" * 60)

    if df_clean.empty:
        logger.error("DataFrame пуст")
        raise ValueError("DataFrame is empty")

    try:
        load_data_to_postgres(df_clean)

        engine = get_db_connection()

        pandas_result = df_clean.groupby("Item")['Total_Spent'].sum().nlargest(5).reset_index()
        pandas_result.columns = ['Item', 'Total_Revenue']

        sql_query = """
            SELECT item, SUM(total_spent) AS total_revenue
            FROM sales
            GROUP BY item
            ORDER BY total_revenue DESC
            LIMIT 5
            """
        sql_result = pd.read_sql(sql_query, engine)

        compare_results(pandas_result, sql_result, "Топ-5 товаров по выручке")

        pandas_result = df_clean.groupby('Month')['Total_Spent'].sum().reset_index()
        pandas_result.columns = ['Month', 'Total_Revenue']

        sql_query = """
                SELECT month, SUM(total_spent) AS total_revenue
                FROM sales
                GROUP BY month
                ORDER BY month
            """
        sql_result = pd.read_sql(sql_query, engine)

        compare_results(pandas_result, sql_result, "Выручка по месяцам")

        logger.info("Валидация завершена")
    except Exception as e:
        logger.error(f"Ошибка в pipeline загрузки: {e}")
        raise

    logger.info("=" * 60)
    logger.info("ЗАГРУЗКА В POSTGRESQL ЗАВЕРШЕНА")
    logger.info("=" * 60)
