from app.core.database import initialize_database
from app.core.paths import ensure_directories
from app.ui.app_window import AppWindow


def main() -> None:
    ensure_directories()
    initialize_database()

    app = AppWindow()
    app.mainloop()


if __name__ == "__main__":
    main()