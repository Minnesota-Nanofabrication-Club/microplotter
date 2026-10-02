"""The application's main window: menus, toolbar, status bar, central widget."""

from __future__ import annotations

from PySide6.QtCore import QByteArray, Qt, Slot
from PySide6.QtGui import QAction, QCloseEvent, QKeySequence
from PySide6.QtWidgets import (
    QDockWidget,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
)

from microplotter import config
from microplotter.ui.central import CentralWidget


class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(config.APP_DISPLAY_NAME)
        self.resize(1024, 720)

        self._central = CentralWidget(self)
        self.setCentralWidget(self._central)

        self._build_actions()
        self._build_menus()
        self._build_toolbar()
        self._build_statusbar()
        self._build_log_dock()
        self._restore_geometry()

        self._central.status_message.connect(self.show_status)

    # ---------------------------------------------------------------- actions

    def _build_actions(self) -> None:
        self.action_open = QAction("&Open…", self)
        self.action_open.setShortcut(QKeySequence.StandardKey.Open)
        self.action_open.setStatusTip("Open a file")
        self.action_open.triggered.connect(self.open_file)

        self.action_quit = QAction("&Quit", self)
        self.action_quit.setShortcut(QKeySequence.StandardKey.Quit)
        self.action_quit.triggered.connect(self.close)

        self.action_about = QAction("&About", self)
        self.action_about.triggered.connect(self.show_about)

    def _build_menus(self) -> None:
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(self.action_open)
        file_menu.addSeparator()
        file_menu.addAction(self.action_quit)

        view_menu = self.menuBar().addMenu("&View")
        self._view_menu = view_menu  # dock toggles are appended here

        help_menu = self.menuBar().addMenu("&Help")
        help_menu.addAction(self.action_about)

    def _build_toolbar(self) -> None:
        toolbar = self.addToolBar("Main")
        toolbar.setObjectName("main_toolbar")  # required for state save/restore
        toolbar.setMovable(False)
        toolbar.addAction(self.action_open)

    def _build_statusbar(self) -> None:
        self._status_label = QLabel("Ready")
        self.statusBar().addWidget(self._status_label, 1)
        self.statusBar().addPermanentWidget(QLabel(f"v{config.app_version()}"))

    def _build_log_dock(self) -> None:
        self.log = QPlainTextEdit(readOnly=True)
        self.log.setMaximumBlockCount(5000)

        dock = QDockWidget("Log", self)
        dock.setObjectName("log_dock")
        dock.setWidget(self.log)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dock)
        self._view_menu.addAction(dock.toggleViewAction())

    # ----------------------------------------------------------------- slots

    @Slot(str)
    def show_status(self, message: str) -> None:
        self._status_label.setText(message)
        self.log.appendPlainText(message)

    @Slot()
    def open_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "All files (*)")
        if path:
            self.show_status(f"Opened {path}")

    @Slot()
    def show_about(self) -> None:
        QMessageBox.about(
            self,
            f"About {config.APP_DISPLAY_NAME}",
            f"<b>{config.APP_DISPLAY_NAME}</b> {config.app_version()}"
            "<p>Qt (PySide6) application template.</p>",
        )

    # ------------------------------------------------------- window geometry

    def _restore_geometry(self) -> None:
        s = config.settings()
        geometry = s.value("window/geometry", QByteArray())
        state = s.value("window/state", QByteArray())
        if isinstance(geometry, QByteArray) and not geometry.isEmpty():
            self.restoreGeometry(geometry)
        if isinstance(state, QByteArray) and not state.isEmpty():
            self.restoreState(state)

    def closeEvent(self, event: QCloseEvent) -> None:
        s = config.settings()
        s.setValue("window/geometry", self.saveGeometry())
        s.setValue("window/state", self.saveState())
        self._central.shutdown()
        super().closeEvent(event)
