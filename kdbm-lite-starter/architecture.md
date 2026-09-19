# Architecture

## Build Shape

Full-stack web application (Python Flask + SQLite + Bootstrap) — requires authentication, database, backend, file uploads, role-based access, admin system.

## Stack Decision

- **Backend:** Python Flask (single `app.py` for simplicity, modular sections for student/admin)
- **Database:** SQLite via Flask-SQLAlchemy
- **Authentication:** Flask-Login with Werkzeug password hashing
- **Frontend:** Bootstrap 5 (CDN), HTML/CSS/JS, Jinja2 templates
- **File Uploads:** `static/uploads/complaints/` with UUID filenames, max 5MB, allowed: PNG/JPG/JPEG/WebP
- **Forms:** Plain HTML forms (no Flask-WTF)
- **Dependencies:** Flask, Flask-SQLAlchemy, Flask-Login, Werkzeug, Pillow (for image validation)

## Structure Overview

```
smartcampuscomplaintsystem/
├── app.py                    # Single Flask app with student/admin sections
├── config.py                 # Configuration (secret key, DB URI, upload folder)
├── models.py                 # SQLAlchemy models (User, Complaint)
├── requirements.txt          # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css         # Custom styles
│   ├── js/
│   │   └── main.js           # Client-side JS
│   └── uploads/
│       └── complaints/       # Uploaded complaint images
├── templates/
│   ├── base.html             # Base layout with Bootstrap
│   ├── student/
│   │   ├── base.html         # Student layout (extends base)
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── submit.html
│   │   ├── complaints.html
│   │   └── complaint_detail.html
│   └── admin/
│       ├── base.html         # Admin layout (extends base)
│       ├── login.html
│       ├── dashboard.html
│       ├── complaints.html
│       └── complaint_detail.html
├── instance/
│   └── complaints.db         # SQLite database (auto-created)
└── sample_data.py            # Script to populate demo data
```

## Component Map

### Backend Components (app.py sections)

**Configuration & Setup:**
- Flask app factory, config loading, extensions init (db, login_manager)
- Upload folder creation, allowed extensions config

**Models (models.py):**
- `User` — id, username, email, password_hash, role (student/admin), created_at
- `Complaint` — id, user_id, category, location, description, image_path, status, priority, admin_remarks, created_at, updated_at

**Authentication:**
- `@login_manager.user_loader`
- `/login` (student), `/logout`, `/register`
- `/admin/login`, `/admin/logout`
- Role-based decorators: `@student_required`, `@admin_required`

**Student Routes:**
- `/` → redirect to `/login` or `/dashboard`
- `/dashboard` — student dashboard (stats + recent complaints)
- `/submit` — complaint submission form (GET/POST)
- `/complaints` — list student's complaints with status
- `/complaint/<id>` — complaint detail view

**Admin Routes:**
- `/admin/dashboard` — stats cards + charts data
- `/admin/complaints` — paginated, searchable, filterable table
- `/admin/complaint/<id>` — detail + status/priority/remarks update
- `/admin/stats` — JSON endpoint for charts

**Utilities:**
- File upload handler (secure_filename + UUID)
- Category/status/priority constants
- Sample data seeder

### Frontend Components

**Shared:**
- `base.html` — Bootstrap 5, navbar, flash messages, footer
- `style.css` — custom colors, card styles, table enhancements
- `main.js` — form validation, image preview, AJAX for admin actions

**Student Pages:**
- Login/Register forms with validation
- Dashboard: stat cards (my total, pending, in-progress, resolved) + recent complaints table
- Submit: category dropdown, location input, description textarea, image upload with preview
- My Complaints: sortable table with status badges
- Complaint Detail: read-only view with status timeline

**Admin Pages:**
- Login (separate from student)
- Dashboard: stat cards (total, new, in-progress, resolved, critical) + category/status charts
- Complaints Management: search box, filter dropdowns (category, status, priority), paginated table with actions
- Complaint Detail: full info + status/priority dropdowns + remarks textarea + update button

## Data / State Model

### User
| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | Primary Key |
| username | String(50) | Unique, Not Null |
| email | String(100) | Unique, Not Null |
| password_hash | String(200) | Not Null |
| role | String(10) | Not Null, Enum: 'student', 'admin' |
| created_at | DateTime | Default: utcnow |

### Complaint
| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | Foreign Key → User.id, Not Null |
| category | String(30) | Not Null, Enum: 11 categories |
| location | String(200) | Not Null |
| description | Text | Not Null |
| image_path | String(300) | Nullable |
| status | String(20) | Not Null, Default: 'Submitted', Enum: 5 statuses |
| priority | String(10) | Not Null, Default: 'Medium', Enum: 4 priorities |
| admin_remarks | Text | Nullable |
| created_at | DateTime | Default: utcnow |
| updated_at | DateTime | Default: utcnow, On Update: utcnow |

### Constants
```python
CATEGORIES = [
    'Classroom', 'Furniture', 'Electrical', 'Water / Plumbing',
    'Internet / Wi-Fi', 'Cleanliness', 'Parking', 'Security',
    'Campus Facilities', 'Library', 'Other'
]

STATUSES = ['Submitted', 'Under Review', 'In Progress', 'Resolved', 'Rejected']

PRIORITIES = ['Low', 'Medium', 'High', 'Critical']
```

## Storage Logic

- **Database:** SQLite file at `instance/complaints.db` (Flask-SQLAlchemy default)
- **File Uploads:** `static/uploads/complaints/{uuid}.{ext}` — only path stored in DB
- **Session:** Flask-Login manages user session via secure cookie
- **Configuration:** `config.py` with `SECRET_KEY`, `SQLALCHEMY_DATABASE_URI`, `UPLOAD_FOLDER`, `MAX_CONTENT_LENGTH`

## User Flow

### Student Flow
1. Landing → `/login` or `/register`
2. Register → auto-login → `/dashboard`
3. Login → `/dashboard`
4. Dashboard → view stats, recent complaints, navigate to Submit or My Complaints
5. Submit Complaint → form → POST → save to DB + upload image → redirect to My Complaints with flash
6. My Complaints → click complaint → Complaint Detail (read-only, shows status, admin remarks if any)
7. Logout

### Admin Flow
1. `/admin/login` → authenticate admin user → `/admin/dashboard`
2. Dashboard → view stats cards, charts, recent complaints
3. Complaints Management → search/filter/paginate → click complaint
4. Complaint Detail → view all info → update status/priority/remarks → save → flash confirmation
5. Logout

## File Expectations

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application, all routes, init |
| `models.py` | SQLAlchemy models (User, Complaint) |
| `config.py` | Configuration class |
| `requirements.txt` | pip dependencies |
| `sample_data.py` | Demo data seeder (run once) |
| `templates/base.html` | Master layout |
| `templates/student/*.html` | Student portal pages |
| `templates/admin/*.html` | Admin portal pages |
| `static/css/style.css` | Custom styling |
| `static/js/main.js` | Client-side interactions |

## Constraints

- Single `app.py` (no blueprints) for beginner clarity
- No Flask-WTF — plain HTML forms with server-side validation
- Bootstrap 5 via CDN (no build step)
- SQLite for zero-config local development
- Password hashing via `werkzeug.security.generate_password_hash` / `check_password_hash`
- Role checks via `current_user.role` in decorators
- File upload validation: extension + MIME type + size (5MB)
- All admin routes protected by `@admin_required`
- All student routes protected by `@student_required` (or `@login_required` + role check)

## Technical Non-Goals

- No REST API (server-rendered Jinja2 templates)
- No WebSockets / real-time updates
- No email notifications
- No password reset flow
- No user profile editing
- No complaint comments/threading
- No export/PDF generation
- No unit tests in planning phase
- No Docker / containerization
- No CI/CD pipeline

## Verification Notes

- Run `python sample_data.py` → creates admin (admin/admin123) + 3 students + 10 sample complaints
- Start app: `python app.py` → http://localhost:5000
- Student login → submit complaint with image → verify appears in My Complaints
- Admin login → dashboard shows stats → filter complaints → update status/priority/remarks → verify persists
- Refresh browser → data persists in SQLite
- Mobile responsive: test dashboard tables, forms, modals