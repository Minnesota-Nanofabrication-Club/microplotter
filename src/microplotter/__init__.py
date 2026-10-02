"""microplotter — Qt desktop application."""

from microplotter.app import run

__all__ = ["main", "run"]


def main() -> None:
    """Console-script entry point (see [project.scripts] in pyproject.toml)."""
    raise SystemExit(run())
