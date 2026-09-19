# Work Card 07 — Admin Dashboard

## Goal

Build admin dashboard with 5 stat cards, 2 Chart.js charts (category + status distribution), and recent complaints table.

## Inputs

- `build-blueprint.md` (Admin Routes, Architecture Summary)
- `architecture.md` (Admin Routes, User Flow)
- `design.md` (Layout Rules, Component Style - Cards, Charts, Tables, Admin Portal)

## Files likely touched

- `app.py` — `/admin/dashboard`, `/admin/stats` (JSON endpoint)
- `templates/admin/dashboard.html` — new
- `templates/admin/base.html` — verify active nav
- `static/css/style.css` — admin dashboard styles, chart containers
- `static/js/main.js` — Chart.js initialization

## Instructions for the coding agent

1. Add routes in `app.py`:
   - `@app.route('/admin/dashboard')` with `@login_required` + `@admin_required`
     - Stats: total, new (Submitted), in_progress (Under Review + In Progress), resolved, critical
     - Recent: 10 most recent complaints across all users
     - Render `admin/dashboard.html`
   - `@app.route('/admin/stats')` with `@login_required` + `@admin_required`
     - Return JSON: `{ categories: {label: count}, statuses: {label: count} }`
     - Query: group by category, group by status

2. Create `templates/admin/dashboard.html` extending `admin/base.html`:
   - Page title: "Admin Dashboard"
   - **Stat Cards Row** (5 cards, responsive: 1 col <576px, 2 col 576-767px, 3 col 768-991px, 5 col ≥992px):
     - Total Complaints (primary blue)
     - New (Submitted) — gray
     - In Progress (Under Review + In Progress) — amber/cyan
     - Resolved — emerald
     - Critical Priority — red
   - **Charts Row** (2 cards side-by-side on ≥768px, stacked on mobile):
     - Left: "Complaints by Category" — doughnut chart
     - Right: "Complaints by Status" — doughnut chart
     - Each in card with canvas element
   - **Recent Complaints Card**:
     - Header: "Recent Complaints" + "View All" link to `/admin/complaints`
     - Table: ID, Student, Category, Location, Status, Priority, Date, Actions
     - Student column shows username (link to filter by student later)
     - Actions: "View" → `/admin/complaint/<id>`
     - Empty state if no complaints

3. Add Chart.js via CDN in `templates/admin/base.html` (or dashboard.html head_extra block):
   - `<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>`

3. Add JS in `static/js/main.js`:
   ```javascript
   // Admin dashboard charts
   document.addEventListener('DOMContentLoaded', () => {
       const categoryCtx = document.getElementById('categoryChart');
       const statusCtx = document.getElementById('statusChart');

       if (categoryCtx) {
           fetch('/admin/stats')
               .then(res => res.json())
               .then(data => {
                   new Chart(categoryCtx, {
                       type: 'doughnut',
                       data: {
                           labels: Object.keys(data.categories),
                           datasets: [{
                               data: Object.values(data.categories),
                               backgroundColor: [
                                   '#2563EB', '#059669', '#D97706', '#DC2626', '#0891B2',
                                   '#7C3AED', '#DB2777', '#EA580C', '#16A34A', '#6B7280', '#9CA3AF'
                               ],
                               borderWidth: 0
                           }]
                       },
                       options: {
                           responsive: true,
                           maintainAspectRatio: false,
                           plugins: { legend: { position: 'bottom', labels: { padding: 16, font: { size: 12 } } } },
                           cutout: '65%'
                       }
                   });

                   new Chart(statusCtx, {
                       type: 'doughnut',
                       data: {
                           labels: Object.keys(data.statuses),
                           datasets: [{
                               data: Object.values(data.statuses),
                               backgroundColor: ['#9CA3AF', '#0891B2', '#D97706', '#059669', '#DC2626'],
                               borderWidth: 0
                           }]
                       },
                       options: {
                           responsive: true,
                           maintainAspectRatio: false,
                           plugins: { legend: { position: 'bottom', labels: { padding: 16, font: { size: 12 } } } },
                           cutout: '65%'
                       }
                   });
               });
       }
   });
   ```

4. Add CSS in `static/css/style.css`:
   - `.chart-card` — height 300px, position relative
   - `.chart-card canvas` — max-height 250px
   - Admin stat cards: distinct from student (darker brand accent)
   - Mobile: charts stack, stat cards 1-col <576px, 2-col 576-767px, 3-col 768-991px, 5-col ≥992px

## What not to do

- Do not implement complaints management list yet
- Do not implement complaint detail/edit yet
- Do not add bar/line charts (doughnut only for V1)
- Do not add date range filters for charts

## Done when

- Admin login → `/admin/dashboard` shows 5 stat cards with correct counts
- Two doughnut charts render with data from `/admin/stats` JSON
- Recent complaints table shows 10 latest with student name, category, status, priority
- Charts responsive: side-by-side on desktop, stacked on mobile
- Stat cards responsive grid
- Navbar highlights "Dashboard" active
- All colors match design.md (status colors for status chart, distinct colors for category chart)

## Verification steps

- [ ] `/admin/dashboard` route with `@admin_required`
- [ ] `/admin/stats` returns JSON with `categories` and `statuses` objects
- [ ] 5 stat cards: Total, New (Submitted), In Progress, Resolved, Critical
- [ ] Stats calculate correctly from DB
- [ ] Two Chart.js doughnut charts render in canvas elements
- [ ] Category chart: 11 segments (or fewer if no data), distinct colors
- [ ] Status chart: 5 segments (Submitted, Under Review, In Progress, Resolved, Rejected) with semantic colors
- [ ] Recent complaints table: ID, Student, Category, Location, Status, Priority, Date, View action
- [ ] "View All" links to `/admin/complaints`
- [ ] Mobile: stat cards stack appropriately, charts stack vertically
- [ ] Navbar "Dashboard" highlighted active
- [ ] No JS errors in console

**Design check:** Admin dashboard follows design.md — 5-card grid with generous spacing, chart cards with 300px height, doughnut charts with 65% cutout, legends at bottom, semantic colors for status chart. Admin navbar distinct from student (darker brand). Mobile stacking works.

## Localhost test before continuing

After this card, the learner should test:

- Start `python app.py`
- Create admin user if not exists (flask shell)
- Login as admin at `/admin/login` → redirect to `/admin/dashboard`
- Verify 5 stat cards show numbers (0 if no data, or counts if sample data exists)
- Verify two doughnut charts render (empty if no data, but canvas present)
- Check `/admin/stats` JSON endpoint directly — returns valid JSON
- Mobile view: stat cards stack, charts stack
- Navbar "Dashboard" highlighted

If all tests pass, reply `continue`.
If anything fails, reply `fix` and paste the error or describe what you see.

## Stop condition

If Chart.js fails to load (CDN blocked, CSP, JS error), stop and fix chart initialization before continuing.

## Status

Not started