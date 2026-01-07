create table if not exists dim_users (
  user_id text primary key,
  first_seen_at timestamp,
  last_seen_at timestamp,
  total_events bigint
);

create table if not exists dim_products (
  product_id text primary key,
  add_to_cart_events bigint,
  purchase_events bigint
);

create table if not exists fct_purchases_daily (
  purchase_day timestamp primary key,
  purchases bigint,
  revenue_gbp double precision,
  purchasing_users bigint
);
