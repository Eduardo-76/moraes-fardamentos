import re
from typing import Any

from app.core.utils import normalize_gender, normalize_name, normalize_size, normalize_text


class AudioParserService:
    def parse_order_text(self, text: str) -> dict[str, Any]:
        clean_text = self._clean_text(text)

        return {
            "client_name": self._extract_client_name(clean_text),
            "quantity": self._extract_total_quantity(clean_text),
            "model": self._extract_model(clean_text),
            "fabric": self._extract_fabric(clean_text),
            "color": self._extract_color(clean_text),
            "items": self._extract_items(clean_text),
            "deadline_text": self._extract_deadline_text(clean_text),
            "raw_text": text,
        }

    def _clean_text(self, text: str) -> str:
        text = text.lower().strip()
        text = text.replace(",", " ")
        text = text.replace(".", " ")
        text = re.sub(r"\s+", " ", text)
        return text

    def _extract_client_name(self, text: str) -> str | None:
        patterns = [
            r"pedido para ([a-záéíóúãõç\s]+?)(?:\s+\d+|\s+com|\s+de|\s+prazo|$)",
            r"cliente ([a-záéíóúãõç\s]+?)(?:\s+\d+|\s+com|\s+de|\s+prazo|$)",
            r"para ([a-záéíóúãõç\s]+?)(?:\s+\d+|\s+com|\s+de|\s+prazo|$)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                name = match.group(1).strip()
            # remove artigos comuns
            name = re.sub(r"^(a|o|para|pro|pra)\s+", "", name)
            return normalize_name(name)
                

        return None

    def _extract_total_quantity(self, text: str) -> int:
        match = re.search(r"(\d+)\s+(?:camisas|camisa|blusas|blusa|calças|calça|peças|peça)", text)
        if match:
            return int(match.group(1))

        quantities = [int(value) for value in re.findall(r"\b\d+\b", text)]
        return quantities[0] if quantities else 0

    def _extract_model(self, text: str) -> str | None:
        model_keywords = {
            "camisa": "Camisa",
            "camisas": "Camisas",
            "blusa": "Blusa",
            "blusas": "Blusas",
            "calça": "Calça",
            "calças": "Calças",
            "short": "Short",
            "bermuda": "Bermuda",
            "gola polo": "Gola Polo",
            "polo": "Gola Polo",
        }

        for keyword, value in model_keywords.items():
            if keyword in text:
                return value

        return None

    def _extract_fabric(self, text: str) -> str | None:
        fabrics = {
            "dryfit": "Dryfit",
            "dry fit": "Dryfit",
            "draifit": "Dryfit",
            "draifite": "Dryfit",
            "drai fit": "Dryfit",
            "pp": "PP",
            "helanca": "Helanca",
            "algodão": "Algodão",
            "poliéster": "Poliéster",
            "malha": "Malha",
        }
        for keyword, value in fabrics.items():
            if keyword in text:
                return value

        return None

    def _extract_color(self, text: str) -> str | None:
        colors = {
            "branca": "Branca",
            "branco": "Branca",
            "preta": "Preta",
            "preto": "Preta",
            "verde": "Verde",
            "azul": "Azul",
            "vermelha": "Vermelha",
            "vermelho": "Vermelha",
            "amarela": "Amarela",
            "amarelo": "Amarela",
            "cinza": "Cinza",
        }

        for keyword, value in colors.items():
            if keyword in text:
                return value

        return None

    def _extract_items(self, text: str) -> list[dict[str, Any]]:
        items = []

        pattern = (
            r"(\d+)\s+"
            r"(pp|p|m|g|gg|xg|xxg)\s+"
            r"(masculina|masculino|feminina|feminino|infantil|unissex)"
        )

        matches = re.findall(pattern, text)

        for quantity, size, gender in matches:
            items.append(
                {
                    "quantity": int(quantity),
                    "size": normalize_size(size),
                    "gender": self._normalize_gender_word(gender),
                }
            )

        return items

    def _normalize_gender_word(self, gender: str) -> str:
        gender = normalize_text(gender) or ""

        mapping = {
            "masculino": "Masculina",
            "masculina": "Masculina",
            "feminino": "Feminina",
            "feminina": "Feminina",
            "infantil": "Infantil",
            "unissex": "Unissex",
        }

        return mapping.get(gender.lower(), normalize_gender(gender) or gender)

    def _extract_deadline_text(self, text: str) -> str | None:
        match = re.search(r"prazo\s+(.+)$", text)
        if match:
            return match.group(1).strip()

        return None