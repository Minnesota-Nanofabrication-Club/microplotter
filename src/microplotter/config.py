"""Application-wide identity and persisted settings."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from PySide6.QtCore import QSettings

ORG_NAME = "nanofabClub"
ORG_DOMAIN = "nanofab.club"
APP_NAME = "microplotter"
APP_DISPLAY_NAME = "Microplotter"


def app_version() -> str:
    try:
        return version(APP_NAME)
    except PackageNotFoundError:  # running from a source tree without an install
        return "0.0.0+dev"


def settings() -> QSettings:
    """QSettings bound to this app; relies on QApplication identity being set."""
    return QSettings()
