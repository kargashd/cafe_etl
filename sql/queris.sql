-- Топ-5 товаров по выручке
SELECT item, SUM(total_spent) AS total_revenue
FROM sales
GROUP BY item
ORDER BY total_revenue DESC
LIMIT 5;

-- Топ-5 товаров по количеству продаж
SELECT item, SUM(quantity) AS total_quantity
FROM sales
GROUP BY item
ORDER BY total_quantity DESC
LIMIT 5;

-- Выручка по месяцам
SELECT month, month_name, SUM(total_spent) AS total_revenue
FROM sales
GROUP BY month, month_name
ORDER BY total_revenue DESC

-- Средний чек по месяцам
SELECT month, month_name, AVG(total_spent) as avg_check
FROM sales
GROUP BY month, month_name
ORDER BY avg_check DESC;

-- Сравнение выручки Takeaway vs In_store
SELECT location, SUM(total_spent) AS total_revenue
FROM sales
GROUP BY location
ORDER BY total_revenue DESC;

-- Топ дней недели по выручке
SELECT day_name, SUM(total_spent) as total_revenue
FROM sales
GROUP BY day_name
ORDER BY total_revenue DESC;
