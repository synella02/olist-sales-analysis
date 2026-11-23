"""Step 1b: Run every query in queries.sql and print the results.

Run:  python run_queries.py
Results are also saved to the results/ folder as CSV files for your README and charts.
"""

import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = Path("olist.db")
SQL_PATH = Path("queries.sql")
OUT_DIR = Path("results")


def main():
    OUT_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    # Queries are separated by semicolons
    queries = [q.strip() for q in SQL_PATH.read_text(encoding="utf-8").split(";")]
    queries = [q for q in queries if "SELECT" in q.upper() or "WITH" in q.upper()]

    pd.set_option("display.width", 200)
    pd.set_option("display.max_columns", None)

    for i, query in enumerate(queries, start=1):
        df = pd.read_sql_query(query, conn)
        print(f"\n===== Q{i} =====")
        print(df.head(15).to_string(index=False))
        df.to_csv(OUT_DIR / f"q{i}.csv", index=False)

    conn.close()
    print("\nSaved all results in the results/ folder.")


if __name__ == "__main__":
    main()
