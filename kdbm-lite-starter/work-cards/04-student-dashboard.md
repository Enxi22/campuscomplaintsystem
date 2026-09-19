# Work Card 04 — Student Dashboard & Navigation

## Goal

Build student portal layout, dashboard with stat cards, recent complaints table, and quick action card.

## Inputs

- `build-blueprint.md` (File and Folder Expectations, Student Routes)
- `architecture.md` (Student Routes, User Flow)
- `design.md` (Layout Rules, Component Style, Cards, Tables, Mobile Rules)

## Files likely touched

- `app.py` — student dashboard route
- `templates/student/dashboard.html` — new
- `templates/student/base.html` — update active nav highlighting
- `static/css/style.css` — add dashboard-specific styles (stat cards, table responsive)

## Instructions for the coding agent

1. Add route in `app.py`:
   - `@app.route('/dashboard')` with `@login_required` + `@student_required`
   - Query: `my_complaints = Complaint.query.filter_by(user_id=current_user.id).order_by(Complaint.created_at.desc()).all()`
   - Stats: total, submitted/under_review (pending), in_progress, resolved
   - Recent: first 5 complaints
   - Render `student/dashboard.html` with stats + recent

2. Create `templates/student/dashboard.html` extending `student/base.html`:
   - Page title: "Dashboard"
   - **Stat Cards Row** (4 cards, responsive: 1 col <576px, 2 col ≥576px, 4 col ≥992px):
     - Total Complaints (blue primary)
     - Pending (Submitted + Under Review) — amber/warning
     - In Progress — cyan/info
     - Resolved — emerald/success
   - Each card: icon (Bootstrap Icons), number (large), label, subtle background color
   - **Recent Complaints Card**:
     - Header: "Recent Complaints" + "View All" link to `/complaints`
     - Table: ID, Category, Location, Status, Priority, Date
     - Status badge using `complaint.status_badge_class()` property
     - Priority badge using `complaint.priority_badge_class()` property
     - Empty state: "No complaints yet. Submit your first complaint." + primary button to `/submit`
   - **Quick Action Card**:
     - "Submit New Complaint" — large primary button to `/submit`
     - Icon + text

3. Update `templates/student/base.html`:
   - Ensure active nav highlighting works for `dashboard`, `submit`, `complaints` endpoints
   - User dropdown shows username, role badge (Student)

4. Add CSS in `static/css/style.css`:
   - `.stat-card` — padding, border-radius, background, icon styling
   - `.stat-number` — 2.5rem, 700 weight, color matching card
   - `.stat-label` — 0.875rem, gray-600
   - `.table-responsive` wrapper for mobile horizontal scroll
   - `.badge-status-*` and `.badge-priority-*` classes matching design.md colors
   - Mobile: stat cards stack 1-col <576px, 2-col ≥576px

## What not to do

- Do not implement submit complaint form yet
- Do not implement my complaints list page yet
- Do not implement complaint detail yet
- Do not add charts (admin only)

## Done when

- Student login → redirect to `/dashboard` shows 4 stat cards with correct counts (0 initially)
- Recent complaints table shows empty state with CTA to submit
- Quick action card navigates to `/submit` (404 expected, but link works)
- Navbar highlights "Dashboard" as active
- Mobile: stat cards stack properly, table horizontally scrolls
- All colors match design.md palette

## Verification steps

- [ ] `/dashboard` route exists with `@login_required` + `@student_required`
- [ ] Stats calculate correctly: total, pending (Submitted+Under Review), in_progress, resolved
- [ ] Recent complaints limited to 5, ordered by created_at desc
- [ ] `templates/student/dashboard.html` extends `student/base.html`
- [ ] 4 stat cards render with icons, numbers, labels, correct colors
- [ ] Recent complaints table renders with columns: ID, Category, Location, Status, Priority, Date
- [ ] Status badges use correct colors: Submitted=gray, Under Review=cyan, In Progress=amber, Resolved=emerald, Rejected=red
- [ ] Priority badges: Low=gray, Medium=blue, High=orange, Critical=red
- [ ] Empty state shows when no complaints with CTA button
- [ ] Mobile: stat cards 1-col <576px, 2-col 576-991px, 4-col ≥992px
- [ ] Table horizontally scrolls on mobile with sticky first column (ID)
- [ ] Navbar active state highlights "Dashboard"

**Design check:** Dashboard follows design.md — card grid layout, 24px gutter, 8px radius, subtle shadows, stat cards use semantic colors, table row height ≥48px, striped rows, hover highlight, status badges have text+color, mobile stacking works.

## Localhost test before continuing

After this card, the learner should test:

- Start `python app.py`
- Login as student → verify redirect to `/dashboard`
- Verify 4 stat cards show 0 counts, correct icons/colors
- Verify "Recent Complaints" shows empty state with "Submit your first complaint" button
- Click button → goes to `/submit` (404 expected)
- Resize browser to mobile width (<576px) — stat cards stack 1 column, table scrolls horizontally
- Check navbar "Dashboard" is highlighted

If all tests pass, reply `continue`.
If anything fails, reply `fix` and paste the error or describe what you see.

## Stop condition

If template inheritance breaks (base.html blocks not working), stop and fix template structure before continuing.

## Status

Not started