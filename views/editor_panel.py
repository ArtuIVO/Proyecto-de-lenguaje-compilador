from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPlainTextEdit
from PyQt6.QtGui import QTextCursor


class EditorPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        label = QLabel("Editor de Código")

        self.editor = QPlainTextEdit()
        self.editor.setPlaceholderText(
            "Escribe tu código aquí...\nEjemplo:\nsi x == 10:\n    ejecutar y"
        )

        layout.addWidget(label)
        layout.addWidget(self.editor)

    def get_code(self) -> str:
        return self.editor.toPlainText()

    def clear(self):
        self.editor.clear()

    def highlight_position(self, pos):
        cursor = self.editor.textCursor()
        cursor.setPosition(pos)
        self.editor.setTextCursor(cursor)
        self.editor.setFocus()