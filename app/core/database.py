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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fabric_rolls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        total_quantity INTEGER NOT NULL,
        reserved_quantity INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fabric_roll_movements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_id INTEGER NOT NULL,
        movement_type TEXT NOT NULL,
        location_name TEXT,
        from_location TEXT,
        to_location TEXT,
        quantity INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fabric_roll_locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_id INTEGER NOT NULL,
        location_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (roll_id) REFERENCES fabric_rolls(id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        city TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        audio_id INTEGER,
        model TEXT,
        fabric TEXT,
        type TEXT,
        quantity INTEGER,
        deadline TEXT,
        priority TEXT,
        unit_value REAL DEFAULT 0,
        total_value REAL,
        paid INTEGER DEFAULT 0,
        stock_reserved INTEGER DEFAULT 0,
        stock_withdrawn INTEGER DEFAULT 0,
        withdrawn_at TEXT,
        status TEXT DEFAULT 'Pendente',
        notes TEXT,
        current_stage TEXT DEFAULT 'Recepção',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE SET NULL,
        FOREIGN KEY (audio_id) REFERENCES audios(id) ON DELETE SET NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        size TEXT,
        gender TEXT,
        quantity INTEGER,
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
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
    """)

    # Histórico de mudanças de status do pedido.
    # Também serve para bancos antigos que ainda não possuem esta tabela:
    # CREATE TABLE IF NOT EXISTS simplesmente cria a estrutura faltante.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_status_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        old_status TEXT,
        new_status TEXT NOT NULL,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model TEXT,
        type TEXT,
        color TEXT,
        fabric TEXT,
        stock_group TEXT,
        stock_category TEXT,
        reference TEXT,
        total_quantity INTEGER DEFAULT 0,
        reserved_quantity INTEGER DEFAULT 0,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_entry_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stock_entry_id INTEGER NOT NULL,
        size TEXT,
        gender TEXT,
        quantity INTEGER,
        reserved_quantity INTEGER DEFAULT 0,
        FOREIGN KEY (stock_entry_id) REFERENCES stock_entries(id) ON DELETE CASCADE
    )
    """)

    # Reservas de estoque vinculadas aos pedidos.
    # Necessária para reserva, cancelamento, retirada e exclusão de pedidos.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_stock_reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        stock_entry_id INTEGER NOT NULL,
        stock_item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'RESERVED',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        cancelled_at TIMESTAMP,
        withdrawn_at TIMESTAMP,
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
        FOREIGN KEY (stock_entry_id) REFERENCES stock_entries(id) ON DELETE CASCADE,
        FOREIGN KEY (stock_item_id) REFERENCES stock_entry_items(id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_movements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stock_entry_id INTEGER NOT NULL,
        movement_type TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (stock_entry_id) REFERENCES stock_entries(id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_movement_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movement_id INTEGER NOT NULL,
        size TEXT,
        gender TEXT,
        quantity INTEGER,
        FOREIGN KEY (movement_id) REFERENCES stock_movements(id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attachments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        file_name TEXT NOT NULL,
        file_type TEXT NOT NULL,
        file_path TEXT NOT NULL,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS generated_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        sector TEXT NOT NULL,
        message_text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_name TEXT NOT NULL,
        file_name TEXT NOT NULL,
        file_path TEXT NOT NULL,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS app_metadata (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        payment_method TEXT NOT NULL,
        paid_at TEXT NOT NULL,
        notes TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
    )
    """)

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
        ensure_orders_columns(connection)
        ensure_stock_columns(connection)
        ensure_stock_movement_columns(connection)
        ensure_payments_table(connection)
        seed_metadata(connection)
    finally:
        connection.close()


def ensure_orders_columns(connection: Connection) -> None:
    cursor = connection.cursor()
    cursor.execute("PRAGMA table_info(orders)")
    columns = {row["name"] for row in cursor.fetchall()}

    if "stock_reserved" not in columns:
        cursor.execute(
            "ALTER TABLE orders ADD COLUMN stock_reserved INTEGER DEFAULT 0"
        )
    if "status" not in columns:
        cursor.execute(
            "ALTER TABLE orders ADD COLUMN status TEXT DEFAULT 'Pendente'"
        )
    if "unit_value" not in columns:
        cursor.execute(
            "ALTER TABLE orders ADD COLUMN unit_value REAL DEFAULT 0"
        )

    connection.commit()


def ensure_stock_columns(connection: Connection) -> None:
    cursor = connection.cursor()

    cursor.execute("PRAGMA table_info(stock_entries)")
    stock_columns = {row["name"] for row in cursor.fetchall()}

    if "reserved_quantity" not in stock_columns:
        cursor.execute(
            "ALTER TABLE stock_entries ADD COLUMN reserved_quantity INTEGER DEFAULT 0"
        )

    cursor.execute("PRAGMA table_info(stock_entry_items)")
    item_columns = {row["name"] for row in cursor.fetchall()}

    if "reserved_quantity" not in item_columns:
        cursor.execute(
            "ALTER TABLE stock_entry_items ADD COLUMN reserved_quantity INTEGER DEFAULT 0"
        )

    connection.commit()


def ensure_stock_movement_columns(connection: Connection) -> None:
    """
    Compatibilidade com bancos criados por versões anteriores.

    Algumas versões antigas criaram stock_movements com stock_item_id
    ou roll_id. A versão atual usa stock_entry_id. Não apagamos o histórico:
    apenas adicionamos as colunas que a estrutura atual precisa.
    """
    cursor = connection.cursor()

    cursor.execute("PRAGMA table_info(stock_movements)")
    columns = {row["name"] for row in cursor.fetchall()}

    if "stock_entry_id" not in columns:
        cursor.execute(
            "ALTER TABLE stock_movements ADD COLUMN stock_entry_id INTEGER"
        )

    if "notes" not in columns:
        cursor.execute(
            "ALTER TABLE stock_movements ADD COLUMN notes TEXT"
        )

    connection.commit()


def ensure_payments_table(connection: Connection) -> None:
    connection.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            paid_at TEXT NOT NULL,
            notes TEXT,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
        )
    """)
    connection.commit()
