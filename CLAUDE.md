# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

"Spendly" is a Flask-based expense tracker built incrementally as a step-by-step learning project. Many routes and modules are intentionally left as placeholders (with comments like "coming in Step N" or "Students will write this file in Step 1") to be implemented progressively — don't be surprised by stubbed-out functionality, and don't "complete" placeholders unless asked to.

## Commands

- Run the app: `python app.py` (serves on `http://127.0.0.1:5001` with debug mode enabled)
- Install dependencies: `pip install -r requirements.txt`
- Run tests: `pytest`
- Activate the virtualenv (already present at `venv/`): `source venv/bin/activate`

## Architecture

- **`app.py`** — Single Flask app with all routes. Currently includes:
  - Implemented page routes: `/` (landing), `/register`, `/login`, `/terms`, `/privacy` — these just render templates with no form handling logic yet.
  - Placeholder routes returning plain strings: `/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`. These map to the project's step-based curriculum (auth, profile, CRUD for expenses).
- **`database/db.py`** — Placeholder for the database layer. Per its header comment, it should eventually expose:
  - `get_db()` — SQLite connection with `row_factory` and foreign keys enabled
  - `init_db()` — creates tables via `CREATE TABLE IF NOT EXISTS`
  - `seed_db()` — inserts sample dev data
  - The DB file (`expense_tracker.db`) is gitignored and created locally.
- **`templates/`** — Jinja2 templates, all extending `templates/base.html` (shared nav/footer, loads `static/css/style.css` and `static/js/main.js`).
  - `landing.html` uses its own additional stylesheet, `static/css/landing.css`.
  - `login.html` / `register.html` post to `/login` and `/register` respectively but the backend doesn't yet process form submissions or handle `error` template variables beyond rendering them if present.
- **`static/`** — `css/style.css` (shared/global styles), `css/landing.css` (landing page only), `js/main.js` (currently empty/minimal).
