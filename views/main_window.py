from PyQt6.QtWidgets import (
    QMainWindow,
    QSplitter,
    QToolBar,
    QToolButton,
    QMenu,
    QFileDialog,
    QMessageBox
)

from PyQt6.QtGui import QAction

from PyQt6.QtCore import Qt

from views.editor_panel import EditorPanel
from views.results_panel import ResultsPanel


class MainWindow(QMainWindow):

    # =====================================================
    # INIT
    # =====================================================

    def __init__(self):

        super().__init__()

        # archivo actualmente abierto
        self.current_file = None

        self._setup_ui()

    # =====================================================
    # UI
    # =====================================================

    def _setup_ui(self):

        self.setWindowTitle(
            "EduLang Studio"
        )

        self.resize(1200, 700)

        self._crear_acciones()

        self._crear_toolbar()

        self._crear_central()

        self.statusBar().showMessage( # type: ignore
            "Listo"
        ) # type: ignore

    # =====================================================
    # ACCIONES
    # =====================================================

    def _crear_acciones(self):

        # =================================================
        # COMPILAR
        # =================================================

        self.action_analizar = QAction(
            "▶ Compilar",
            self
        )

        self.action_analizar.setShortcut(
            "F1"
        )

        # =================================================
        # ABRIR
        # =================================================

        self.action_abrir = QAction(
            "📂 Abrir",
            self
        )

        self.action_abrir.setShortcut(
            "Ctrl+O"
        )

        self.action_abrir.triggered.connect(
            self.abrir_archivo
        )

        # =================================================
        # GUARDAR
        # =================================================

        self.action_guardar = QAction(
            "💾 Guardar",
            self
        )

        self.action_guardar.setShortcut(
            "Ctrl+S"
        )

        self.action_guardar.triggered.connect(
            self.guardar_archivo
        )

        # =================================================
        # LIMPIAR
        # =================================================

        self.action_limpiar = QAction(
            "🧹 Limpiar",
            self
        )

        self.action_limpiar.setShortcut(
            "Ctrl+L"
        )

        self.action_limpiar.triggered.connect(
            self.limpiar_editor
        )

        # =================================================
        # EXPORTAR
        # =================================================

        self.action_exportar_python = QAction(
            "🐍 Exportar Python",
            self
        )

        self.action_exportar_javascript = QAction(
            "🟨 Exportar JavaScript",
            self
        )

        self.action_exportar_csharp = QAction(
            "🔷 Exportar C#",
            self
        )

        # =================================================
        # IMPORTAR
        # =================================================

        # IMPORTAR QUEDA PENDIENTE
        # SOLO PREPARANDO UI

        self.action_importar_python = QAction(
            "🐍 Importar Python",
            self
        )

        self.action_importar_javascript = QAction(
            "🟨 Importar JavaScript",
            self
        )

        self.action_importar_csharp = QAction(
            "🔷 Importar C#",
            self
        )

    # =====================================================
    # TOOLBAR
    # =====================================================

    def _crear_toolbar(self):

        bar = QToolBar()

        self.addToolBar(bar)

        # =================================================
        # ABRIR
        # =================================================

        bar.addAction(
            self.action_abrir
        )

        # =================================================
        # GUARDAR
        # =================================================

        bar.addAction(
            self.action_guardar
        )

        bar.addSeparator()

        # =================================================
        # COMPILAR
        # =================================================

        bar.addAction(
            self.action_analizar
        )

        bar.addSeparator()

        # =================================================
        # EXPORTAR
        # =================================================

        exportar_menu = QMenu()

        exportar_menu.addAction(
            self.action_exportar_python
        )

        exportar_menu.addAction(
            self.action_exportar_javascript
        )

        exportar_menu.addAction(
            self.action_exportar_csharp
        )

        exportar_button = QToolButton()

        exportar_button.setText(
            "📤 Exportar"
        )

        exportar_button.setPopupMode(
            QToolButton.ToolButtonPopupMode.InstantPopup
        )

        exportar_button.setMenu(
            exportar_menu
        )

        bar.addWidget(
            exportar_button
        )

        # =================================================
        # IMPORTAR
        # =================================================

        importar_menu = QMenu()

        importar_menu.addAction(
            self.action_importar_python
        )

        importar_menu.addAction(
            self.action_importar_javascript
        )

        importar_menu.addAction(
            self.action_importar_csharp
        )

        importar_button = QToolButton()

        importar_button.setText(
            "📥 Importar"
        )

        importar_button.setPopupMode(
            QToolButton.ToolButtonPopupMode.InstantPopup
        )

        importar_button.setMenu(
            importar_menu
        )

        bar.addWidget(
            importar_button
        )

        bar.addSeparator()

        # =================================================
        # LIMPIAR
        # =================================================

        bar.addAction(
            self.action_limpiar
        )

    # =====================================================
    # CENTRAL
    # =====================================================

    def _crear_central(self):

        splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        self.editor_panel = EditorPanel()

        self.results_panel = ResultsPanel()

        splitter.addWidget(
            self.editor_panel
        )

        splitter.addWidget(
            self.results_panel
        )

        splitter.setSizes([600, 600])

        self.setCentralWidget(splitter)

    # =====================================================
    # ABRIR ARCHIVO
    # =====================================================

    def abrir_archivo(self):

        # =================================================
        # SOLO TXT
        # =================================================

        ruta, _ = QFileDialog.getOpenFileName(

            self,

            "Abrir archivo EduLang",

            "",

            "Archivos de texto (*.txt)"
        )

        # =================================================
        # CANCELADO
        # =================================================

        if not ruta:
            return

        try:

            # =============================================
            # LEER ARCHIVO
            # =============================================

            with open(
                ruta,
                "r",
                encoding="utf-8"
            ) as f:

                contenido = f.read()

            # =============================================
            # CARGAR SOLO EN EL EDITOR
            # =============================================

            self.editor_panel.editor.setPlainText(
                contenido
            )

            # =============================================
            # GUARDAR REFERENCIA
            # =============================================

            self.current_file = ruta

            # =============================================
            # CAMBIAR TÍTULO
            # =============================================

            nombre_archivo = (
                ruta.split("/")[-1]
            )

            self.setWindowTitle(
                f"EduLang Studio - {nombre_archivo}"
            )

            # =============================================
            # STATUS
            # =============================================

            self.statusBar().showMessage( # type: ignore
                (
                    "Archivo cargado correctamente"
                )
            ) # type: ignore

            # =============================================
            # IMPORTANTE
            # =============================================

            # NO COMPILAR AUTOMÁTICAMENTE
            # SOLO ABRIR EL ARCHIVO

        except Exception as e:

            QMessageBox.critical(

                self,

                "Error",

                (
                    "No se pudo abrir el archivo.\n\n"
                    f"{str(e)}"
                )
            )

    # =====================================================
    # GUARDAR ARCHIVO
    # =====================================================

    def guardar_archivo(self):

        try:

            # =============================================
            # CONTENIDO DEL EDITOR
            # =============================================

            contenido = (
                self.editor_panel.editor
                .toPlainText()
            )

            # =============================================
            # PEDIR NOMBRE/RUTA SI ES NUEVO
            # =============================================

            ruta, _ = QFileDialog.getSaveFileName(

                self,

                "Guardar archivo EduLang",

                "",

                "Archivos de texto (*.txt)"
            )

            # =============================================
            # CANCELADO
            # =============================================

            if not ruta:
                return

            # =============================================
            # AGREGAR .txt SI FALTA
            # =============================================

            if not ruta.endswith(".txt"):

                ruta += ".txt"

            # =============================================
            # GUARDAR
            # =============================================

            with open(
                ruta,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(contenido)

            # =============================================
            # ACTUALIZAR REFERENCIA
            # =============================================

            self.current_file = ruta

            # =============================================
            # ACTUALIZAR TÍTULO
            # =============================================

            nombre_archivo = (
                ruta.split("/")[-1]
            )

            self.setWindowTitle(
                f"EduLang Studio - {nombre_archivo}"
            )

            # =============================================
            # STATUS
            # =============================================

            self.statusBar().showMessage( # type: ignore
                (
                    "Archivo guardado correctamente"
                )
            ) # type: ignore

        except Exception as e:

            QMessageBox.critical(

                self,

                "Error",

                (
                    "No se pudo guardar el archivo.\n\n"
                    f"{str(e)}"
                )
            )

    # =====================================================
    # LIMPIAR EDITOR
    # =====================================================

    def limpiar_editor(self):

        self.editor_panel.editor.clear()

        self.statusBar().showMessage( # type: ignore
            "Editor limpiado"
        ) 