# Copilot instructions for this repo

> Goal: make AI agents productive quickly by documenting how this Flask app is structured and operated.

## Big picture
- Flask app serving a slide-based learning experience with simple auth and per-user progress.
- Routing in `routes/main.py` (pages) and `routes/auth.py` (auth + persistence helpers). `app.py` wires functions via `app.route()`.
- Views: Jinja templates in `templates/` with layout `templates/base.html`. Slides are individual files in `templates/slides/slideN.html`.
- Static behavior: `static/js/presentation.js` (keyboard, swipe, animations, TTS helper); styles in `static/css/presentation.css`.
- Persistence is hybrid: Users in MySQL (PyMySQL); learning progress in JSON (`data/user_progress.json`).

## Dev workflow
- Python 3.12 (see `runtime.txt`). Install deps (`requirements.txt`) and run `python app.py`. Listens on `PORT` or 8325.
- Env vars: `SECRET_KEY` (override default in `app.py`), `DATABASE_URL` (mysql://user:pass@host:port/db?requireSSL=true).
- Deploy: `Procfile` uses `web: gunicorn app:app` (Heroku/Render-compatible). Ensure write perms for `data/`.

## Key patterns and contracts
- Route names are relied upon by `url_for` and `app.route` registration (e.g., `slide`, `lessons`). Keep names stable.
- Slide flow: `main.slide(slide_number)` validates range, computes prev/next, updates progress when logged in, and renders `slides/slide{n}.html` inside `base.html`.
- Template contract for slides: extend `base.html` and fill `{% block content %}`. `base.html` expects `current_slide`, `prev_slide`, `next_slide` to render nav and progress bar. IDs `prev-btn` and `next-btn` are used by JS.
- Session: `session['user']` stores the lowercase username across routes.
- Auth: `login/register/logout` in `routes/main.py` call DB helpers in `routes/auth.py`. Passwords use SHA-256 comparison. Flash categories: `success|error|info`.
- DB: `routes/auth.get_db_connection()` parses `DATABASE_URL`; TLS is enabled when `useSSL`/`requireSSL` query params are true (uses `certifi`). `ensure_users_table()` creates table on demand.
- Progress JSON helpers: `load_user_progress`, `save_user_progress`, `update_user_progress`, `get_user_data`.

## Common changes (do it this way)
- Add slide N:
  1) Create `templates/slides/slideN.html` with `{% extends 'base.html' %}` and `{% block content %}`.
  2) Update slide range and prev/next in `routes/main.py`.
  3) Update total slide count/progress denominator in `templates/base.html` and End-key target in `static/js/presentation.js` if needed.
  4) (If listed) add to `lessons()` items in `routes/main.py`.
- Persist new interactions: call `update_user_progress(session['user'], slide_number)` after success.
- Add user fields: update SQL in `ensure_users_table` and adjust queries in `get_user_by_username`/`create_user`.

## Gotchas
- Slide count mismatch: code enforces 8 slides; repo has up to 10 and JS maps End→`/slide/10`. Align all places together when changing.
- Secrets: don’t commit real creds. Prefer env `SECRET_KEY` and `DATABASE_URL`. Replace the hardcoded secret in `app.py` for production.
- File writes: `data/` must be writable in deploy targets.
- Error surface: DB helpers raise `RuntimeError`; routes catch and flash user-friendly messages—preserve this pattern.

## Files to know
- Python: `app.py`, `routes/main.py`, `routes/auth.py`
- Templates: `templates/base.html`, `templates/*`, `templates/slides/slide*.html`
- Static: `static/js/presentation.js`, `static/css/presentation.css`
- Ops: `requirements.txt`, `Procfile`, `runtime.txt`, `data/user_progress.json`
