import customtkinter as ctk

from app.ui.screens.security_screen import SecurityScreen


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Teste Security Screen")
        self.geometry("1200x700")

        screen = SecurityScreen(self)
        screen.pack(fill="both", expand=True)


app = App()
app.mainloop()