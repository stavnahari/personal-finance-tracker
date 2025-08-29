-- users
CREATE TABLE IF NOT EXISTS users (
  id            SERIAL PRIMARY KEY,
  name          VARCHAR(100),
  email         VARCHAR(150) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at    TIMESTAMP DEFAULT NOW()
);

-- categories (optional)
CREATE TABLE IF NOT EXISTS categories (
  id      SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id) ON DELETE CASCADE NOT NULL,
  name    VARCHAR(100) NOT NULL,
  UNIQUE(user_id, name)
);

-- transactions
CREATE TABLE IF NOT EXISTS transactions (
  id          SERIAL PRIMARY KEY,
  user_id     INT REFERENCES users(id) ON DELETE CASCADE NOT NULL,
  date        DATE NOT NULL,
  amount      DECIMAL(12,2) NOT NULL,
  merchant    VARCHAR(150),
  description TEXT,
  category    VARCHAR(100),
  created_at  TIMESTAMP DEFAULT NOW()
);

-- helpful indexes
CREATE INDEX IF NOT EXISTS idx_tx_user_date    ON transactions(user_id, date DESC);
CREATE INDEX IF NOT EXISTS idx_tx_user_category ON transactions(user_id, category);
CREATE INDEX IF NOT EXISTS idx_tx_user_amount   ON transactions(user_id, amount);
