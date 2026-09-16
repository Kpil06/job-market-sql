import sqlite3 

DB_PATH = "jobs.db"


def run_query(conn, title, sql):
    """Run a SQL query and print te results under a header."""
    print(f"\n{'=' * 30}")
    print(title)
    print('=' * 30)
    cursor = conn.execute(sql)
    columns = [description[0] for description in cursor.description]
    print(columns)
    for row in cursor.fetchall():
        print(row)


def main():
    conn = sqlite3.connect(DB_PATH)

    run_query(
        conn,
        "Job count by category",
        """
        SELECT category, COUNT(*) as job_count
        FROM jobs 
        GROUP BY category 
        ORDER BY job_count DESC
        """
    )
    
    run_query(
        conn,
        "Top hiring companies",
        """
        SELECT company, COUNT(*) as job_count
        FROM jobs 
        GROUP BY company
        ORDER BY job_count DESC
        LIMIT 5
        """
    )

    run_query(
        conn,
        "Percentage of listings missing salary info",
        """
        SELECT
            ROUND(100.0 * SUM(CASE WHEN salary IS NULL OR salary = '' THEN 1 ELSE 0 END) / COUNT(*), 1)
            AS pct_missing_salary
        FROM jobs
        """
    )

    run_query(
        conn,
        "Companies hiring across multiple categories",
        """
        SELECT company, COUNT(DISTINCT category) as category_count
        FROM jobs
        GROUP BY company
        HAVING category_count > 1
        ORDER BY category_count DESC
        """
    )

    run_query(
        conn,
        "Jobs categorized as 'other (not cleanly matched)",
        """
        SELECT title, company
        FROM jobs
        WHERE category = 'other'
        """
    )

    conn.close()

if __name__ == "__main__":
    main()