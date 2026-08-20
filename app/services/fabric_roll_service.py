from app.repositories.fabric_roll_repository import FabricRollRepository
from app.models.fabric_roll_model import FabricRollModel
from app.repositories.fabric_roll_movement_repository import FabricRollMovementRepository
import re
from difflib import SequenceMatcher
import unicodedata


class FabricRollService:
    def __init__(self):
        self.repo = FabricRollRepository()
        self.movement_repo = FabricRollMovementRepository()

    def create_roll(self, roll: FabricRollModel):
        total_locations = sum(loc.quantity for loc in roll.locations)

        if total_locations != roll.total_quantity:
            raise ValueError("Soma das localizações diferente do total")

        return self.repo.create_roll(roll)

    def list_rolls(self):
        return self.repo.list_rolls()

    def update_roll(self, roll):
        return self.repo.update_roll(roll)

    def register_movement(
        self,
        roll_id,
        quantity,
        movement_type,
        location_name=None,
    ):

        self.movement_repo.create_movement(
            roll_id=roll_id,
            movement_type=movement_type,
            location_name=location_name,
            quantity=quantity
        )

    def delete_roll(self, roll_id):
        self.repo.delete_roll(roll_id)

    def register_transfer(
        self,
        roll_id,
        from_location,
        to_location,
        qty
    ):
        self.movement_repo.create_transfer(
            roll_id,
            from_location,
            to_location,
            qty
        )

    def find_by_name(self, name):

        rolls = self.repo.list_rolls()

        search = self._normalize_text(name)

        for roll in rolls:

            roll_name = self._normalize_text(
                roll.name
            )

            # match parcial
            if search in roll_name:
                return roll

            if roll_name in search:
                return roll

            # match por palavras
            search_words = search.split()
            roll_words = roll_name.split()

            matches = sum(
                1 for w in search_words
                if w in roll_words
            )

            if matches >= 2:
                return roll

        return None
    
    def _normalize_text(self, text):

        text = text.lower()

        # remove pontuação
        text = re.sub(r"[^\w\s]", "", text)

        # remove palavras comuns
        remove_words = [
            "rolo",
            "rolos",
            "malha",
            "de",
            "da",
            "do",
            "colos",
            "holes",
            "rollos",
        ]

        words = text.split()

        filtered = [
            w for w in words
            if w not in remove_words
        ]

        return " ".join(filtered)

    def register_entry(
        self,
        roll_id,
        location,
        quantity
    ):

        self.movement_repo.create_movement(
            roll_id=roll_id,
            movement_type="entrada",
            location_name=location,
            quantity=quantity,
        )

    def register_exit(
        self,
        roll_id,
        location,
        quantity
    ):

        self.movement_repo.create_movement(
            roll_id=roll_id,
            movement_type="saida",
            location_name=location,
            quantity=quantity,
        )

    def reserve_quantity(
        self,
        roll,
        quantity
    ):

        available = (
            roll.total_quantity
            - roll.reserved_quantity
        )

        if quantity > available:

            raise Exception(
                "Quantidade indisponível para reserva."
            )

        roll.reserved_quantity += quantity

        self.repository.update_roll(roll)

        print("Quantidade reservada")

    def _normalize_text(self, text):

        text = unicodedata.normalize(
            "NFKD",
            text
        )

        text = (
            text
            .encode("ASCII", "ignore")
            .decode("utf-8")
        )

        return text.strip().lower()

    def find_similar_rolls(
        self,
        name: str,
        limit: int = 5
    ):

        if not name:
            return []

        target = self._normalize_text(name)

        rolls = self.list_rolls()

        matches = []

        for roll in rolls:

            roll_name = self._normalize_text(
                roll.name
            )

            ratio = SequenceMatcher(
                None,
                target,
                roll_name
            ).ratio()

            if target in roll_name:
                ratio += 0.25

            matches.append(
                (
                    ratio,
                    roll
                )
            )

        matches.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return [
            roll
            for score, roll in matches[:limit]
            if score >= 0.25
        ]