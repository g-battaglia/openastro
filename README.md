# OpenAstro (legacy)

OpenAstro is a legacy open‑source astrology application. This repo contains a lightly adapted version that can be run on modern macOS and Linux systems.

Highlights

-   GUI built with GTK 3 via PyGObject
-   Swiss Ephemeris data bundled under `data/swisseph/`
-   Data and temporary files stored under `data/home/`

## Run program

Once dependencies are installed (see below), run:

```bash
uv run python main.py
```

## Quick start (macOS, using uv)

This project is configured with `pyproject.toml` and `uv.lock`. We recommend using [uv](https://docs.astral.sh/uv/) to create the environment and run the app.

1. Install system libraries with Homebrew

    - Install Homebrew first: https://brew.sh
    - Install required libraries:
        ```bash
        brew install gtk+3 pygobject3 librsvg
        ```
        What these provide:
    - gtk+3: GTK3 graphical libraries (with Quartz backend on macOS)
    - pygobject3: GObject introspection runtime used by Python bindings
    - librsvg: SVG rendering library, provides the `Rsvg-2.0` GI typelib

2. Ensure you have uv installed (one‑time)

    - See official install options at https://docs.astral.sh/uv/getting-started/installation/
    - Example (optional): `curl -Ls https://astral.sh/uv/install.sh | sh`

3. Sync and install Python dependencies
   In the repo root (`openastro/`):

    ```bash
    uv sync
    ```

    This will create a virtual environment and install `PyGObject`, `pyswisseph`, and `pytz` from `pyproject.toml`.

4. Run OpenAstro
    ```bash
    uv run python main.py
    ```
    A GTK3 window should appear. On first run, OpenAstro initializes SQLite databases under `data/home/` and creates temporary SVGs under `data/home/tmp/`.

## Python GTK3 on macOS with uv — Complete Setup

This is a text‑only guide to install and use GTK3 and PyGObject in Python on macOS using uv, including librsvg support (used by OpenAstro to render SVG charts).

1. Install system dependencies with Homebrew
   Make sure Homebrew is installed first (https://brew.sh).
   Then install the required libraries:

    ```bash
    brew install gtk+3 pygobject3 librsvg
    ```

    Provides:

    - gtk+3: GTK3 graphical libraries
    - pygobject3: Python GObject Introspection runtime/bindings
    - librsvg: SVG rendering library with Introspection (Rsvg-2.0)

2. Use an existing uv project (this repo) or create a new one

    - For this repo, just use it in place (no init needed).
    - If experimenting elsewhere: `uv init gtk3-test && cd gtk3-test`

3. Add PyGObject to your uv environment
   Even though Homebrew supplies the native libs, add the Python package too. In this repo it’s already declared in `pyproject.toml`, so simply:

    ```bash
    uv sync
    ```

    If you’re in a scratch project: `uv add PyGObject`

4. Verify that the Rsvg typelib is present
   Check that the Introspection file exists:

    ```bash
    ls "$(brew --prefix)"/lib/girepository-1.0 | grep Rsvg
    ```

    Expected output:

    ```
    Rsvg-2.0.typelib
    ```

5. Test GTK3
   Run a Python REPL inside uv:

    ```bash
    uv run python
    ```

    Then enter:

    ```python
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk

    win = Gtk.Window(title="Hello from GTK3!")
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
    ```

    A window should appear.

6. Test librsvg
   Still inside the same Python REPL (or a new one via `uv run python`):
    ```python
    import gi
    gi.require_version("Rsvg", "2.0")
    from gi.repository import Rsvg
    print("Rsvg loaded:", Rsvg)
    ```
    If it prints something like `<gi.repository.Rsvg>`, the binding is working.

## Linux notes (Debian/Ubuntu‑like)

System packages (example):

```bash
sudo apt update
sudo apt install -y python3-gi gir1.2-gtk-3.0 gir1.2-rsvg-2.0 libgtk-3-0 librsvg2-2 gobject-introspection libgirepository1.0-dev
```

Then install Python deps via uv (recommended) or pip:

```bash
uv sync
# or
pip install -r requirements.txt  # if you create one, otherwise use pyproject via uv
```

Run:

```bash
uv run python main.py
```

## Data, files, and where things go

-   Swiss Ephemeris files live in `data/swisseph/` and are used at runtime. The code points to this directory automatically.
-   App data lives under `data/home/`:
    -   `astrodb.sql`, `peopledb.sql` are created/updated at first run
    -   `tmp/` holds generated SVG charts, like:
    -   `data/home/tmp/openAstroChart.svg`
    -   `data/home/tmp/openAstroChartTable.svg`
-   Additional bundled data:
    -   `data/famous.sql` (example famous people dataset)
    -   `data/geonames.sql` (geographical data)

## Useful command‑line options

These affect database initialization/maintenance:

-   `--dbcheck` Enable database schema checks and default inserts
-   `--purge` Recreate certain default values (INSERT OR REPLACE)

Example:

```bash
uv run python main.py --dbcheck
```

## Troubleshooting

-   Error: `ValueError: Namespace Rsvg not available`
    Fixes:

    -   Ensure you ran: `brew install librsvg`
    -   Confirm `Rsvg-2.0.typelib` exists in:

    ```
    $(brew --prefix)/lib/girepository-1.0/
    ```

    -   Optional: set environment vars if discovery fails in your shell session:

    ```bash
    export GI_TYPELIB_PATH="$(brew --prefix)/lib/girepository-1.0:${GI_TYPELIB_PATH}"
    export DYLD_LIBRARY_PATH="$(brew --prefix)/lib:${DYLD_LIBRARY_PATH}"
    ```

-   GTK window does not appear (macOS)
    Checks:

    -   Run from a normal desktop session (not headless/SSH without GUI).
    -   No XQuartz is required for GTK3 on macOS; the Quartz backend is used.

-   Import errors for `gi`
    -   Make sure `uv sync` completed successfully (installs `PyGObject`).
    -   Ensure Homebrew `pygobject3` and `gobject-introspection` bits are installed and on default paths.

## Development notes

-   Python version: the `pyproject.toml` targets Python `>= 3.11`. uv will select/download an appropriate interpreter as needed.
-   Entry point: run `main.py`.
-   GUI stack: GTK 3 + PyGObject; SVG rendering via `librsvg`/`Rsvg` GI namespace.

## License

OpenAstro is licensed under the AGPLv3 (see headers in source files). This fork includes minor changes only to aid running on current systems.

## Copyright

The original creator of OpenAstro is Pelle van der Scheer, great thanks for releasing this historically foundational software as open source. It contributed greatly to my learning of both astrology and programming, in generale to the open source ecosystem and the development of Astrology as a science and practice.
