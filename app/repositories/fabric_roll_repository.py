from app.core.database import get_connection
from app.models.fabric_roll_model import FabricRollModel, FabricRollLocation
import sqlite3

class FabricRollRepository:

    def create_roll(self, roll: FabricRollModel) -> int:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO fabric_rolls
            (
                name,
                total_quantity,
                reserved_quantity
            )
            VALUES (?, ?, ?)
            """,
            (roll.name, roll.total_quantity, roll.reserved_quantity),
        )

        roll_id = cursor.lastrowid

        for loc in roll.locations:
            cursor.execute(
                """
                INSERT INTO fabric_roll_locations (roll_id, location_name, quantity)
                VALUES (?, ?, ?)
                """,
                (roll_id, loc.location_name, loc.quantity),
            )

        conn.commit()
        conn.close()
        return roll_id

    def list_rolls(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM fabric_rolls")
        rolls = cursor.fetchall()

        result = []

        for r in rolls:
            cursor.execute(
                "SELECT location_name, quantity FROM fabric_roll_locations WHERE roll_id = ?",
                (r["id"],),
            )
            locations = [
                FabricRollLocation(loc["location_name"], loc["quantity"])
                for loc in cursor.fetchall()
            ]

            result.append(
                FabricRollModel(
                    id=r["id"],
                    name=r["name"],
                    total_quantity=r["total_quantity"],
                    reserved_quantity=r["reserved_quantity"],
                    locations=locations,
                )
            )

        conn.close()
        return result
    


    def update_roll(self, roll):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE fabric_rolls
            SET
                name = ?,
                total_quantity = ?,
                reserved_quantity = ?
            WHERE id = ?
        """, (
            roll.name,
            roll.total_quantity,
            roll.reserved_quantity,
            roll.id
        ))

        cursor.execute("""
            DELETE FROM fabric_roll_locations
            WHERE roll_id = ?
        """, (roll.id,))

        for loc in roll.locations:

            cursor.execute("""
                INSERT INTO fabric_roll_locations (
                    roll_id,
                    location_name,
                    quantity
                )
                VALUES (?, ?, ?)
            """, (
                roll.id,
                loc.location_name,
                loc.quantity
            ))

        conn.commit()
        conn.close()

        print("Rolo atualizado com sucesso")

    def delete_roll(self, roll_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM fabric_roll_locations
            WHERE roll_id = ?
        """, (roll_id,))

        cursor.execute("""
            DELETE FROM fabric_roll_movements
            WHERE roll_id = ?
        """, (roll_id,))

        cursor.execute("""
            DELETE FROM fabric_rolls
            WHERE id = ?
        """, (roll_id,))

        conn.commit()
        conn.close()

    def create_transfer(self, roll_id, from_location, to_location, quantity):
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
            quantity
        ))

        conn.commit()
        conn.close()