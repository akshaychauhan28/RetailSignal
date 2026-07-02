import pandas as pd
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://postgres:password123@localhost:5432/retailsignal"
DATA_PATH = "data/raw"

engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    conn.execute(text("TRUNCATE TABLE fact_orders, fact_payments, fact_reviews, dim_customers, dim_products, dim_sellers, dim_date CASCADE"))
    conn.commit()

customers_df = pd.read_csv(f"{DATA_PATH}/olist_customers_dataset.csv")
orders_df = pd.read_csv(f"{DATA_PATH}/olist_orders_dataset.csv")
order_items_df = pd.read_csv(f"{DATA_PATH}/olist_order_items_dataset.csv")
order_payments_df = pd.read_csv(f"{DATA_PATH}/olist_order_payments_dataset.csv")
order_reviews_df = pd.read_csv(f"{DATA_PATH}/olist_order_reviews_dataset.csv")
products_df = pd.read_csv(f"{DATA_PATH}/olist_products_dataset.csv")
sellers_df = pd.read_csv(f"{DATA_PATH}/olist_sellers_dataset.csv")
category_translation_df = pd.read_csv(f"{DATA_PATH}/product_category_name_translation.csv")

products_df = pd.merge(products_df,category_translation_df, on='product_category_name',how='left')

products_df['product_category_name'] = products_df['product_category_name'].fillna('UNKNOWN')
products_df['product_category_name_english'] = products_df['product_category_name_english'].fillna('UNKNOWN')

customers_df = customers_df.drop_duplicates()
sellers_df = sellers_df.drop_duplicates()
order_reviews_df = order_reviews_df.drop_duplicates()
category_translation_df = category_translation_df.drop_duplicates()
products_df = products_df.drop_duplicates()

orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
orders_df['order_approved_at'] = pd.to_datetime(orders_df['order_approved_at'])
orders_df['order_delivered_carrier_date'] = pd.to_datetime(orders_df['order_delivered_carrier_date'])
orders_df['order_delivered_customer_date'] = pd.to_datetime(orders_df['order_delivered_customer_date'])
orders_df['order_estimated_delivery_date'] = pd.to_datetime(orders_df['order_estimated_delivery_date'])
order_reviews_df['review_creation_date'] = pd.to_datetime(order_reviews_df['review_creation_date'])
order_reviews_df['review_answer_timestamp'] = pd.to_datetime(order_reviews_df['review_answer_timestamp'])

all_dates = pd.concat([
    orders_df['order_purchase_timestamp'],
    orders_df['order_approved_at'],
    orders_df['order_delivered_carrier_date'],
    orders_df['order_delivered_customer_date'],
    orders_df['order_estimated_delivery_date'],
    order_reviews_df['review_creation_date'],
    order_reviews_df['review_answer_timestamp']
]).dt.date.unique()

dim_date_df = pd.DataFrame({'full_date':all_dates})
dim_date_df = dim_date_df.dropna()

dim_date_df['full_date'] = pd.to_datetime(dim_date_df['full_date'])

dim_date_df['day'] = dim_date_df['full_date'].dt.day
dim_date_df['month'] = dim_date_df['full_date'].dt.month
dim_date_df['year'] = dim_date_df['full_date'].dt.year
dim_date_df['quarter'] = dim_date_df['full_date'].dt.quarter
dim_date_df['month_name'] = dim_date_df['full_date'].dt.month_name()

dim_date = dim_date_df.to_sql('dim_date', engine, if_exists='append', index=False)
dim_customers = customers_df.to_sql('dim_customers', engine, if_exists='append', index=False)

products_df = products_df[['product_id', 'product_category_name_english', 'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']]
products_df.to_sql('dim_products', engine, if_exists='append', index=False)
sellers_df.to_sql('dim_sellers', engine, if_exists='append', index=False)

orders_df['purchase_date'] = orders_df['order_purchase_timestamp'].dt.date
dim_date_keys = pd.read_sql("SELECT date_key, full_date FROM dim_date", engine)