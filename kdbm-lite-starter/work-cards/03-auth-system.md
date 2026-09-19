# Work Card 03 — Authentication System

## Goal

Implement registration, login, logout, Flask-Login setup, and role-based access decorators.

## Inputs

- `build-blueprint.md` (Architecture Summary, Implementation Rules)
- `architecture.md` (Authentication section, User Flow)
- `models.py` (User model with role, password methods)

## Files likely touched

- `app.py` — add auth routes, login_manager config, role decorators
- `templates/base.html` — new (base layout with flash messages)
- `templates/student/login.html` — new
- `templates/student/register.html` — new
- `templates/admin/login.html` — new

## Instructions for the coding agent

1. Update `app.py` — Login Manager & User Loader:
   - `login_manager.login_view = 'login'`
   - `login_manager.login_message = 'Please log in to access this page.'`
   - `login_manager.login_message_category = 'info'`
   - `@login_manager.user_loader` → `return User.query.get(int(user_id))`

2. Add role decorators in `app.py` (after user_loader):
   ```python
   from functools import wraps
   from flask import abort
   from flask_login import current_user

   def student_required(f):
       @wraps(f)
       def decorated_function(*args, **kwargs):
           if not current_user.is_authenticated or not current_user.is_student():
               flash('Student access required.', 'error')
               return redirect(url_for('login'))
           return f(*args, **kwargs)
       return decorated_function

   def admin_required(f):
       @wraps(f)
       def decorated_function(*args, **kwargs):
           if not current_user.is_authenticated or not current_user.is_admin():
               flash('Admin access required.', 'error')
               return redirect(url_for('admin_login'))
           return f(*args, **kwargs)
       return decorated_function
   ```

3. Create `templates/base.html` with:
   - `<!DOCTYPE html>`, `<html lang="en">`, Bootstrap 5 CDN (CSS + JS bundle)
   - Bootstrap Icons CDN
   - `<head>`: meta tags, title block, `style.css` link
   - `<body>`: navbar (conditional — shown only when authenticated), main container, flash messages block, footer
   - Blocks: `title`, `head_extra`, `content`, `scripts`
   - Flash message rendering with dismiss button, categories: success/error/warning/info

4. Create `templates/student/base.html` extending `base.html`:
   - Navbar with: "Campus Complaints" brand, "Dashboard", "Submit Complaint", "My Complaints", user dropdown (username + Logout)
   - Active nav highlighting via `request.endpoint`

5. Create `templates/admin/base.html` extending `base.html`:
   - Navbar with: "Admin Dashboard" brand (red badge), "Dashboard", "Complaints", "Statistics", user dropdown (username + Logout)
   - Different styling (darker brand color) to distinguish from student portal

6. Create `templates/student/login.html` extending `student/base.html`:
   - Centered card (max-width 400px)
   - Form: email (type=email), password (type=password), remember checkbox, submit button
   - Link to register page
   - CSRF not required (same-origin)

7. Create `templates/student/register.html` extending `student/base.html`:
   - Centered card
   - Form: username, email, password, confirm password, submit
   - Validation: username ≥ 3 chars, email format, password ≥ 8 chars, passwords match
   - Server-side: check username/email unique, flash errors
   - On success: hash password, create User(role='student'), flash success, redirect to login

8. Create `templates/admin/login.html` extending `admin/base.html`:
   - Same as student login but posts to `/admin/login`
   - Validates user exists AND `user.is_admin()` else flash error

9. Add routes in `app.py`:
   - `/login` (GET/POST) — student login, redirect to `/dashboard` on success
   - `/register` (GET/POST) — student registration
   - `/logout` — logout_user(), redirect to `/login`
   - `/admin/login` (GET/POST) — admin login, redirect to `/admin/dashboard`
   - `/admin/logout` — logout_user(), redirect to `/admin/login`
   - `/` — redirect to `/login` (or `/dashboard` if authenticated student)

## What not to do

- Do not implement student dashboard or complaint routes yet
- Do not implement admin dashboard or complaint management yet
- Do not add password reset
- Do not add "remember me" cookie persistence beyond Flask-Login default

## Done when

- Student can register → login → logout
- Admin can login → logout (admin user must be created manually or via seeder later)
- Role decorators block unauthorized access (student cannot access /admin/*, admin cannot access student routes)
- Flash messages display correctly on login/error
- All templates extend correct base, navbar shows appropriate links

## Verification steps

- [ ] `app.py` has login_manager config, user_loader, student_required, admin_required
- [ ] `templates/base.html` has Bootstrap 5 CDN, flash messages, blocks
- [ ] `templates/student/base.html` has student navbar with correct links
- [ ] `templates/admin/base.html` has admin navbar with correct links
- [ ] `templates/student/login.html` renders form, posts to `/login`
- [ ] `templates/student/register.html` renders form, validates, creates user
- [ ] `templates/admin/login.html` renders form, validates admin role
- [ ] Routes: `/login`, `/register`, `/logout`, `/admin/login`, `/admin/logout`, `/` all respond
- [ ] Register new student → login → see student navbar → logout works
- [ ] Login as admin (create manually in shell) → see admin navbar → logout works
- [ ] Student tries `/admin/dashboard` → redirected to login with flash
- [ ] Admin tries `/dashboard` → redirected to admin login with flash

**Design check:** Login/register forms follow design.md — centered card, 40px inputs, labels above, primary button full-width on mobile, proper spacing, focus rings, error messages in red 500.

## Localhost test before continuing

After this card, the learner should test:

- Start `python app.py`
- Visit `http://localhost:5000/register` — register a new student (e.g., `testuser` / `test@example.com` / `password123`)
- Verify redirect to login, then login successfully → see student dashboard (404 expected, but navbar visible)
- Visit `http://localhost:5000/admin/dashboard` — should redirect to `/admin/login` with flash "Admin access required"
- Visit `http://localhost:5000/admin/login` — login fails for student (flash error)
- Create admin user via flask shell: `from models import User, db; u = User(username='admin', email='admin@test.com', role='admin'); u.set_password('admin123'); db.session.add(u); db.session.commit()`
- Login as admin at `/admin/login` → see admin navbar
- Logout from both portals

If all tests pass, reply `continue`.
If anything fails, reply `fix` and paste the error or describe what you see.

## Stop condition

If Flask-Login session not persisting (check secret key, user_loader), stop and fix before continuing.

## Status

Not started