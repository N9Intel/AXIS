from pathlib import Path
import sqlite3
from typing import List, Tuple, Optional


DB_PATH = Path("axis.db") #should change to .env file


def get_connection() -> sqlite3.Connection:
     conn = sqlite3.connect(DB_PATH)
     
     conn.execute("PRAGMA foreign_keys = ON;")
     return conn


def create_tables() -> None:
    with get_connection() as conn:
        cursor = conn.cursor()

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


def insert_broker(name: str, raw_name: str, notes: str) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO brokers (name, raw_name, notes)
            VALUES (?, ?, ?)
            """,
            (name, raw_name, notes),
        )
        conn.commit()
        return cursor.lastrowid
    

def get_all_brokers() -> List[Tuple]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, name, raw_name, notes, created_at
            FROM brokers
            ORDER BY created_at DESC
            """
        )
        return cursor.fetchall()


def find_broker_by_name(name: str) -> Optional[Tuple]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, name, raw_name, notes, created_at
            FROM brokers
            WHERE name = ?
            """,
            (name,),
        )
        return cursor.fetchone()


def get_broker_by_id(broker_id: int) -> Optional[Tuple]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, name, raw_name, notes, created_at
            FROM brokers
            WHERE id = ?
            """,
            (broker_id,),
        )
        return cursor.fetchone()
    

def insert_listing(
    broker_id: int,
    access_type: str,
    country: str,
    privilege: str,
    price: str,
    description: str,
    source: str,
    post_date: str,
    sector: str,
    revenue: str,
) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO listings (
                broker_id,
                access_type,
                country,
                privilege,
                price,
                description,
                source,
                post_date,
                sector,
                revenue
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                broker_id,
                access_type,
                country,
                privilege,
                price,
                description,
                source,
                post_date,
                sector,
                revenue,
            ),
        )
        conn.commit()
        return cursor.lastrowid


def get_all_listings() -> List[Tuple]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                l.id,
                b.name AS broker_name,
                l.access_type,
                l.country,
                l.privilege,
                l.price,
                l.description,
                l.source,
                l.post_date,
                l.sector,
                l.revenue,
                l.created_at
            FROM listings l
            JOIN brokers b ON l.broker_id = b.id
            ORDER BY l.created_at DESC
            """
        )
        return cursor.fetchall()


def find_listings_by_broker_name(broker_name: str) -> List[Tuple]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                l.id,
                b.name AS broker_name,
                l.access_type,
                l.country,
                l.privilege,
                l.price,
                l.description,
                l.source,
                l.post_date,
                l.sector,
                l.revenue,
                l.created_at
            FROM listings l
            JOIN brokers b ON l.broker_id = b.id
            WHERE b.name = ?
            ORDER BY l.created_at DESC
            """,
            (broker_name,),
        )
        return cursor.fetchall()
     

def find_listings_by_sector(sector: str) -> List[Tuple]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                l.id,
                b.name AS broker_name,
                l.access_type,
                l.country,
                l.privilege,
                l.price,
                l.description,
                l.source,
                l.post_date,
                l.sector,
                l.revenue,
                l.created_at
            FROM listings l
            JOIN brokers b ON l.broker_id = b.id
            WHERE l.sector = ?
            ORDER BY l.created_at DESC
            """,
            (sector,),
        )
        return cursor.fetchall()

def search_query(q: str) -> List[Tuple]:
    """
    Freeform search across broker name, access type, country, privilege,
    price, description, source, sector, revenue, and post_date.

    Returns rows in the same format as get_all_listings().
    """
    pattern = f"%{q.lower()}%"

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                l.id,
                b.name AS broker_name,
                l.access_type,
                l.country,
                l.privilege,
                l.price,
                l.description,
                l.source,
                l.post_date,
                l.sector,
                l.revenue,
                l.created_at
            FROM listings l
            JOIN brokers b ON l.broker_id = b.id
            WHERE
                LOWER(b.name)      LIKE ?
             OR LOWER(l.access_type) LIKE ?
             OR LOWER(l.country)     LIKE ?
             OR LOWER(l.privilege)   LIKE ?
             OR LOWER(l.price)       LIKE ?
             OR LOWER(l.description) LIKE ?
             OR LOWER(l.source)      LIKE ?
             OR LOWER(l.sector)      LIKE ?
             OR LOWER(l.revenue)     LIKE ?
             OR LOWER(l.post_date)   LIKE ?
            ORDER BY l.created_at DESC
            """,
            (pattern,) * 10,
        )
        return cursor.fetchall()


def find_duplicate_listings(
    broker_id: int,
    access_type: str,
    country: str,
    price: str,
    description: str,
    source: str,
    post_date: str,
    sector: str,
    revenue: str,
) -> List[Tuple]:
    """
    Look for listings that look like strong duplicates of a new one.

    Criteria (strict match):
      - same broker_id
      - same access_type
      - same country
      - same price
      - same source
      - same post_date
      - same sector
      - same revenue
      - same description

    Returns rows in the same format as get_all_listings()
    so print_listings() can be reused.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                l.id,
                b.name AS broker_name,
                l.access_type,
                l.country,
                l.privilege,
                l.price,
                l.description,
                l.source,
                l.post_date,
                l.sector,
                l.revenue,
                l.created_at
            FROM listings l
            JOIN brokers b ON l.broker_id = b.id
            WHERE
                l.broker_id   = ?
            AND l.access_type = ?
            AND l.country     = ?
            AND l.price       = ?
            AND l.source      = ?
            AND l.post_date   = ?
            AND l.sector      = ?
            AND l.revenue     = ?
            AND l.description = ?
            ORDER BY l.created_at DESC
            """,
            (
                broker_id,
                access_type,
                country,
                price,
                source,
                post_date,
                sector,
                revenue,
                description,
            ),
        )
        return cursor.fetchall()


def get_listing_by_id(listing_id: int) -> Optional[Tuple]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                id,
                broker_id,
                access_type,
                country,
                privilege,
                price,
                description,
                source,
                post_date,
                sector,
                revenue,
                created_at
            FROM listings
            WHERE id = ?
            """,
            (listing_id,),
        )
        return cursor.fetchone()


def update_listing(listing_id: int,access_type: str,country: str,privilege: str,price: str,description: str,source: str,post_date: str,sector: str,revenue: str,) -> None:

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE listings
            SET
                access_type = ?,
                country     = ?,
                privilege   = ?,
                price       = ?,
                description = ?,
                source      = ?,
                post_date   = ?,
                sector      = ?,
                revenue     = ?
            WHERE id = ?
            """,
            (
                access_type,
                country,
                privilege,
                price,
                description,
                source,
                post_date,
                sector,
                revenue,
                listing_id,
            ),
        )
        conn.commit()


def delete_listing(listing_id: int) -> None:
    """Delete a listing by ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM listings WHERE id = ?",
            (listing_id,),
        )
        conn.commit()


