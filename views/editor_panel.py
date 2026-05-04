from PyQt6.QtWidgets import (
    QTextEdit, QWidget, QVBoxLayout, QLabel,
    QPlainTextEdit
)
from PyQt6.QtGui import (
    QColor, QPainter, QTextCharFormat,
    QSyntaxHighlighter, QFont, QTextFormat,QTextCursor, QKeyEvent
)
from PyQt6.QtCore import QRect, QSize, Qt, QRegularExpression


# ---------- RESALTADOR ----------
class SyntaxHighlighter(QSyntaxHighlighter):

    def __init__(self, document):
        super().__init__(document)

        self.rules = []

        # ===== PALABRAS RESERVADAS =====
        formato_kw = QTextCharFormat()
        formato_kw.setForeground(QColor("#1F3A5F"))
        formato_kw.setFontWeight(QFont.Weight.Bold)

        palabras = [
            "si",
            "sino",
            "mientras",
            "escribir",
            "cuando",
            "ejecutar",
            "funcion",
            "retornar",
            "para",
            "en",
            "rango",
            "npc",
            "hablar",
            "mover",
            "patrullar",
            "atacar",
            "vida",
            "animar",
            "esperar",
            "ruta",
        ]

        for palabra in palabras:
            self.rules.append(
                (QRegularExpression(rf"\b{palabra}\b"), formato_kw)
            )

        # ===== NÚMEROS =====
        formato_num = QTextCharFormat()
        formato_num.setForeground(QColor("#B58900"))

        self.rules.append(
            (QRegularExpression(r"\b\d+\b"), formato_num)
        )

        # ===== STRINGS =====
        formato_str = QTextCharFormat()
        formato_str.setForeground(QColor("#3A7D44"))

        self.rules.append(
            (QRegularExpression(r'"[^"]*"|\'[^\']*\''), formato_str)
        )

        # ===== OPERADORES =====
        formato_op = QTextCharFormat()
        formato_op.setForeground(QColor("#444444"))

        self.rules.append(
            (
                QRegularExpression(r"(==|!=|<=|>=|=|<|>|\+|\-|\*|/)"),
                formato_op
            )
        )

        # ===== FUNCIONES =====
        formato_func = QTextCharFormat()
        formato_func.setForeground(QColor("#2C5AA0"))

        self.rules.append(
            (
                QRegularExpression(r"\b[a-zA-Z_][a-zA-Z0-9_]*(?=\()"),
                formato_func
            )
        )

        # ===== COMENTARIOS =====
        formato_comment = QTextCharFormat()
        formato_comment.setForeground(QColor("#888888"))

        self.rules.append(
            (QRegularExpression(r"#.*"), formato_comment)
        )

    def highlightBlock(self, text):

        self.setFormat(0, len(text), QTextCharFormat())  # 🔥 reset

        for patron, formato in self.rules:
            it = patron.globalMatch(text)

            while it.hasNext():
                m = it.next()
                self.setFormat(
                    m.capturedStart(),
                    m.capturedLength(),
                    formato
                )


# ---------- LINE NUMBER AREA ----------
class LineNumberArea(QWidget):

    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.setStyleSheet("background-color: #F5E6CC; border: none;")

    def sizeHint(self):
        return QSize(
            self.editor.lineNumberAreaWidth(),
            0
        )

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)

# ---------- EDITOR ----------
class CodeEditor(QPlainTextEdit):

    def __init__(self):
        super().__init__()
        self.setFrameStyle(0)

        self.setFont(QFont("Consolas", 12))
        self.setTabStopDistance(40)
        self.setLineWrapMode(
            QPlainTextEdit.LineWrapMode.NoWrap
        )

        self.highlighter = SyntaxHighlighter(
            self.document()
        )

        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(
            self.updateLineNumberAreaWidth
        )

        self.updateRequest.connect(
            self.updateLineNumberArea
        )

        self.cursorPositionChanged.connect(
            self.highlightCurrentLine
        )

        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

    def lineNumberAreaWidth(self):
        digits = len(str(max(1, self.blockCount())))
        return 15 + self.fontMetrics().horizontalAdvance("9") * digits

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(
            self.lineNumberAreaWidth(), 0, 0, 0
        )

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(
                0, rect.y(),
                self.lineNumberArea.width(),
                rect.height()
            )

    def resizeEvent(self, event):
        super().resizeEvent(event)

        cr = self.contentsRect()

        self.lineNumberArea.setGeometry(
            QRect(
                cr.left(),
                cr.top(),
                self.lineNumberAreaWidth(),
                cr.height()
            )
        )

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor("#F5E6CC"))  # fondo beige
        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = round(
            self.blockBoundingGeometry(block)
            .translated(self.contentOffset())
            .top()
        )

        bottom = top + round(
            self.blockBoundingRect(block).height()
        )

        while block.isValid() and top <= event.rect().bottom():

            if block.isVisible():
                number = str(blockNumber + 1)

                painter.setPen(QColor("#1F3A5F"))     

                painter.drawText(
                    0, top,
                    self.lineNumberArea.width() - 5,
                    self.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight,
                    number
                )

            block = block.next()
            top = bottom
            bottom = top + round(
                self.blockBoundingRect(block).height()
            )
            blockNumber += 1

    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            color = QColor("#E6F0FF")  # azul claro

            selection.format.setBackground(color)
            selection.format.setProperty(
                QTextFormat.Property.FullWidthSelection,
                True
            )

            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()

            extraSelections.append(selection)

        self.setExtraSelections(extraSelections)

    def keyPressEvent(self, event):

        # TAB manual
        if event.key() == Qt.Key.Key_Tab:
            self.insertPlainText("    ")
            return

        # ENTER inteligente
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):

            cursor = self.textCursor()
            linea = cursor.block().text()

            # contar espacios actuales
            espacios = len(linea) - len(linea.lstrip(" "))
            indent = " " * espacios

            # detectar :
            if linea.rstrip().endswith(":"):
                indent += "    "

            # ejecutar salto de línea
            super().keyPressEvent(event)

            # insertar indentación
            self.insertPlainText(indent)

            return

        # resto normal
        super().keyPressEvent(event)

# ---------- PANEL ----------
class EditorPanel(QWidget):

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        titulo = QLabel("Editor de Código")

        self.editor = CodeEditor()

        self.editor.setPlaceholderText(
            "\nx = 10\n"
            "si x == 10:\n"
            "    escribir(x)"
        )

        layout.addWidget(titulo)
        layout.addWidget(self.editor)

    def get_code(self):
        return self.editor.toPlainText()

    def clear(self):
        self.editor.clear()

    def set_code(self, texto):
        self.editor.setPlainText(texto)