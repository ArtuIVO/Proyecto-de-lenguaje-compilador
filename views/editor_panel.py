from PyQt6.QtWidgets import (
    QTextEdit, QWidget, QVBoxLayout, QLabel,
    QPlainTextEdit
)
from PyQt6.QtGui import (
    QColor, QPainter, QTextCharFormat,
    QSyntaxHighlighter, QFont, QTextFormat
)
from PyQt6.QtCore import QRect, QSize, Qt, QRegularExpression


# ---------- RESALTADOR ----------
class SyntaxHighlighter(QSyntaxHighlighter):

    def __init__(self, document):
        super().__init__(document)

        self.rules = []

        # palabras reservadas
        formato = QTextCharFormat()
        formato.setForeground(QColor("#00ff9c"))
        formato.setFontWeight(QFont.Weight.Bold)

        palabras = [
            "si", "escribir", "cuando", "ejecutar"
        ]

        for palabra in palabras:
            self.rules.append(
                (
                    QRegularExpression(rf"\b{palabra}\b"),
                    formato
                )
            )

        # numeros
        formato_num = QTextCharFormat()
        formato_num.setForeground(QColor("#ffd700"))

        self.rules.append(
            (QRegularExpression(r"\b\d+\b"), formato_num)
        )

        # operadores
        formato_op = QTextCharFormat()
        formato_op.setForeground(QColor("#ff7b72"))

        self.rules.append(
            (
                QRegularExpression(r"(==|!=|<=|>=|=|<|>)"),
                formato_op
            )
        )

    def highlightBlock(self, text):
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
        painter.fillRect(event.rect(), QColor("#111111"))

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

                painter.setPen(QColor("#00ff9c"))

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

            color = QColor("#002b20")

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

        if event.key() == Qt.Key.Key_Tab:
            self.insertPlainText("    ")
            return

        if event.key() == Qt.Key.Key_Return:
            cursor = self.textCursor()
            linea = cursor.block().text()

            espacios = len(linea) - len(linea.lstrip(" "))

            super().keyPressEvent(event)
            self.insertPlainText(" " * espacios)
            return

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