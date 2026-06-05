import sqlite3
from app.core.config import DB_PATH


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database() -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS app_meta (key TEXT PRIMARY KEY, value TEXT)')
    conn.commit()
    conn.close()

import sqlite3
from sqlite3 import Connection

from app.core.config import DATABASE_PATH
from app.core.constants import ORDER_STAGES, PRIORITIES, STAGE_STATUSES


def get_connection() -> Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection


def create_tables(connection: Connection) -> None:
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            city TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            model TEXT,
            fabric TEXT,
            type TEXT,
            quantity INTEGER,
            deadline TEXT,
            priority TEXT,
            total_value REAL,
            paid INTEGER DEFAULT 0,
            notes TEXT,
            current_stage TEXT DEFAULT 'Recepção',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE SET NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            size TEXT,
            gender TEXT,
            quantity INTEGER,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS order_stages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            stage_name TEXT NOT NULL,
            status TEXT DEFAULT 'Em espera',
            notes TEXT,
            responsible TEXT,
            started_at TEXT,
            finished_at TEXT,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS stock_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT,
            fabric TEXT,
            color TEXT,
            size TEXT,
            gender TEXT,
            quantity INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS stock_movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_item_id INTEGER NOT NULL,
            movement_type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (stock_item_id) REFERENCES stock_items(id) ON DELETE CASCADE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS attachments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            file_name TEXT NOT NULL,
            file_type TEXT NOT NULL,
            file_path TEXT NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS generated_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            sector TEXT NOT NULL,
            message_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS app_metadata (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """
    )

    connection.commit()


def seed_metadata(connection: Connection) -> None:
    cursor = connection.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO app_metadata (key, value) VALUES (?, ?)",
        ("default_stage", "Recepção"),
    )

    cursor.execute(
        "INSERT OR IGNORE INTO app_metadata (key, value) VALUES (?, ?)",
        ("available_stages", ",".join(ORDER_STAGES)),
    )

    cursor.execute(
        "INSERT OR IGNORE INTO app_metadata (key, value) VALUES (?, ?)",
        ("available_statuses", ",".join(STAGE_STATUSES)),
    )

    cursor.execute(
        "INSERT OR IGNORE INTO app_metadata (key, value) VALUES (?, ?)",
        ("available_priorities", ",".join(PRIORITIES)),
    )

    connection.commit()


def initialize_database() -> None:
    connection = get_connection()
    try:
        create_tables(connection)
        seed_metadata(connection)
    finally:
        connection.close()