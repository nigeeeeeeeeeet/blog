-- Схема
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
);

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    order_date DATE NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- 1. Додавання продуктів
INSERT INTO products (name, category, price) VALUES
    ('iPhone 15', 'смартфони', 999.99),
    ('Samsung Galaxy S24', 'смартфони', 899.99),
    ('Xiaomi Redmi Note 13', 'смартфони', 299.99),
    ('MacBook Air M3', 'ноутбуки', 1299.99),
    ('Dell XPS 13', 'ноутбуки', 1199.99),
    ('Lenovo ThinkPad X1', 'ноутбуки', 1399.99),
    ('iPad Air', 'планшети', 599.99),
    ('Samsung Galaxy Tab S9', 'планшети', 649.99),
    ('Lenovo Tab P11', 'планшети', 249.99);

-- 2. Додавання клієнтів
INSERT INTO customers (first_name, last_name, email) VALUES
    ('Іван', 'Петренко', 'ivan.petrenko@example.com'),
    ('Олена', 'Коваль', 'olena.koval@example.com'),
    ('Марія', 'Шевченко', 'maria.shevchenko@example.com'),
    ('Андрій', 'Бондаренко', 'andriy.bondarenko@example.com');

-- 3. Замовлення товарів
INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES
    (1, 1, 1, '2026-01-05'),
    (1, 4, 2, '2026-01-06'),
    (2, 2, 1, '2026-01-10'),
    (2, 7, 1, '2026-01-11'),
    (3, 3, 3, '2026-02-01'),
    (3, 5, 1, '2026-02-02'),
    (4, 9, 2, '2026-02-15'),
    (4, 1, 1, '2026-03-01'),
    (1, 8, 1, '2026-03-05'),
    (2, 6, 1, '2026-03-10');

-- 4. Сумарний обсяг продажів
SELECT SUM(p.price * o.quantity) AS total_sales
FROM orders o
JOIN products p ON o.product_id = p.product_id;

-- 5. Кількість замовлень на кожного клієнта
SELECT c.customer_id, c.first_name, c.last_name, COUNT(o.order_id) AS orders_count
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id;

-- 6. Середній чек замовлення
SELECT AVG(order_total) AS average_order_value
FROM (
    SELECT o.order_id, SUM(p.price * o.quantity) AS order_total
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY o.order_id
);

-- 7. Найбільш популярна категорія товарів
SELECT p.category, COUNT(o.order_id) AS orders_count
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY orders_count DESC
LIMIT 1;

-- 8. Загальна кількість товарів кожної категорії
SELECT category, COUNT(*) AS products_count
FROM products
GROUP BY category;

-- 9. Оновлення цін (смартфони +10%)
UPDATE products
SET price = price * 1.10
WHERE category = 'смартфони';
