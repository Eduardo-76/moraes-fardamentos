import re


class IntentParser:

    def parse(self, text):

        original_text = text
        text = text.lower()

        # -----------------------------------
        # ENTRADA DE MALHA
        # -----------------------------------

        if (
            "rolo" in text
            or "rolos" in text
            or "malha" in text
        ):

            quantity = self._extract_quantity(text)
            fabric_name = self._extract_fabric_name(text)

            return {
                "intent": "fabric_entry",
                "label": "Entrada de Malha",
                "quantity": quantity,
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

        # remove quantidade
        text = re.sub(r"\d+", "", text)

        # remove palavras comuns
        words_to_remove = [
            "rolo",
            "rolos",
            "de",
            "malha"
        ]

        words = text.split()

        filtered = [
            w for w in words
            if w not in words_to_remove
        ]

        return " ".join(filtered).strip()