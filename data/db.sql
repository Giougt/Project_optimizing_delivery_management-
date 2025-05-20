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

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS users_data (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    country VARCHAR(100),
    age INTEGER
);

-- for test admin --
INSERT INTO users (username, password) VALUES ('admin', '1234');