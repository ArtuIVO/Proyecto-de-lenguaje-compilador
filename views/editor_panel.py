from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPlainTextEdit


class EditorPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        label = QLabel("Editor")
        self.editor = QPlainTextEdit()
        self.editor.setPlaceholderText("Escribe tu código aquí...")

        layout.addWidget(label)
        layout.addWidget(self.editor)

    def get_code(self) -> str:
        return self.editor.toPlainText()

    def clear(self):
        self.editor.clear()