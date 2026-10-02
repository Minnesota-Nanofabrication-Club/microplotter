# microplotter

Qt (PySide6) desktop application.

## Run

```sh
uv run microplotter      # console script
uv run python -m microplotter
```

## Layout

| Path | Purpose |
| --- | --- |
| `src/microplotter/__init__.py` | `main()` console-script entry point |
| `src/microplotter/app.py` | `QApplication` setup, stylesheet, `run()` |
| `src/microplotter/config.py` | app identity constants, `QSettings` accessor |
| `src/microplotter/ui/main_window.py` | `QMainWindow`: menus, toolbar, status bar, log dock, geometry persistence |
| `src/microplotter/ui/central.py` | central widget — replace the placeholder with the real UI |
| `src/microplotter/workers.py` | `QThread` worker pattern for background/serial work |
| `src/microplotter/resources/style.qss` | application stylesheet |
