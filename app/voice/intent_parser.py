import re


class IntentParser:

    def parse(self, text):

        original_text = text
        text = text.lower().strip()

        # ===================================
        # OPERAÇÃO
        # ===================================

        operation = self._detect_operation(text)

        # ===================================
        # PEDIDO
        # ===================================
        #
        # Pedido tem prioridade quando existem
        # sinais claros de cliente/pedido/produto.
        #
        # Isso evita que uma frase como:
        #
        # "Cliente Eduardo pediu camisas de malha"
        #
        # seja confundida com entrada de malha.
        #

        if self._is_order(text):

            items = self._extract_order_items(text)

            quantity = sum(
                item["quantity"]
                for item in items
            )

            if quantity == 0:
                quantity = self._extract_quantity(text)

            return {
                "intent": "create_order",
                "label": "Criar Pedido",

                "client_name": self._extract_client_name(text),

                "city": self._extract_city(text),

                "quantity": quantity,

                "product_name": self._extract_product_name(text),

                "items": items,

                "model": self._extract_model(text),

                "order_type": self._extract_order_type(text),

                "fabric": self._extract_order_fabric(text),

                "deadline": self._extract_deadline(text),

                "raw_text": original_text
            }
        # ===================================
        # ENTRADA / SAÍDA / TRANSFERÊNCIA
        # DE MALHA
        # ===================================

        if self._is_fabric_command(text):

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

        # ===================================
        # DESCONHECIDO
        # ===================================

        return {
            "intent": "unknown",
            "label": "Não identificado",
            "raw_text": original_text
        }

    # ===================================
    # DETECTAR OPERAÇÃO
    # ===================================

    def _detect_operation(self, text):

        transfer_words = [
            "transferir",
            "transferência",
            "transferencia",
            "mover",
            "mandar",
        ]

        exit_words = [
            "saida",
            "saída",
            "retirar",
            "retirada",
            "remove",
            "remover",
            "tirar",
            "sairam",
            "saíram",
        ]

        words = text.split()

        if any(word in words for word in transfer_words):
            return "transfer"

        if any(word in words for word in exit_words):
            return "exit"

        return "entry"

    # ===================================
    # DETECTAR PEDIDO
    # ===================================

    def _is_order(self, text):

        order_words = [
            "cliente",
            "pedido",
            "pediu",
            "pedir",
            "encomendou",
            "encomenda",
        ]

        product_words = [
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

        has_order_word = any(
            word in text
            for word in order_words
        )

        has_product_word = any(
            word in text
            for word in product_words
        )

        return (
            has_order_word
            or (
                has_product_word
                and not self._is_fabric_command(text)
            )
        )

    # ===================================
    # DETECTAR MALHA
    # ===================================

    def _is_fabric_command(self, text):

        return (
            "rolo" in text
            or "rolos" in text
            or "malha" in text
        )

    # ===================================
    # ITENS DO PEDIDO
    # ===================================

    def _extract_order_items(self, text):

        items = []

        pattern = re.compile(
            r"""
            (?P<quantity>\d+)

            \s*

            (?:camisa[s]?
            |blusa[s]?
            |short[s]?
            |farda[s]?
            |uniforme[s]?)?

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
                |masc

                |feminina
                |feminino
                |femininas
                |femininos
                |femi

                |infantil
                |infantis
                |infantil masculino
                |infantil feminina
                |infantil feminino
            )
            """,
            re.IGNORECASE | re.VERBOSE,
        )

        for match in pattern.finditer(text):

            quantity = int(
                match.group("quantity")
            )

            size = (
                match.group("size")
                .upper()
            )

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

    # ===================================
    # NORMALIZAR GÊNERO
    # ===================================

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

        infantil = [
            "infantil",
            "infantis",
            "infantil masculino",
            "infantil feminina",
            "infantil feminino",
        ]

        if gender in masculine:
            return "Masculina"

        if gender in feminine:
            return "Feminina"

        if gender in infantil:
            return "Infantil"

        return gender.capitalize()

    # ===================================
    # QUANTIDADE
    # ===================================

    def _extract_quantity(self, text):

        match = re.search(
            r"\d+",
            text
        )

        if match:
            return int(match.group())

        return 0

    # ===================================
    # CLIENTE
    # ===================================

    def _extract_client_name(self, text):

        patterns = [

            # Exemplo:
            # Cliente Eduardo da cidade de Piracuruca pediu...
            r"cliente\s+(.+?)\s+(?:da\s+cidade\s+de|cidade\s+de)",

            # Exemplo:
            # Cliente Eduardo pediu...
            r"cliente\s+(.+?)\s+(?:pediu|pedido|quer|encomendou|encomenda)",

            # Exemplo:
            # Cliente Eduardo, pediu...
            r"cliente\s+(.+?)\s*,",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                name = (
                    match.group(1)
                    .strip()
                    .title()
                )

                return name

        return None

    def _extract_city(self, text):

        patterns = [

            # Exemplo:
            # da cidade de Piracuruca pediu
            r"(?:da\s+cidade\s+de|cidade\s+de)\s+(.+?)\s+(?:pediu|pedido|quer|encomendou|encomenda)",

            # Exemplo:
            # cidade de Piracuruca,
            r"(?:da\s+cidade\s+de|cidade\s+de)\s+(.+?)(?:,|$)",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                city = (
                    match.group(1)
                    .strip()
                    .title()
                )

                return city

        return None

    # ===================================
    # PRODUTO
    # ===================================

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

        for product in products:

            if product in text:

                return product.rstrip("s").capitalize()

        return None

    # ===================================
    # MODELO
    # ===================================

    def _extract_model(self, text):

        models = [
            "normal",
            "polo",
            "social",
            "regata",
        ]

        for model in models:

            if model in text:

                return model.capitalize()

        return None

    # ===================================
    # TIPO
    # ===================================

    def _extract_order_type(self, text):

        types = [
            "estampada toda",
            "estampado toda",
            "estampada",
            "estampado",
            "bordada",
            "bordado",
            "lisa",
        ]

        for order_type in types:

            if order_type in text:

                return order_type.title()

        return None

    # ===================================
    # PRAZO
    # ===================================

    def _extract_deadline(self, text):

        # Exemplo:
        # dia 18 de 8 de 2026

        match = re.search(
            r"dia\s+(\d{1,2})\s+de\s+(\d{1,2})\s+de\s+(\d{4})",
            text
        )

        if match:

            day = int(match.group(1))
            month = int(match.group(2))
            year = int(match.group(3))

            return (
                f"{year:04d}-"
                f"{month:02d}-"
                f"{day:02d}"
            )

        return None

    # ===================================
    # NOME DA MALHA
    # ===================================

    def _extract_fabric_name(self, text):

        text = text.lower()

        text = re.sub(
            r"\d+",
            "",
            text
        )

        remove_words = [

            # operações
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
            "transferencia",
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

        result = " ".join(
            filtered
        ).strip()

        result = result.replace(
            ".",
            ""
        )

        result = result.replace(
            ",",
            ""
        )

        return result

    # ===================================
    # TRANSFERÊNCIA
    # ===================================

    def _extract_transfer_locations(self, text):

        words = text.lower().split()

        from_location = None
        to_location = None

        for i, word in enumerate(words):

            if word in ["do", "da"]:

                if i + 1 < len(words):

                    candidate = words[i + 1]

                    normalized = (
                        self._normalize_location(
                            candidate
                        )
                    )

                    if normalized:
                        from_location = normalized

            if word == "para":

                if i + 1 < len(words):

                    candidate = words[i + 1]

                    normalized = (
                        self._normalize_location(
                            candidate
                        )
                    )

                    if normalized:
                        to_location = normalized

        return (
            from_location,
            to_location
        )

    # ===================================
    # NORMALIZAR LOCAL
    # ===================================

    def _normalize_location(self, word):

        aliases = {

            "deposito": "Depósito",
            "depósito": "Depósito",

            "casa": "Casa",

            "costureira": "Costureiras",
            "costureiras": "Costureiras",

            "empresa": "Empresa",
        }

        return aliases.get(
            word.strip().lower()
        )

    # ===================================
    # LOCAL DA ENTRADA
    # ===================================

    def _extract_fabric_location(self, text):

        patterns = [

            r"\bna\s+(depósito|deposito|casa|empresa|costureira|costureiras)\b",

            r"\bno\s+(depósito|deposito|casa|empresa|costureira|costureiras)\b",

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

            normalized = (
                self._normalize_location(
                    match.group(1)
                )
            )

            if normalized:
                return normalized

        return None

    def _extract_order_fabric(self, text):

        patterns = [

            # Exemplo:
            # na malha PP branca para ser entregue
            r"\b(?:na|em)\s+malha\s+(.+?)(?=\s+(?:para|pra)\s+ser\s+entregue\b|[,.]|$)",

            # Exemplo:
            # malha PP branca para entrega
            r"\bmalha\s+(.+?)(?=\s+(?:para|pra)\s+(?:entrega|ser\s+entregue)\b|[,.]|$)",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                fabric = (
                    match.group(1)
                    .strip()
                    .strip(".,")
                )

                if fabric:
                    return fabric.upper()

        return None