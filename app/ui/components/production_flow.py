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

        self.content.grid_columnconfigure(
            0,
            weight=1
        )

        stages = ORDER_STAGES

        for index in range(len(stages)):
            self.content.grid_columnconfigure(
                index,
                weight=1
            )       

        for index, stage in enumerate(stages):
            "Entrega"

        for index in range(len(stages)):
            self.content.grid_columnconfigure(
                index,
                weight=1
            )       

        for index, stage in enumerate(stages):

            state = self._get_stage_state(stage)

            if state == "done":
                prefix = "✓"

            elif state == "current":
                prefix = "▶"

            else:
                prefix = "○"

            label = ctk.CTkLabel(
                self.content,
                text=f"{prefix} {stage}",
                font=ctk.CTkFont(
                    size=15,
                    weight="bold"
                )
            )

            label.grid(
                row=0,
                column=index,
                padx=15,
                pady=15
            )        