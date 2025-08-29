-- Month spend totals
CREATE OR REPLACE VIEW v_monthly_totals AS
SELECT
  user_id,
  DATE_TRUNC('month', date)::date AS month,
  SUM(amount) AS total_spend
FROM transactions
GROUP BY user_id, DATE_TRUNC('month', date);

-- Spend by category (last 90 days)
CREATE OR REPLACE VIEW v_spend_by_category_90d AS
SELECT
  user_id,
  category,
  SUM(amount) AS total_spend
FROM transactions
WHERE date >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY user_id, category;
