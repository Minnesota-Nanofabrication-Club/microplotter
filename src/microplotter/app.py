"""QApplication construction and the program entry point."""

from __future__ import annotations

import signal
import sys
from collections.abc import Sequence

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from microplotter import config
from microplotter.ui.main_window import MainWindow


def create_app(argv: Sequence[str] | None = None) -> QApplication:
    """Build the QApplication with the identity QSettings and dialogs rely on."""
    app = QApplication(list(argv if argv is not None else sys.argv))
    app.setOrganizationName(config.ORG_NAME)
    app.setOrganizationDomain(config.ORG_DOMAIN)
    app.setApplicationName(config.APP_NAME)
    app.setApplicationDisplayName(config.APP_DISPLAY_NAME)
    app.setApplicationVersion(config.app_version())
    app.setStyleSheet(_load_stylesheet())
    return app


def _load_stylesheet() -> str:
    from importlib.resources import files

    qss = files("microplotter.resources").joinpath("style.qss")
    return qss.read_text(encoding="utf-8") if qss.is_file() else ""


def _install_sigint_handler(app: QApplication) -> None:
    """Let Ctrl+C in the launching terminal quit the GUI."""
    signal.signal(signal.SIGINT, lambda *_: app.quit())
    # Qt's event loop blocks Python signal delivery; a periodic no-op timer
    # hands control back to the interpreter often enough to notice SIGINT.
    timer = QTimer(app)
    timer.timeout.connect(lambda: None)
    timer.start(200)


def run(argv: Sequence[str] | None = None) -> int:
    app = create_app(argv)
    _install_sigint_handler(app)

    window = MainWindow()
    window.show()

    return app.exec()
