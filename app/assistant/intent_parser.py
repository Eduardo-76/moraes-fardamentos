import re

from numpy.ma import product
from app.core.constants import FABRIC_LOCATIONS
from difflib import get_close_matches


class IntentParser:

    def parse(self, text):

        product = self._extract_product_name(text)
        quantity = self._extract_order_quantity(text)
        client_name = self._extract_client_name(text)

        original_text = text
        text = text.lower()

        operation = "entry"

        # ----------------------------
        # TRANSFERÊNCIA
        # ----------------------------

        transfer_words = [
            "transferir",
            "transferência",
            "mover",
            "mandar",
        ]

        # ----------------------------
        # SAÍDA
        # ----------------------------

        exit_words = [
            "saida",
            "saída",
            "retirar",
            "remove",
            "remover",
            "tirar",
            "sairam",
            "saíram",
        ]

        words = text.split()

        if any(word in words for word in transfer_words):

            operation = "transfer"

        elif any(word in words for word in exit_words):

            operation = "exit"

        
        # -----------------------------------
        # ENTRADA DE MALHA
        # -----------------------------------

        if (
            "rolo" in text
            or "rolos" in text
            or "malha" in text
        ):

            quantity = self._extract_quantity(text)

            from_location = None
            to_location = None

            if operation == "transfer":

                from_location, to_location = (
                    self._extract_transfer_locations(text)
                )

            fabric_name = self._extract_fabric_name(text)

            return {
                "intent": f"fabric_{operation}",
                "label": f"Operação: {operation}",
                "quantity": quantity,
                "from_location": from_location,
                "to_location": to_location,
                "fabric_name": fabric_name,
                "raw_text": original_text
            }

        # -----------------------------------
        # PEDIDO
        # -----------------------------------

        if (
            "cliente" in text
            or "blusa" in text
            or "camisa" in text
            or "pedido" in text
        ):

            return {
                "intent": "create_order",
                "label": "Criar Pedido",

                "client_name": client_name,

                "quantity": quantity,

                "product_name": product,

                "raw_text": original_text
            }

        # -----------------------------------
        # DESCONHECIDO
        # -----------------------------------

        return {
            "intent": "unknown",
            "label": "Não identificado",
            "raw_text": original_text
        }

    # ===================================
    # HELPERS
    # ===================================

    def _extract_quantity(self, text):

        match = re.search(r"\d+", text)

        if match:
            return int(match.group())

        return 0

    def _extract_fabric_name(self, text):

        # remove números
        text = re.sub(r"\d+", "", text)

        # remove palavras comuns
        remove_words = [

            # operação
            "rolo",
            "rolos",
            "rollo",
            "rollos",
            "rolios",
            "holes",
            "hole",
            "holles",

            # conectores
            "de",
            "da",
            "do",

            # categoria
            "malha",
        ]

        words = text.split()

        filtered = [
            w for w in words
            if w not in remove_words
        ]

        result = " ".join(filtered).strip()

        result = result.replace(".", "")
        result = result.replace(",", "")

        return result
    
    def _extract_transfer_locations(self, text):

        text = text.lower()

        words = text.split()

        from_location = None
        to_location = None

        # -----------------------------------
        # PROCURA "DO"
        # -----------------------------------

        for i, word in enumerate(words):

            if word in ["do", "da"]:

                if i + 1 < len(words):

                    candidate = words[i + 1]

                    normalized = self._normalize_location(
                        candidate.capitalize()
                    )

                    if normalized:

                        from_location = normalized

            # -----------------------------------
            # PROCURA "PARA"
            # -----------------------------------

            if word == "para":

                if i + 1 < len(words):

                    candidate = words[i + 1]

                    normalized = self._normalize_location(
                        candidate.capitalize()
                    )

                    if normalized:

                        to_location = normalized

        return from_location, to_location
    
    def _normalize_location(self, word):

        locations = [
            "Depósito",
            "Casa",
            "Costureira"
        ]

        match = get_close_matches(
            word,
            locations,
            n=1,
            cutoff=0.6
        )

        if match:
            return match[0]

        return None
    
    def _extract_client_name(self, text):

        patterns = [

            r"cliente\s+([a-zA-ZÀ-ÿ\s]+?)\s+pedido",

            r"cliente\s+([a-zA-ZÀ-ÿ\s]+?)\s+quer",

            r"cliente\s+([a-zA-ZÀ-ÿ\s]+?)\s+pediu",

        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                return match.group(1).strip().title()

        return None
    
    def _extract_order_quantity(self, text):

        match = re.search(r"(\d+)", text)

        if match:

            return int(match.group(1))

        return 0
    
    def _extract_product_name(self, text):

        products = [

            "camisa",
            "camisas",

            "blusa",
            "blusas",

            "short",
            "shorts",

            "farda",
            "fardas",

            "uniforme",
            "uniformes",
        ]

        text = text.lower()

        for product in products:

            if product in text:

                return product.capitalize()

        return None