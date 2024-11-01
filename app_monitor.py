from src.config import Config
from src.db_manager import DatabaseManager
from src.terminalGui import TerminalGui
import monitor # monitoramento com prometheus + grafana


class App:
    def __init__(self):
        self.config = Config()
        self.db = DatabaseManager(self.config.db_path)
        self.gui = TerminalGui(self.db)

    def run(self):
        self.gui.clear_terminal()
        print('Bem vindo ao UserHub! Digite --help para menu de ações do app.')

        # Mostrar mensagem inicial e desabilita no primeiro uso do app
        if self.config.show_startup_message:
            self.gui._menu()
            self.config.show_startup_message = False

        # rodar a aplicacao
        while True:
            try:
                self.gui.run()
            except KeyboardInterrupt:
                print("\nSaindo do UserHub...")
                return


if __name__ == "__main__":
    app = App()
    app.run()
