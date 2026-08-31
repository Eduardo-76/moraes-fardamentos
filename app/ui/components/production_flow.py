import customtkinter as ctk

from app.core.constants import ORDER_STAGES


class ProductionFlow(ctk.CTkFrame):

    def __init__(
        self,
        master,
        order
    ):
        super().__init__(master)

        self.order = order

        self._build()

    def _get_stage_state(self, stage):

        current = self.order.current_stage or "Recepção"

        current_index = ORDER_STAGES.index(current)
        stage_index = ORDER_STAGES.index(stage)

        if stage_index < current_index:
            return "done"

        if stage_index == current_index:
            return "current"

        return "pending"

    def _build(self):

        self.grid_columnconfigure(
            0,
            weight=1
        )

        # =====================================================
        # TÍTULO
        # =====================================================

        title = ctk.CTkLabel(
            self,
            text="Fluxo de Produção",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=8,
            pady=(10, 15)
        )

        # =====================================================
        # ÁREA DO FLUXO
        # =====================================================

        self.content = ctk.CTkFrame(
            self
        )

        self.content.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=8,
            pady=(0, 10)
        )

        # Quatro colunas.
        # Os estágios serão distribuídos em duas linhas.
        for column in range(4):
            self.content.grid_columnconfigure(
                column,
                weight=1
            )

        # =====================================================
        # ESTÁGIOS
        # =====================================================

        for index, stage in enumerate(ORDER_STAGES):

            state = self._get_stage_state(stage)

            if state == "done":
                prefix = "✓"

            elif state == "current":
                prefix = "▶"

            else:
                prefix = "○"

            row = index // 4
            column = index % 4

            label = ctk.CTkLabel(
                self.content,
                text=f"{prefix} {stage}",
                font=ctk.CTkFont(
                    size=15,
                    weight="bold"
                ),
                wraplength=160,
                justify="center"
            )

            label.grid(
                row=row,
                column=column,
                padx=6,
                pady=10,
                sticky="ew"
            )