import sqlite3

DB_NAME = "results.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            home_team TEXT,
            away_team TEXT,
            score TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_result(home, away, score):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO results(home_team, away_team, score) VALUES (?, ?, ?)",
        (home, away, score)
    )

    conn.commit()
    conn.close()


def get_results():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT home_team, away_team, score
        FROM results
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows