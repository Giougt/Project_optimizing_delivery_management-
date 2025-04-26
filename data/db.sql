CREATE DATABASE IF NOT EXISTS optimizing_delivery;

USE optimizing_delivery;

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255),
    delivery_address VARCHAR(255),
    start_address VARCHAR(255),
    weight FLOAT,
    product VARCHAR(255),
    delivery_date INT,
    payment_method VARCHAR(255),
    price FLOAT
);
