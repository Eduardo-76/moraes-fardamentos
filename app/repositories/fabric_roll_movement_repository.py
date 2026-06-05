from app.core.database import get_connection


class FabricRollMovementRepository:


    def create(self, roll_id, location_name, qty, movement_type="saida"):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO fabric_roll_movements
            (
                roll_id,
                movement_type,
                location_name,
                quantity
            )
            VALUES (?, ?, ?, ?)
        """, (
            roll_id,
            movement_type,
            location_name,
            qty
        ))

        conn.commit()
        conn.close()

    # 🔥 NOVO
    def create_transfer(
        self,
        roll_id,
        from_location,
        to_location,
        qty
    ):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO fabric_roll_movements
            (
                roll_id,
                movement_type,
                from_location,
                to_location,
                quantity
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            roll_id,
            "transferencia",
            from_location,
            to_location,
            qty
        ))

        conn.commit()
        conn.close()

    def list_all(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                m.*,
                r.name AS roll_name
            FROM fabric_roll_movements m
            JOIN fabric_rolls r
                ON r.id = m.roll_id
            ORDER BY m.created_at DESC
        """)

        rows = cursor.fetchall()

        conn.close()

        return rows
    
    def create_movement(
        self,
        roll_id,
        movement_type,
        location_name,
        quantity
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO fabric_roll_movements (
                roll_id,
                movement_type,
                location_name,
                quantity
            )
            VALUES (?, ?, ?, ?)
        """, (
            roll_id,
            movement_type,
            location_name,
            quantity
        ))

        conn.commit()
        conn.close()