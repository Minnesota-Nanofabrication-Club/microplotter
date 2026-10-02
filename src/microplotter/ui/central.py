"""Central widget: replace the placeholder with the real application UI."""

from __future__ import annotations

from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from microplotter.workers import Worker


class CentralWidget(QWidget):
    status_message = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._thread: QThread | None = None
        self._worker: Worker | None = None

        self._heading = QLabel("Microplotter")
        self._heading.setObjectName("heading")

        self._progress = QProgressBar()
        self._progress.setRange(0, 100)

        self._start_button = QPushButton("Start task")
        self._start_button.clicked.connect(self.start_task)

        self._cancel_button = QPushButton("Cancel", enabled=False)
        self._cancel_button.clicked.connect(self.cancel_task)

        buttons = QHBoxLayout()
        buttons.addWidget(self._start_button)
        buttons.addWidget(self._cancel_button)
        buttons.addStretch(1)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        layout.addWidget(self._heading)
        layout.addWidget(self._progress)
        layout.addLayout(buttons)
        layout.addStretch(1)

    # ------------------------------------------------------------------ task

    @Slot()
    def start_task(self) -> None:
        if self._thread is not None:
            return

        self._thread = QThread(self)
        self._worker = Worker(steps=200)
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.progress.connect(self._progress.setValue)
        self._worker.message.connect(self.status_message)
        self._worker.failed.connect(lambda msg: self.status_message.emit(f"Error: {msg}"))
        self._worker.finished.connect(self._thread.quit)
        self._thread.finished.connect(self._on_thread_finished)

        self._start_button.setEnabled(False)
        self._cancel_button.setEnabled(True)
        self.status_message.emit("Task started")
        self._thread.start()

    @Slot()
    def cancel_task(self) -> None:
        if self._worker is not None:
            self._worker.cancel()

    @Slot()
    def _on_thread_finished(self) -> None:
        if self._worker is not None:
            self._worker.deleteLater()
            self._worker = None
        if self._thread is not None:
            self._thread.deleteLater()
            self._thread = None
        self._start_button.setEnabled(True)
        self._cancel_button.setEnabled(False)

    def shutdown(self) -> None:
        """Stop background work before the window closes."""
        if self._worker is not None:
            self._worker.cancel()
        if self._thread is not None:
            self._thread.quit()
            self._thread.wait(3000)
