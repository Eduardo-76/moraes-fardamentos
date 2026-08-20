import re

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

        elif operation == "entry":

            to_location = self._extract_fabric_location(text)

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

            items = self._extract_order_items(text)

            if items:
                quantity = sum(
                    item["quantity"]
                    for item in items
                )

            return {
                "intent": "create_order",
                "label": "Criar Pedido",

                "client_name": client_name,

                "quantity": quantity,

                "product_name": product,

                "items": items,

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

    def _extract_order_items(self, text):

        items = []

        pattern = re.compile(
            r"""
            (?P<quantity>\d+)

            \s+

            (?:camisa[s]?|blusa[s]?|short[s]?|farda[s]?|uniforme[s]?)?

            [\s,.-]*

            (?P<size>
                XGG
                |XG
                |GG
                |PP
                |P
                |M
                |G
            )

            [\s,.-]+

            (?P<gender>
                masculina
                |masculino
                |masculinas
                |masculinos
                |feminina
                |feminino
                |femininas
                |femininos
                |masc
                |femi
            )
            """,
            re.IGNORECASE | re.VERBOSE,
        )

        for match in pattern.finditer(text):

            quantity = int(
                match.group("quantity")
            )

            size = match.group("size").upper()

            gender = self._normalize_order_gender(
                match.group("gender")
            )

            items.append(
                {
                    "size": size,
                    "gender": gender,
                    "quantity": quantity,
                }
            )

        return items

    def _normalize_order_gender(self, gender):

        gender = gender.lower().strip()

        masculine = [
            "masculina",
            "masculino",
            "masculinas",
            "masculinos",
            "masc",
        ]

        feminine = [
            "feminina",
            "feminino",
            "femininas",
            "femininos",
            "femi",
        ]

        if gender in masculine:
            return "Masculina"

        if gender in feminine:
            return "Feminina"

        return gender.capitalize()

    def _extract_quantity(self, text):

        match = re.search(r"\d+", text)

        if match:
            return int(match.group())

        return 0

    def _extract_fabric_name(self, text):

        text = text.lower()

        # Remove números
        text = re.sub(r"\d+", "", text)

        remove_words = [
            # operação
            "entrada",
            "entrar",
            "entrei",
            "adicionar",
            "adiciona",
            "acrescentar",
            "acrescentei",

            "saida",
            "saída",
            "retirar",
            "retirada",
            "remover",

            "transferir",
            "transferência",
            "mover",
            "mandar",

            # rolo
            "rolo",
            "rolos",
            "rollo",
            "rollos",
            "rolios",
            "holes",
            "hole",
            "holles",

            # categoria
            "malha",

            # conectores
            "de",
            "da",
            "do",
            "na",
            "no",
            "em",

            # locais
            "depósito",
            "deposito",
            "casa",
            "costureira",
            "costureiras",
            "empresa",
        ]

        words = text.split()

        filtered = [
            word
            for word in words
            if word not in remove_words
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
            "Costureiras",
            "Empresa",
        ]

        normalized_word = (
            word
            .strip()
            .lower()
        )

        aliases = {
            "deposito": "Depósito",
            "depósito": "Depósito",

            "casa": "Casa",

            "costureira": "Costureiras",
            "costureiras": "Costureiras",

            "empresa": "Empresa",
        }

        if normalized_word in aliases:
            return aliases[normalized_word]

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

    def _extract_fabric_location(self, text):

        text = text.lower()

        locations = [
            "Depósito",
            "Casa",
            "Costureiras",
            "Empresa",
        ]

        patterns = [
            r"\bna\s+(depósito|deposito|casa|empresa|costureira|costureiras)\b",
            r"\bno\s+(depósito|deposito|casa|empresa|costureiro|costureiros)\b",
            r"\bem\s+(depósito|deposito|casa|empresa|costureira|costureiras)\b",
            r"\bpara\s+(depósito|deposito|casa|empresa|costureira|costureiras)\b",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text
            )

            if not match:
                continue

            candidate = match.group(1)

            normalized = self._normalize_location(
                candidate
            )

            if normalized:
                return normalized

        return None    