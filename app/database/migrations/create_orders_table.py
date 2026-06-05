from app.core.database import get_connection


def up():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            client_name TEXT NOT NULL,

            product_name TEXT NOT NULL,

            color TEXT,

            size TEXT,

            quantity INTEGER NOT NULL,

            due_date TEXT,

            notes TEXT,

            status TEXT DEFAULT 'PENDENTE',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

    print("Tabela orders criada.")