INSERT INTO users (name, email, password_hash)
VALUES ('Demo', 'demo@example.com', '$2b$12$abcdefghijklmnopqrstuvwxN5hYI5i'); -- dummy hash

INSERT INTO categories (user_id, name)
VALUES (1, 'Food & Drinks'), (1, 'Transport'), (1, 'Rent'), (1, 'Entertainment');

INSERT INTO transactions (user_id, date, amount, merchant, description, category)
VALUES
(1, '2025-08-01', 7.50,  'Starbucks', 'Latte and muffin', 'Food & Drinks'),
(1, '2025-08-02', 50.00, 'Uber',      'Ride downtown',    'Transport'),
(1, '2025-08-03', 120.00,'Netflix',   'Monthly payment',  'Entertainment');
