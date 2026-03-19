from models.lexico_model import LexicoModel


class LexicoController:
    def __init__(self, window):
        self.window = window
        self.lexico = LexicoModel()
        self._connect_signals()

    def _connect_signals(self):
        self.window.action_analizar.triggered.connect(self.analizar)
        self.window.action_limpiar.triggered.connect(self.limpiar)

    def analizar(self):
        codigo = self.window.editor_panel.get_code()

        if not codigo.strip():
            self.window.statusBar().showMessage("El editor está vacío.")
            return

        self.window.statusBar().showMessage("Analizando...")

        tokens, errores = self.lexico.analizar(codigo)

        tokens_vista = [(t.valor, t.tipo, t.linea) for t in tokens]
        self.window.results_panel.load_tokens(tokens_vista)
        self.window.results_panel.load_errors(errores)

        n_err = len(errores)

        if n_err == 0:
            estado = "Todo bien."
        else:
            estado = f"{n_err} error(es) léxico(s)"

        self.window.statusBar().showMessage(
            f"{estado}  |  {len(tokens_vista)} tokens"
        )

    def limpiar(self):
        self.window.editor_panel.clear()
        self.window.results_panel.clear()
        self.window.statusBar().showMessage("Listo.")