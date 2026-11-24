
import sqlite3
from pathlib import Path

import pandas as pd

DATA_DIR = Path("data")
DB_PATH = Path("olist.db")


FILES = {
    "olist_customers_dataset.csv": "customers",
    "olist_orders_dataset.csv": "orders",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "product_category_name_translation.csv": "category_translation",
}


INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_orders_id ON orders(order_id)",
    "CREATE INDEX IF NOT EXISTS idx_orders_cust ON orders(customer_id)",
    "CREATE INDEX IF NOT EXISTS idx_items_order ON order_items(order_id)",
    "CREATE INDEX IF NOT EXISTS idx_items_product ON order_items(product_id)",
    "CREATE INDEX IF NOT EXISTS idx_items_seller ON order_items(seller_id)",
    "CREATE INDEX IF NOT EXISTS idx_pay_order ON order_payments(order_id)",
    "CREATE INDEX IF NOT EXISTS idx_rev_order ON order_reviews(order_id)",
    "CREATE INDEX IF NOT EXISTS idx_prod_id ON products(product_id)",
    "CREATE INDEX IF NOT EXISTS idx_cust_id ON customers(customer_id)",
]


def main():
    missing = [f for f in FILES if not (DATA_DIR / f).exists()]
    if missing:
        print("These files are missing from the data/ folder:")
        for name in missing:
            print("  -", name)
        return

    conn = sqlite3.connect(DB_PATH)

    for file_name, table in FILES.items():
        df = pd.read_csv(DATA_DIR / file_name)
        df.to_sql(table, conn, if_exists="replace", index=False)
        print(f"Loaded {table}: {len(df):,} rows, {len(df.columns)} columns")

    for statement in INDEXES:
        conn.execute(statement)
    conn.commit()
    conn.close()
    print("\nDone. Database saved as", DB_PATH)


if __name__ == "__main__":
    main()
