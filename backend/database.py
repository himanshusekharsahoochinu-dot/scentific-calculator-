import sqlite3
from pathlib import Path


# ==========================================
# DATABASE LOCATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

DATABASE = BASE_DIR / "calculator.db"


# ==========================================
# CREATE DATABASE
# ==========================================

def create_database():

    connection = sqlite3.connect(
        DATABASE
    )

    cursor = connection.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            expression TEXT NOT NULL,

            result TEXT NOT NULL,

            mode TEXT NOT NULL,

            created_at
            TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)


    connection.commit()

    connection.close()


# ==========================================
# ADD HISTORY
# ==========================================

def add_history(
    expression,
    result,
    mode
):

    connection = sqlite3.connect(
        DATABASE
    )

    cursor = connection.cursor()


    cursor.execute(
        """
        INSERT INTO history
        (
            expression,
            result,
            mode
        )
        VALUES (?, ?, ?)
        """,
        (
            expression,
            str(result),
            mode
        )
    )


    connection.commit()

    connection.close()


# ==========================================
# GET HISTORY
# ==========================================

def get_history():

    connection = sqlite3.connect(
        DATABASE
    )

    connection.row_factory = (
        sqlite3.Row
    )


    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT
            id,
            expression,
            result,
            mode,
            created_at
        FROM history
        ORDER BY id DESC
        LIMIT 50
        """
    )


    rows = cursor.fetchall()


    connection.close()


    return [
        dict(row)
        for row in rows
    ]


# ==========================================
# CLEAR HISTORY
# ==========================================

def clear_history():

    connection = sqlite3.connect(
        DATABASE
    )

    cursor = connection.cursor()


    cursor.execute(
        "DELETE FROM history"
    )


    connection.commit()

    connection.close()