# Work Card 06 — My Complaints & Detail

## Goal

Build student complaint list page with sortable table and complaint detail view showing status timeline and admin remarks.

## Inputs

- `build-blueprint.md` (Student Routes, File and Folder Expectations)
- `architecture.md` (Student Routes: `/complaints`, `/complaint/<id>`)
- `design.md` (Component Style - Tables, Cards, Badges, Mobile Rules)

## Files likely touched

- `app.py` — `/complaints` and `/complaint/<id>` routes
- `templates/student/complaints.html` — new
- `templates/student/complaint_detail.html` — new
- `static/css/style.css` — table styles, detail layout, timeline

## Instructions for the coding agent

1. Add routes in `app.py`:
   - `@app.route('/complaints')` with `@login_required` + `@student_required`
     - Query: `complaints = Complaint.query.filter_by(user_id=current_user.id).order_by(Complaint.created_at.desc()).all()`
     - Render `student/complaints.html`
   - `@app.route('/complaint/<int:complaint_id>')` with `@login_required` + `@student_required`
     - Query: `complaint = Complaint.query.get_or_404(complaint_id)`
     - Authorization: `if complaint.user_id != current_user.id: abort(403)`
     - Render `student/complaint_detail.html`

2. Create `templates/student/complaints.html` extending `student/base.html`:
   - Page title: "My Complaints"
   - Card with table:
     - Columns: ID, Category, Location, Status, Priority, Submitted Date, Actions
     - Status badge using `complaint.status_badge_class()`
     - Priority badge using `complaint.priority_badge_class()`
     - Actions: "View" button/link to `/complaint/<id>`
     - Empty state: "No complaints submitted yet." + CTA to `/submit`
     - Mobile: table → card list (each row = card with labeled fields) on < 768px

3. Create `templates/student/complaint_detail.html` extending `student/base.html`:
   - Page title: "Complaint #{{ complaint.id }}"
   - Header card: Complaint ID, Category badge, Status badge, Priority badge, Submitted date
   - Details card:
     - Location (with map pin icon)
     - Description (formatted with line breaks)
     - Image (if exists): `<img src="{{ url_for('static', filename=complaint.image_path) }}" alt="Complaint image">` max-width 100%
   - Admin Response card (if admin_remarks or status != Submitted):
     - Status timeline: simple vertical list with icons
       - Submitted: always, timestamp
       - Under Review: if status ≥ Under Review, show admin_remarks if any
       - In Progress: if status ≥ In Progress
       - Resolved/Rejected: final status with timestamp
     - Admin Remarks: if `complaint.admin_remarks`, show in styled block
   - Back button to `/complaints`

3. Add CSS in `static/css/style.css`:
   - `.complaint-table` — responsive, striped, hover
   - `.complaint-card-mobile` — for < 768px, each complaint as card with labeled fields
   - `.timeline` — vertical line with dots, labels, timestamps
   - `.admin-remarks` — bordered block with gray background
   - `.complaint-image` — max-width 100%, border-radius, shadow

## What not to do

- Do not add edit/delete for student complaints (read-only)
- Do not add pagination (student typically has few complaints)
- Do not add real-time updates
- Do not add comments/threading

## Done when

- `/complaints` shows all student's complaints in table (or card list on mobile)
- Click "View" → `/complaint/<id>` shows full details
- Status badges, priority badges render with correct colors
- Image displays if uploaded
- Admin remarks and status timeline show when admin has updated
- Unauthorized access (other student's complaint) → 403
- Mobile: table converts to card list, image scales, timeline stacks

## Verification steps

- [ ] `/complaints` route lists all complaints for current user only
- [ ] Table columns: ID, Category, Location, Status, Priority, Date, Actions
- [ ] Status badges: correct colors for all 5 statuses
- [ ] Priority badges: correct colors for all 4 priorities
- [ ] Click "View" → `/complaint/<id>` shows detail page
- [ ] Detail page shows: ID, category, status, priority, date, location, description, image (if any)
- [ ] Admin remarks section shows only if remarks exist or status changed
- [ ] Status timeline shows progression with timestamps
- [ ] Other student's complaint ID → 403 Forbidden
- [ ] Empty state on `/complaints` with CTA to submit
- [ ] Mobile < 768px: table → card list, detail page stacks, image full-width
- [ ] Navbar "My Complaints" highlighted active

**Design check:** Table follows design.md — 48px row height, striped, hover highlight, badges with text+color. Detail page: card layout, 24px padding, timeline vertical with connectors, admin remarks in distinct block. Mobile: card list with labeled fields, no horizontal scroll.

## Localhost test before continuing

After this card, the learner should test:

- Start `python app.py`
- Login as student → go to `/complaints` — verify empty state (or list if previous test data exists)
- Submit a complaint via `/submit` → go to `/complaints` → verify appears in list
- Click "View" → verify detail page shows all fields, status badge, priority badge
- Submit another complaint → verify both show in list, ordered by date desc
- Try accessing another student's complaint ID directly → 403
- Mobile view: `/complaints` shows card list, detail page stacks properly

If all tests pass, reply `continue`.
If anything fails, reply `fix` and paste the error or describe what you see.

## Stop condition

If authorization check fails (students seeing each other's complaints), stop and fix ownership verification in `/complaint/<id>` route before continuing.

## Status

Not started