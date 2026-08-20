import customtkinter as ctk
from app.ui.components.action_card import ActionCard
from pathlib import Path
from tkinter import filedialog, messagebox
from app.core.system_paths import SystemPaths
from app.services.backup_service import BackupService, BackupError
from app.ui.screens.order_management_screen import OrderManagementScreen
import os


class SecurityScreen(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.backup_service = BackupService()

        self._build_ui()

    def _build_ui(self):

        # =====================================================
        # TÍTULO
        # =====================================================

        title = ctk.CTkLabel(
            self,
            text="🛠 Administração do Sistema",
            font=("Segoe UI", 26, "bold")
        )
        title.pack(pady=(20, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Gerencie backups, restaure dados e execute operações administrativas.",
            text_color="#BDBDBD",
            font=("Segoe UI", 14)
        )
        subtitle.pack(pady=(0, 25))

        # =====================================================
        # ÁREA DOS CARDS
        # =====================================================

        cards_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        cards_frame.pack(expand=True)

        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)

        # =====================================================
        # PRIMEIRA LINHA
        # =====================================================

        backup_card = ActionCard(
            cards_frame,
            icon="💾",
            title="Fazer Backup",
            description="Cria um backup completo do sistema.",
            command=self._backup
        )

        backup_card.grid(
            row=0,
            column=0,
            padx=15,
            pady=15
        )

        restore_card = ActionCard(
            cards_frame,
            icon="📂",
            title="Restaurar Backup",
            description="Recupera um backup salvo anteriormente.",
            command=self._restore
        )

        restore_card.grid(
            row=0,
            column=1,
            padx=15,
            pady=15
        )

        # =====================================================
        # SEGUNDA LINHA
        # =====================================================

        folder_card = ActionCard(
            cards_frame,
            icon="📁",
            title="Abrir Backups",
            description="Abre a pasta onde ficam armazenados os backups.",
            command=self._open_folder
        )

        folder_card.grid(
            row=1,
            column=0,
            padx=15,
            pady=15
        )

        delete_card = ActionCard(
            cards_frame,
            icon="🗑",
            title="Excluir Pedido",
            description="Exclusão protegida por senha.",
            command=self._delete_order
        )

        delete_card.grid(
            row=1,
            column=1,
            padx=15,
            pady=15
        )

        # =====================================================
        # RODAPÉ
        # =====================================================

        footer = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        footer.pack(fill="x", padx=20, pady=20)

        system = ctk.CTkLabel(
            footer,
            text="Sistema: Moraes Fardamentos",
            anchor="w"
        )

        version = ctk.CTkLabel(
            footer,
            text="Versão: 1.0.0",
            anchor="e"
        )

        database = ctk.CTkLabel(
            footer,
            text="Banco: SQLite",
            anchor="w"
        )

        backup = ctk.CTkLabel(
            footer,
            text="Backup: Local",
            anchor="e"
        )

        footer.grid_columnconfigure(0, weight=1)
        footer.grid_columnconfigure(1, weight=1)

        system.grid(row=0, column=0, sticky="w")
        version.grid(row=0, column=1, sticky="e")

        database.grid(row=1, column=0, sticky="w")
        backup.grid(row=1, column=1, sticky="e")

    # ==========================================================
    # CALLBACKS
    # ==========================================================

    def _backup(self):

        try:

            result = self.backup_service.create_backup()

            messagebox.showinfo(
                "Backup concluído",
                (
                    f"Backup criado com sucesso!\n\n"
                    f"Arquivos: {result.total_files}\n"
                    f"Tamanho: {result.total_size:,} bytes\n\n"
                    f"Local:\n{result.backup_path}"
                )
            )

        except BackupError as exc:

            messagebox.showerror(
                "Erro",
                str(exc)
            )

    def _restore(self):

        backup = filedialog.askopenfilename(
            title="Selecionar Backup",
            initialdir=str(SystemPaths.BACKUPS_DIR),
            filetypes=[
                ("Arquivos de Backup", "*.zip")
            ]
        )

        if not backup:
            return

        confirm = messagebox.askyesno(
            "Confirmar restauração",
            (
                "Deseja realmente restaurar este backup?\n\n"
                "Os arquivos atuais do sistema serão substituídos."
            )
        )

        if not confirm:
            return

        try:

            self.backup_service.restore_backup(
                Path(backup)
            )

            messagebox.showinfo(
                "Backup restaurado",
                (
                    "Backup restaurado com sucesso!\n\n"
                    "Reinicie o sistema para garantir que todas as alterações sejam carregadas."
                )
            )

        except BackupError as exc:

            messagebox.showerror(
                "Erro",
                str(exc)
            )

    def _open_folder(self):

        try:

            os.startfile(
                str(SystemPaths.BACKUPS_DIR)
            )

        except Exception as exc:

            messagebox.showerror(
                "Erro",
                f"Não foi possível abrir a pasta de backups.\n\n{exc}"
            )

    def _delete_order(self, card=None):

        self.destroy()

        screen = OrderManagementScreen(self.master)

        screen.pack(
            fill="both",
            expand=True
        )