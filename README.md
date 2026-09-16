# Job Market SQL Pipeline 

Loads job listings data collected in job-market-tracker into a SQLite database and runs SQL queries to answer questions about the Irish data job market. Second project in a portfolio series building towards a full data pipeline.

## What it does 

- Reads job listings data from a CSV (from the job-market-tracker scrapper)
- Loads it into a SQLite database with an explicit schema (load_to_db.py)
- Runs a set of SQL queries a:nswering real questions about the dataset (queries.py):
    - Job count by category 
    - Top hiring companies 
    - Percentage of listings missing salary info
    - Most recently posted jobs 
    - companies hiring across multiple categories 
    - Jobs that didn't cleanly match a category ("other")

## Tech stack 

Python, pandas, sqlite3 (standard library)

## Setup

1. Clone this repo and create a virtual environment:
    python3 -m venv venv 
    source venv/bin/activate
    pip install -r requirements.txt 

2. Build the database from the included CSV:
    python load_to_db.py

3. Run the queries:
    python queries.py 
    
## Schema 

CREATE TABLE jobs (
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

id is stored as TEXT rather than INTERGER - the source API's job ID's  are large enough that treating them as numbers risks losing precision (e.g. via float conversion), so they are kept as text throughout.

## Findings 

- 100% of listings in this dataset are missing salary information - confirms a known data liitation flagged in the job-market-tracker project.
- A handful of listings didn't cleanly match a category based on title keywords (labelled as "other").

## Design decisions 

- jobs.db is not commited to the repo - it's generated from the csv by load_to_db.py, so anyone cloning the repo can rebuild it in one command. Commiting to the source data & build script is cleaner than commiting a binary databse file.
- Re-running load_to_db.py is safe - it replaces the table each time rather than appending, so the database always reflects the current CSV exactly.

## Possible next steps

- Feed this database into an interactive dashboard (see next project in this series)
- Expand querie as the dataset grows (more rows from jo-market-tracker)
- Improve category keyword matching to reduce "other" classifications