"""Background work.

Qt widgets may only be touched from the GUI thread, so long-running work
(serial I/O, file parsing, motion planning) belongs in a QObject that is moved
onto a QThread and reports back exclusively through signals.
"""

from __future__ import annotations

from PySide6.QtCore import QObject, Signal, Slot


class Worker(QObject):
    """Template worker: counts to `steps`, emitting progress as it goes."""

    progress = Signal(int)          # 0..100
    message = Signal(str)
    finished = Signal()
    failed = Signal(str)

    def __init__(self, steps: int = 100, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._steps = steps
        self._cancelled = False

    @Slot()
    def cancel(self) -> None:
        """Thread-safe enough for a plain flag; call via a queued connection."""
        self._cancelled = True

    @Slot()
    def run(self) -> None:
        try:
            for i in range(1, self._steps + 1):
                if self._cancelled:
                    self.message.emit("Cancelled")
                    break
                # Replace with real work. Never call time.sleep in production
                # code that must stay responsive to cancellation requests;
                # poll the device or use QThread.msleep in small slices.
                self.progress.emit(round(i / self._steps * 100))
            else:
                self.message.emit("Done")
        except Exception as exc:  # surfaced in the GUI rather than lost
            self.failed.emit(str(exc))
        finally:
            self.finished.emit()
