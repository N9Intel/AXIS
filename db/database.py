from pathlib import Path
import sqlite3
from typing import List, Tuple


DB_PATH = Path("axis.db") #should change to .env file


def get_connection() -> sqlite3.Connection:
     return sqlite3.connect(DB_PATH)


def create_tables() -> None:
     with get_connection() as conn:
          cursor = conn.cursor()
          cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                broker TEXT NOT NULL,
                listings INTEGER NOT NULL,
                tier TEXT NOT NULL,
                sector TEXT NOT NULL,
                revenue TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
          conn.commit()


def insert_listing(broker: str,listings: str,tier: str,sector: str,revenue: str,) -> None:
     with get_connection() as conn:
          cursor = conn.cursor()
          cursor.execute(
            """
            INSERT INTO listings (broker, listings, tier, sector, revenue)
            VALUES (?, ?, ?, ?, ?)
            """,
            (broker, listings, tier, sector, revenue),
        )
          conn.commit()


def get_all_listings() -> list[tuple]:
     with get_connection() as conn:
          cursor = conn.cursor()
          cursor.execute(
            """
            SELECT
                id, broker, listings, tier, sector, revenue, created_at
            FROM listings
            ORDER BY created_at DESC
            """
        )
          return cursor.fetchall()


def find_by_broker(broker: str) -> list[tuple]:
     with get_connection() as conn:
          cursor = conn.cursor()
          cursor.execute(
            """
            SELECT
                id, broker, listings, tier, sector, revenue, created_at
            FROM listings
            WHERE broker = ?
            ORDER BY created_at DESC
            """,
            (broker,),
        )