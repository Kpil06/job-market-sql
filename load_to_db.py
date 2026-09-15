import sqlite3
import pandas as pd 

CSV_PATH = "data/jobs.csv"
DB_PATH = "jobs.db"


def create_table(conn):
    """Creates teh jobs table with a schema.
    id is stored as TEXT, not INTERGER, Jooble's job ID's are large enough that Python/SQLite can mishandle them as floats which loses precision, so treating them as a text avoids that entirely.
    """
    conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            location TEXT,
            salary TEXT,
            snippet TEXT,
            date_posted TEXT,
            category TEXT,
            url TEXT,
            fetched_at TEXT
        )
    """)
    conn.commit()

def load_csv_to_db(conn):
    """Read the csv and load it into the jobs table, replacing any existing data so re-running this script is always safe/repeatable."""
    df = pd.read_csv(CSV_PATH, dtype={"id": str}) # forceis to stay text
    df.to_sql("jobs", conn, if_exists="replace", index=False)
    return len(df)

def main():
    conn = sqlite3.connect(DB_PATH)
    create_table(conn)

    row_count = load_csv_to_db(conn)

    print(f"Loaded {row_count} rows into {DB_PATH}")

    # Quick check to confirm if the table looks right

    cursor = conn.execute("SELECT COUNT(*) FROM jobs")
    total = cursor.fetchone()[0]
    print(f"Total rows in jobs table: {total}")

    cursor = conn.execute("SELECT title, company, category FROM jobs LIMIT 3")
    print("\nSample rows:")
    for row in cursor.fetchall():
        print(row)

    conn.close

if __name__ == "__main__":
    main()