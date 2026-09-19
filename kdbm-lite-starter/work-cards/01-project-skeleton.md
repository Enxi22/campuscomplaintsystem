# Work Card 01 — Project Setup & Config

## Goal

Scaffold the Flask project structure, create configuration, requirements, and minimal app.py skeleton.

## Inputs

- `build-blueprint.md` (File and Folder Expectations, Implementation Rules)
- `architecture.md` (Structure Overview, Stack Decision)
- `design.md` (Color palette for CSS variables)

## Files likely touched

- `config.py` — new
- `requirements.txt` — new
- `app.py` — new (skeleton with sections)
- `static/css/style.css` — new (CSS custom properties from design.md)
- `static/js/main.js` — new (empty, ready for later)
- Folder structure: `templates/`, `templates/student/`, `templates/admin/`, `static/uploads/complaints/`, `instance/`

## Instructions for the coding agent

1. Create `config.py` with:
   - `Config` class: `SECRET_KEY` from env (`os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')`)
   - `SQLALCHEMY_DATABASE_URI = 'sqlite:///complaints.db'`
   - `SQLALCHEMY_TRACK_MODIFICATIONS = False`
   - `UPLOAD_FOLDER = 'static/uploads/complaints'`
   - `MAX_CONTENT_LENGTH = 5 * 1024 * 1024` (5MB)
   - `ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}`

2. Create `requirements.txt` with exact versions:
   ```
   Flask==3.0.3
   Flask-SQLAlchemy==3.1.1
   Flask-Login==0.6.3
   Werkzeug==3.0.3
   Pillow==10.4.0
   ```

3. Create `app.py` skeleton with comment sections:
   ```python
   # --- IMPORTS ---
   # --- CONFIG ---
   # --- EXTENSIONS ---
   # --- MODELS ---
   # --- CONSTANTS ---
   # --- HELPERS ---
   # --- AUTH ---
   # --- STUDENT ROUTES ---
   # --- ADMIN ROUTES ---
   # --- ERROR HANDLERS ---
   # --- MAIN ---
   ```
   - Import Flask, render_template, request, redirect, url_for, flash, send_from_directory
   - Import SQLAlchemy, LoginManager
   - Load config from `config.Config`
   - Initialize `db = SQLAlchemy(app)`, `login_manager = LoginManager(app)`
   - `login_manager.login_view = 'login'`, `login_manager.login_message_category = 'info'`
   - Create upload folder if not exists
   - `if __name__ == '__main__': app.run(debug=True)`

4. Create `static/css/style.css` with CSS custom properties from `design.md` palette:
   - `--color-primary`, `--color-primary-hover`, `--color-primary-light`
   - `--color-success`, `--color-success-light`, `--color-warning`, `--color-warning-light`
   - `--color-danger`, `--color-danger-light`, `--color-info`, `--color-info-light`
   - `--color-gray-50` through `--color-gray-900`
   - `--spacing-xs`, `--spacing-sm`, `--spacing-md`, `--spacing-lg`, `--spacing-xl`
   - `--radius-sm`, `--radius-md`, `--radius-lg`
   - `--shadow-card`, `--shadow-modal`
   - `--font-family`, `--fs-xs`, `--fs-sm`, `--fs-base`, `--fs-lg`, `--fs-xl`, `--fs-2xl`
   - Basic reset, body styles, focus-visible ring

5. Create empty `static/js/main.js` with `// Main JS entry point` comment

6. Create folder structure:
   - `templates/student/`, `templates/admin/`
   - `static/uploads/complaints/`
   - `instance/` (will hold SQLite DB)

## What not to do

- Do not implement any routes yet
- Do not create models yet
- Do not create templates yet
- Do not install packages (learner will run `pip install`)
- Do not add any business logic

## Done when

- All files created with correct content
- Folder structure exists
- `pip install -r requirements.txt` succeeds without errors
- `python app.py` starts Flask dev server (even if no routes work yet)

## Verification steps

- [ ] `config.py` exists with all required config values
- [ ] `requirements.txt` has 5 packages with pinned versions
- [ ] `app.py` has all 11 comment sections and basic Flask init
- [ ] `static/css/style.css` has all CSS custom properties from design.md
- [ ] `static/js/main.js` exists
- [ ] Folder structure: `templates/student/`, `templates/admin/`, `static/uploads/complaints/`, `instance/`
- [ ] `pip install -r requirements.txt` completes successfully
- [ ] `python app.py` starts server on http://localhost:5000 (shows 404 for `/` — expected)

**Design check:** CSS custom properties match `design.md` color palette, spacing scale, typography scale, shadows, and border radius. Focus ring uses primary color with 40% opacity.

## Localhost test before continuing

After this card, the learner should test:

- Run `pip install -r requirements.txt` — confirm all 5 packages install without version conflicts
- Run `python app.py` — confirm Flask starts on `http://localhost:5000` with debug mode
- Visit `http://localhost:5000` — confirm 404 page (no routes defined yet, this is expected)
- Stop server with Ctrl+C

If all tests pass, reply `continue`.
If anything fails, reply `fix` and paste the error or describe what you see.

## Stop condition

If `pip install` fails due to network or version issues, stop and fix requirements.txt before continuing.

## Status

Not started