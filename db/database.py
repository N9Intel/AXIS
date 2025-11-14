from pathlib import Path
import sqlite3
from typing import List, Tuple


DB_PATH = Path("axis.db") #should change to .env file


def get_connection() -> sqlite3.Connection:
     conn = sqlite3.connect(DB_PATH)
     
     conn.execute("PRAGMA foreign_keys = ON;")
     return conn


def create_tables() -> None:
    """Create brokers and listings tables if they don't exist."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Brokers table: one row per broker
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS brokers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,         -- normalized broker name
                raw_name TEXT,              -- original broker name as seen
                notes TEXT,                 -- optional analyst notes
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # Listings table: one row per access listing, linked to a broker
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                broker_id INTEGER NOT NULL,
                access_type TEXT,
                country TEXT,
                privilege TEXT,
                price TEXT,
                description TEXT,
                source TEXT,
                post_date TEXT,
                sector TEXT,
                revenue TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (broker_id) REFERENCES brokers(id) ON DELETE CASCADE
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
          return cursor.fetchall()


def find_by_tier(tier: str) -> list[tuple]:
     with get_connection() as conn:
          cursor = conn.cursor()
          cursor.execute(
            """
            SELECT
                id, broker, listings, tier, sector, revenue, created_at
            FROM listings
            WHERE LOWER(tier) = LOWER(?)
            ORDER BY created_at DESC
            """,
            (tier,),
        )
          return cursor.fetchall()
     

def find_by_sector(sector: str) -> list[tuple]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                id, broker, listings, tier, sector, revenue, created_at
            FROM listings
            WHERE sector = ?
            ORDER BY created_at DESC
            """,
            (sector,),
        )
        return cursor.fetchall()

def search_query(q: str) -> list[tuple]:
     q = f"%{q.lower()}%"

     with get_connection() as conn:
          cursor = conn.cursor()
          cursor.execute(
            """
            SELECT id, broker, listings, tier, sector, revenue, created_at
            FROM listings
            WHERE LOWER(broker) LIKE ?
               OR LOWER(sector) LIKE ?
               OR LOWER(revenue) LIKE ?
               OR LOWER(tier) LIKE ?
            ORDER BY created_at DESC
            """,
            (q, q, q, q),
        )
          
          return cursor.fetchall()
