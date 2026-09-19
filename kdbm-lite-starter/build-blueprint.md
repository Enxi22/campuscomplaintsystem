# Build Blueprint

## Source Files

- `project-brief.md` — Project identity, users, goals, success criteria
- `architecture.md` — Stack, structure, data models, routes, constraints
- `design.md` — Visual mood, layout rules, color palette, components, mobile, accessibility

## Project Identity

**Smart Campus Complaint System** — A full-stack web application where students submit campus complaints with categories/locations/images, track status via complaint ID, and admins manage complaints through a dashboard with filtering, status updates, priorities, remarks, and analytics.

## Build Shape

Full-stack web application (Python Flask + SQLite + Bootstrap) — requires authentication, database, backend, file uploads, role-based access, admin system. Exceeds KDBM Lite browser-only guardrails; planning phase only per learner choice.

## Version-One Promise

A working local Flask application with:
- Student registration/login, complaint submission (category, location, description, optional image), complaint tracking with status badges, complaint detail view
- Admin login, dashboard with statistics cards and charts, complaint management with search/filter/pagination, complaint detail with status/priority/remarks editing
- SQLite database with User and Complaint models, Flask-Login authentication, Werkzeug password hashing
- Bootstrap 5 responsive UI matching calm productivity design: clean cards, generous spacing, semantic status colors, mobile-first
- Sample data seeder creating admin user + demo students + 10 varied complaints

## Scope Lock

### Now (Planning Complete — Ready for Implementation)

- All planning documents (this blueprint + work cards)
- Project structure, dependencies, configuration
- Database models and migrations (Flask-SQLAlchemy create_all)
- Authentication system (register, login, logout, role guards)
- Student routes: dashboard, submit complaint, my complaints, complaint detail
- Admin routes: dashboard, complaints list (search/filter/paginate), complaint detail (edit status/priority/remarks)
- Templates: base, student portal (5 pages), admin portal (4 pages)
- Static assets: custom CSS, vanilla JS for interactions
- File upload handling with validation
- Sample data seeder script
- Verification checklist for manual testing

### Later (Post-V1 Enhancements)

- Email notifications on status change
- Password reset flow
- User profile editing (avatar, password change)
- Complaint comments/threading (student-admin dialogue)
- Export complaints to CSV/PDF
- Real-time updates via WebSockets
- Dark mode toggle
- Multi-campus support
- Advanced analytics (response time, resolution rate, category trends)
- Unit/integration tests (pytest)
- Docker containerization
- CI/CD pipeline

### Never

- Payment integration
- Social login (Google, Microsoft)
- Mobile native app
- Multi-language/i18n
- AI-powered complaint categorization
- Public complaint board/forum
- Third-party integrations (Slack, Teams, Jira)

## Architecture Summary

**Backend:** Single `app.py` with modular sections (config, models, auth, student routes, admin routes, utilities). Flask-SQLAlchemy ORM, Flask-Login for sessions, Werkzeug for password hashing. SQLite database at `instance/complaints.db`.

**Models:**
- `User` — id, username, email, password_hash, role (student/admin), created_at
- `Complaint` — id, user_id (FK), category, location, description, image_path, status, priority, admin_remarks, created_at, updated_at

**Constants:** 11 categories, 5 statuses, 4 priorities (defined in `architecture.md`)

**Routes:**
- Public: `/login`, `/register`, `/logout`
- Student: `/dashboard`, `/submit`, `/complaints`, `/complaint/<id>`
- Admin: `/admin/login`, `/admin/logout`, `/admin/dashboard`, `/admin/complaints`, `/admin/complaint/<id>`, `/admin/stats` (JSON)

**File Uploads:** `static/uploads/complaints/{uuid}.{ext}` — 5MB max, PNG/JPG/JPEG/WebP, secure filename + MIME validation.

**Security:** Role decorators (`@student_required`, `@admin_required`), CSRF via Flask-WTF not used (rely on same-origin + login_required), parameterized queries via ORM, file type validation.

## Data / State / Storage Rules

| Entity | Storage | Key Rules |
|--------|---------|-----------|
| Users | SQLite (User table) | Unique username/email, hashed password, role enum |
| Complaints | SQLite (Complaint table) | FK to User, category/status/priority enums, nullable image_path |
| Sessions | Flask-Login (secure cookie) | `remember_me` optional, 31-day expiry |
| Uploaded Files | Filesystem (`static/uploads/complaints/`) | UUID names, only path in DB, served as static files |
| Config | `config.py` + env vars | `SECRET_KEY`, `DATABASE_URI`, `UPLOAD_FOLDER`, `MAX_CONTENT_LENGTH` |

**State Transitions (Complaint Status):**
`Submitted` → `Under Review` → `In Progress` → `Resolved`  
`Submitted` → `Rejected` (admin can reject at any stage)  
Admin can move between any statuses (no strict enforcement in V1)

**Priority:** Set by admin (default: Medium). Student cannot set priority.

## Design Direction Summary

**Borrow from "Calm Productivity App":**
- Clean dashboard layout with organized card grid and clear visual hierarchy
- Generous whitespace (8px/16px/24px rhythm) — no cramped elements
- Subtle card shadows (0 2px 8px rgba(0,0,0,0.08)), 8–12px border radius
- Readable tables (48px+ row height, striped, sortable headers, status badges)
- Single-column forms with labels above inputs, generous tap targets
- System UI font stack — no external font loads
- Semantic color system: Blue (primary), Emerald (success), Amber (warning), Red (danger), Cyan (info)
- Mobile-first: sidebar → drawer, tables → card lists, forms stacked
- Accessibility: semantic HTML, focus rings, ARIA labels, WCAG AA contrast

**Do Not Copy:**
- Any brand-specific colors, logos, illustrations
- Proprietary icon sets (use Bootstrap Icons)
- Dark mode as default
- Complex animations (subtle 150ms transitions only)
- Exact layout measurements (adapt to content)

**Result Feel:** Student-friendly and calm — professional campus style, modern, approachable, trustworthy.

## Implementation Rules

1. **Single `app.py`** — no blueprints. Use comment sections: `# --- CONFIG ---`, `# --- MODELS ---`, `# --- AUTH ---`, `# --- STUDENT ROUTES ---`, `# --- ADMIN ROUTES ---`, `# --- UTILITIES ---`

2. **Models in `models.py`** — imported in `app.py`. Use Flask-SQLAlchemy declarative base.

3. **Templates:** Jinja2 with template inheritance. `base.html` → `student/base.html` / `admin/base.html` → page templates.

4. **Forms:** Plain HTML `<form>` with server-side validation in route handlers. No Flask-WTF.

5. **Validation:** 
   - Registration: username/email unique, password ≥ 8 chars
   - Login: verify hash, check role for admin routes
   - Complaint submit: category required, location required, description ≥ 20 chars, file type/size validated
   - Admin edit: status/priority must be valid enum values

6. **Flash Messages:** Categories: `success`, `error`, `warning`, `info`. Rendered in base template with dismiss button.

7. **Pagination:** 10 items per page. Admin complaints list only.

8. **Search/Filter:** Admin complaints — `q` (search description/location), `category`, `status`, `priority` as query params. Preserved in pagination links.

9. **Charts:** Admin dashboard — Chart.js via CDN. Two doughnut charts: complaints by category, complaints by status. Data from `/admin/stats` JSON endpoint.

10. **Image Preview:** Client-side JS shows thumbnail after file selection. Server validates MIME + size on upload.

11. **Error Handling:** 404/500 templates. DB errors → flash + redirect. Validation errors → re-render form with values + error messages.

12. **No Secrets in Code:** `SECRET_KEY` from env var with dev fallback. Database URI relative path.

13. **Sample Data:** `sample_data.py` creates:
    - Admin: `admin` / `admin123`
    - Students: `student1`/`student123`, `student2`/`student123`, `student3`/`student123`
    - 10 complaints across categories, statuses, priorities, with/without images (placeholder SVGs)

## File and Folder Expectations

```
smartcampuscomplaintsystem/
├── app.py
├── config.py
├── models.py
├── requirements.txt
├── sample_data.py
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── uploads/
│       └── complaints/
├── templates/
│   ├── base.html
│   ├── 404.html
│   ├── 500.html
│   ├── student/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── submit.html
│   │   ├── complaints.html
│   │   └── complaint_detail.html
│   └── admin/
│       ├── base.html
│       ├── login.html
│       ├── dashboard.html
│       ├── complaints.html
│       └── complaint_detail.html
└── instance/
    └── complaints.db (auto-created)
```

## Work Card Plan

| Card | Title | Scope | Verification |
|------|-------|-------|--------------|
| 01 | Project Setup & Config | `config.py`, `requirements.txt`, folder structure, `app.py` skeleton | `pip install -r requirements.txt` succeeds |
| 02 | Database Models | `models.py` with User, Complaint, constants | `flask shell` → `db.create_all()` works |
| 03 | Authentication System | Login/register/logout, Flask-Login, role decorators | Register → login → logout works for both roles |
| 04 | Student Dashboard & Navigation | Base templates, student layout, dashboard with stat cards | Student login → dashboard shows 4 stats + recent table |
| 05 | Submit Complaint Form | `/submit` GET/POST, category dropdown, location, description, image upload with preview | Submit complaint with image → appears in My Complaints |
| 06 | My Complaints & Detail | `/complaints` list, `/complaint/<id>` detail with status badge | Click complaint → detail shows all fields + status |
| 07 | Admin Dashboard | Admin layout, login, dashboard with 5 stat cards + 2 Chart.js charts | Admin login → dashboard shows stats + charts |
| 08 | Admin Complaints Management | `/admin/complaints` with search, filter, pagination, table | Search/filter/paginate works, click → detail |
| 09 | Admin Complaint Detail & Edit | `/admin/complaint/<id>` — view + edit status/priority/remarks | Change status/priority/remarks → saves + flash |
| 10 | Sample Data & Polish | `sample_data.py`, error pages, empty states, loading states, mobile check | Run seeder → 10 complaints visible; mobile responsive |

## Review Mirror

After each work card, verify:
- [ ] Code matches blueprint scope (no extra features)
- [ ] Design rules applied (spacing, colors, components, mobile)
- [ ] Accessibility basics met (labels, focus, contrast, semantics)
- [ ] Anti-slop rules followed (no fake content, real data only)
- [ ] Manual test passes (happy path + one edge case)
- [ ] `build-status.md` updated with completed card

## Proof Ladder

1. **Local Dev:** `python app.py` → http://localhost:5000
2. **Student Flow:** Register → login → submit complaint (with image) → view in My Complaints → detail view
3. **Admin Flow:** Login as admin → dashboard (stats + charts) → complaints list (search/filter) → edit complaint (status/priority/remarks) → verify persists
4. **Persistence:** Refresh browser → data remains. Restart server → data remains.
5. **Mobile:** Chrome DevTools device toolbar (375px, 768px) — no horizontal scroll, touch targets 44px+
6. **Sample Data:** `python sample_data.py` → 1 admin + 3 students + 10 complaints load correctly

## 60-Second Explanation Template

> "Smart Campus Complaint System is a Flask web app where students report campus issues — like broken furniture, Wi-Fi problems, or plumbing leaks — by selecting a category, entering a location, describing the problem, and optionally uploading a photo. They get a complaint ID and can track status updates. Admins log into a dashboard showing real-time statistics, filter and search all complaints, and update each one's status, priority, and add remarks. It uses SQLite for zero-config local development, Flask-Login for authentication, and Bootstrap 5 for a clean, calm, responsive UI that works on mobile. The whole thing runs with `python app.py` — no Docker, no external services."

## Guardrails for the Coding Agent

- Read `build-status.md`, `build-blueprint.md`, and the current work card before editing
- Implement **only** the current work card — do not jump ahead
- Stop after verification steps pass
- Update `build-status.md` after each work card (completed cards, in-progress, decisions)
- Do not add backend/auth/database/API beyond what this blueprint explicitly specifies
- Do not add secrets, API keys, or credentials to code — use environment variables
- Do not invent claims, testimonials, logos, or real-looking fake numbers
- Apply the anti-slop rules from `design.md` (no lorem ipsum, no fake content, one primary action per screen)
- Use the exact file/folder structure defined in this blueprint
- Follow the color palette, spacing, typography, and component styles from `design.md`
- All admin routes must enforce `@admin_required`; all student routes must enforce `@student_required` (or `@login_required` + role check)
- File uploads must validate extension, MIME type, and size (5MB) server-side
- Passwords must be hashed with `werkzeug.security.generate_password_hash` / `check_password_hash`
- Bootstrap 5 via CDN only — no build step, no local node_modules
- Chart.js via CDN for admin dashboard charts
- System UI font stack only — no Google Fonts or external font loads