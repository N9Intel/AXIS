from pathlib import Path
import sqlite3
from typing import List, Tuple, Optional


DB_PATH = Path("axis.db") #should change to .env file


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
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
                raw_title TEXT,
                raw_text TEXT,
                raw_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (broker_id) REFERENCES brokers(id) ON DELETE CASCADE
            )
            """
        )

        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_brokers_name "
            "ON brokers(name)"
        )

        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_listings_broker_id "
            "ON listings(broker_id)"
        )

        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_listings_sector "
            "ON listings(sector)"
        )

        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_listings_created_at "
            "ON listings(created_at)"
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
    raw_title: str = "",
    raw_text: str = "",
    raw_url: str = "",
) -> int:
    """
    Insert a listing.

    raw_title/raw_text/raw_url are new in v0.4. Existing callers can ignore them;
    they default to empty strings for backward compatibility.
    """
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
                revenue,
                raw_title,
                raw_text,
                raw_url
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                raw_title,
                raw_text,
                raw_url,
            ),
        )
        conn.commit()
        return cursor.lastrowid


def get_listing_by_id(listing_id: int) -> Optional[Tuple]:
    """
    Return a single listing row by ID, joined with broker name.

    Row layout:
    (
        id,
        broker_name,
        access_type,
        country,
        privilege,
        price,
        description,
        source,
        post_date,
        sector,
        revenue,
        raw_title,
        raw_text,
        raw_url,
        created_at,
    )
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
                l.raw_title,
                l.raw_text,
                l.raw_url,
                l.created_at
            FROM listings l
            JOIN brokers b ON l.broker_id = b.id
            WHERE l.id = ?
            """,
            (listing_id,),
        )
        return cursor.fetchone()


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
                l.raw_title,
                l.raw_text,
                l.raw_url,
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
            l.raw_title,
            l.raw_text,
            l.raw_url,
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
            l.raw_title,
            l.raw_text,
            l.raw_url,
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

    tokens = [t.strip().lower() for t in q.split() if t.strip()]
    if not tokens:
        return []

    # We build a WHERE clause like:
    # (field1 LIKE ? OR field2 LIKE ? OR ...)  AND
    # (field1 LIKE ? OR field2 LIKE ? OR ...)  AND ...
    field_expr = """
        LOWER(b.name)      LIKE ?
     OR LOWER(l.access_type) LIKE ?
     OR LOWER(l.country)     LIKE ?
     OR LOWER(l.privilege)   LIKE ?
     OR LOWER(l.price)       LIKE ?
     OR LOWER(l.description) LIKE ?
     OR LOWER(l.source)      LIKE ?
     OR LOWER(l.post_date)   LIKE ?
     OR LOWER(l.sector)      LIKE ?
     OR LOWER(l.revenue)     LIKE ?
    """

    where_clauses = []
    params: list[str] = []

    for token in tokens:
        pattern = f"%{token}%"
        where_clauses.append(f"({field_expr})")
        # 10 fields → 10 params per token
        params.extend([pattern] * 10)

    where_sql = " AND ".join(where_clauses)

    sql = f"""
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
            l.raw_title,
            l.raw_text,
            l.raw_url,
            l.created_at
        FROM listings l
        JOIN brokers b ON l.broker_id = b.id
        WHERE {where_sql}
        ORDER BY l.created_at DESC
    """

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
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
            l.raw_title,
            l.raw_text,
            l.raw_url,
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


def get_summary_counts() -> Tuple[int, int]:
    """
    Return (total_brokers, total_listings).
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM brokers")
        total_brokers = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM listings")
        total_listings = cursor.fetchone()[0] or 0

        return total_brokers, total_listings


def get_broker_listing_counts(limit: int = 10) -> List[Tuple]:
    """
    Return top brokers by listing count.

    Each row: (broker_name, listing_count)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                b.name AS broker_name,
                COUNT(l.id) AS listing_count
            FROM brokers b
            LEFT JOIN listings l ON l.broker_id = b.id
            GROUP BY b.id
            ORDER BY listing_count DESC, broker_name ASC
            LIMIT ?
            """,
            (limit,),
        )
        return cursor.fetchall()


def get_sector_counts(limit: int = 10) -> List[Tuple]:
    """
    Return top sectors by listing count (ignores empty/null sectors).

    Each row: (sector, listing_count)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                COALESCE(NULLIF(l.sector, ''), 'unknown') AS sector,
                COUNT(*) AS listing_count
            FROM listings l
            GROUP BY sector
            ORDER BY listing_count DESC, sector ASC
            LIMIT ?
            """,
            (limit,),
        )
        return cursor.fetchall()




