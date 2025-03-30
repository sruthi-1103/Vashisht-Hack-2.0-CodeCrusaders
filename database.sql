create database see;
use see;

CREATE TABLE sign_up (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    ph_no BIGINT,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE surplus_food (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    ph_no VARCHAR(15) NOT NULL,
    email VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    food_name VARCHAR(255) NOT NULL,
    food_quantity VARCHAR(255) NOT NULL,
    expiry DATETIME NOT NULL,
    status VARCHAR(20) DEFAULT 'NOT EXPIRED',
    description TEXT,
    food_image VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //
CREATE EVENT update_food_status
ON SCHEDULE EVERY 1 MINUTE
DO
    UPDATE surplus_food
    SET status = 'EXPIRED'
    WHERE expiry < NOW() - INTERVAL 1 MINUTE
    AND status = 'NOT EXPIRED';
// 
DELIMITER ;

select * from sign_up;
select * from surplus_food;

drop table sign_up;
drop table surplus_food;