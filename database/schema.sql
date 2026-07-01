CREATE DATABASE IF NOT EXISTS foodease_db;
USE foodease_db;

-- 1. Roles Table
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Users Table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    role_id INT NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE RESTRICT,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Restaurants Table
CREATE TABLE restaurants (
    restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
    owner_id INT NOT NULL,
    restaurant_name VARCHAR(150) NOT NULL,
    description TEXT,
    cuisine VARCHAR(100),
    phone VARCHAR(20),
    
    address TEXT,
    city VARCHAR(100),
    opening_time TIME,
    closing_time TIME,
    logo VARCHAR(255),
    cover_image VARCHAR(255),
    rating DECIMAL(2,1) DEFAULT 0.0,
    status ENUM('Pending','Approved','Rejected') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (owner_id) REFERENCES users(user_id)
);

-- 4. Categories Table
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Food Items Table
CREATE TABLE food_items (
    food_id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT NOT NULL,
    category_id INT NOT NULL,

    food_name VARCHAR(150) NOT NULL,
    description TEXT,

    price DECIMAL(10,2) NOT NULL,

    image VARCHAR(255),

    availability BOOLEAN DEFAULT TRUE,

    discount DECIMAL(5,2) DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (restaurant_id)
        REFERENCES restaurants(restaurant_id)
        ON DELETE CASCADE,

    FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
);

-- 6. Orders Table
CREATE TABLE orders (

    order_id INT AUTO_INCREMENT PRIMARY KEY,

    customer_id INT NOT NULL,

    restaurant_id INT NOT NULL,

    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,

    total_amount DECIMAL(10,2) NOT NULL,

    order_status ENUM(
        'Pending',
        'Accepted',
        'Preparing',
        'Picked',
        'Out for Delivery',
        'Delivered',
        'Cancelled'
    ) DEFAULT 'Pending',

    payment_status ENUM(
        'Pending',
        'Paid'
    ) DEFAULT 'Pending',

    delivery_address TEXT,

    FOREIGN KEY (customer_id)
        REFERENCES users(user_id),

    FOREIGN KEY (restaurant_id)
        REFERENCES restaurants(restaurant_id)
);
-- 7. Order Items Table
CREATE TABLE order_items (

    order_item_id INT AUTO_INCREMENT PRIMARY KEY,

    order_id INT NOT NULL,

    food_id INT NOT NULL,

  quantity INT NOT NULL DEFAULT 1,

   unit_price DECIMAL(10,2) NOT NULL,

    subtotal DECIMAL(10,2) NOT NULL,

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
        ON DELETE CASCADE,

    FOREIGN KEY (food_id)
        REFERENCES food_items(food_id)
);

-- 8. Reviews Table
CREATE TABLE reviews (

    review_id INT AUTO_INCREMENT PRIMARY KEY,

    customer_id INT,

    restaurant_id INT,

    food_id INT,

    rating TINYINT CHECK (rating BETWEEN 1 AND 5),

    comment TEXT,

    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id)
        REFERENCES users(user_id),

    FOREIGN KEY (restaurant_id)
        REFERENCES restaurants(restaurant_id),

    FOREIGN KEY (food_id)
        REFERENCES food_items(food_id)
);
-- Seed Basic Data
INSERT INTO roles (id, name) VALUES (1, 'Admin'), (2, 'Customer'), (3, 'Restaurant Owner'), (4, 'Delivery Staff');

CREATE TABLE addresses(
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    postal_code VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  
    FOREIGN KEY (customer_id)
REFERENCES users(user_id)
ON DELETE CASCADE
    
);

CREATE TABLE cart (
    cart_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);
CREATE TABLE cart_items (
    cart_item_id INT AUTO_INCREMENT PRIMARY KEY,

    cart_id INT NOT NULL,

    food_id INT NOT NULL,

    quantity INT DEFAULT 1,

    unit_price DECIMAL(10,2),

    FOREIGN KEY (cart_id)
        REFERENCES cart(cart_id)
        ON DELETE CASCADE,

    FOREIGN KEY (food_id)
        REFERENCES food_items(food_id)
);

CREATE TABLE payments (

    payment_id INT AUTO_INCREMENT PRIMARY KEY,

    order_id INT NOT NULL,

    payment_method ENUM(
        'Cash',
        'Card'
    ),

    payment_status ENUM(
        'Pending',
        'Paid',
        'Failed'
    ),

    transaction_id VARCHAR(150),

    payment_date DATETIME,

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);


CREATE TABLE delivery_assignments (

    assignment_id INT AUTO_INCREMENT PRIMARY KEY,

    order_id INT,

    delivery_staff_id INT,

    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    delivery_status ENUM(
        'Assigned',
        'Picked',
        'On The Way',
        'Delivered'
    ) DEFAULT 'Assigned',

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY (delivery_staff_id)
        REFERENCES users(user_id)
);