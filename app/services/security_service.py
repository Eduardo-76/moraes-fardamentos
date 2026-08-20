class SecurityService:
    """
    Responsável pelas validações de segurança do sistema.
    """

    DELETE_PASSWORD = "123"

    def validate_delete_password(
        self,
        password: str
    ) -> bool:
        """
        Valida a senha para exclusão de pedidos.
        """

        return password == self.DELETE_PASSWORD