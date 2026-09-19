# Work Card 02 — Database Models

## Goal

Create SQLAlchemy models for User and Complaint with all fields, relationships, enums, and constants.

## Inputs

- `build-blueprint.md` (Data / State / Storage Rules, Architecture Summary)
- `architecture.md` (Data / State Model, Models section)
- `models.py` will be imported by `app.py`

## Files likely touched

- `models.py` — new
- `app.py` — import models, add `db.create_all()` in app context

## Instructions for the coding agent

1. Create `models.py` with:
   - Import: `from flask_sqlalchemy import SQLAlchemy`, `from werkzeug.security import generate_password_hash, check_password_hash`, `from datetime import datetime`, `from enum import Enum`
   - `db = SQLAlchemy()` (initialized in app.py, but declared here for import)

2. Define constants (matching `architecture.md`):
   ```python
   CATEGORIES = [
       'Classroom', 'Furniture', 'Electrical', 'Water / Plumbing',
       'Internet / Wi-Fi', 'Cleanliness', 'Parking', 'Security',
       'Campus Facilities', 'Library', 'Other'
   ]

   STATUSES = ['Submitted', 'Under Review', 'In Progress', 'Resolved', 'Rejected']

   PRIORITIES = ['Low', 'Medium', 'High', 'Critical']

   ROLES = ['student', 'admin']
   ```

3. Define `User` model:
   - `id` — Integer, primary_key
   - `username` — String(50), unique, nullable=False
   - `email` — String(100), unique, nullable=False
   - `password_hash` — String(200), nullable=False
   - `role` — String(10), nullable=False, default='student'
   - `created_at` — DateTime, default=datetime.utcnow
   - Methods: `set_password(password)`, `check_password(password)`, `is_admin()`, `is_student()`
   - `__repr__` returning `<User username>`

4. Define `Complaint` model:
   - `id` — Integer, primary_key
   - `user_id` — Integer, ForeignKey('user.id'), nullable=False
   - `category` — String(30), nullable=False
   - `location` — String(200), nullable=False
   - `description` — Text, nullable=False
   - `image_path` — String(300), nullable=True
   - `status` — String(20), nullable=False, default='Submitted'
   - `priority` — String(10), nullable=False, default='Medium'
   - `admin_remarks` — Text, nullable=True
   - `created_at` — DateTime, default=datetime.utcnow
   - `updated_at` — DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
   - Relationship: `user = db.relationship('User', backref=db.backref('complaints', lazy=True))`
   - Properties: `status_badge_class()`, `priority_badge_class()` returning CSS classes
   - `__repr__` returning `<Complaint id - category>`

4. Update `app.py`:
   - Import `db` from models: `from models import db, User, Complaint`
   - Remove local `db = SQLAlchemy(app)` line
   - Add `with app.app_context(): db.create_all()` before `app.run()`

## What not to do

- Do not create any routes
- Do not create templates
- Do not implement authentication logic
- Do not run migrations (SQLAlchemy create_all is sufficient for SQLite)

## Done when

- `models.py` contains User and Complaint models with all fields, methods, relationships
- Constants match architecture.md exactly
- `app.py` imports models and calls `db.create_all()` in app context
- `python app.py` starts without errors (tables created in instance/complaints.db)

## Verification steps

- [ ] `models.py` exists with User and Complaint classes
- [ ] All 4 constant lists (CATEGORIES, STATUSES, PRIORITIES, ROLES) defined correctly
- [ ] User model has all 6 fields + 4 methods + `__repr__`
- [ ] Complaint model has all 11 fields + relationship + 2 properties + `__repr__`
- [ ] `app.py` imports `db, User, Complaint` from models
- [ ] `app.py` has `with app.app_context(): db.create_all()`
- [ ] Run `python app.py` → server starts → `instance/complaints.db` created
- [ ] Optional: `flask shell` → `from models import User, Complaint; User.query.all()` returns empty list

**Design check:** No design verification needed for backend models (no UI).

## Localhost test before continuing

After this card, the learner should test:

- Run `python app.py` — confirm server starts without SQLAlchemy errors
- Check `instance/complaints.db` file exists (SQLite database created)
- Stop server with Ctrl+C

If all tests pass, reply `continue`.
If anything fails, reply `fix` and paste the error or describe what you see.

## Stop condition

If SQLAlchemy fails to create tables (import errors, circular imports), stop and fix models.py / app.py imports before continuing.

## Status

Not started