# Work Card 08 — Admin Complaints Management

## Goal

Build admin complaints list with search, filter (category/status/priority), pagination, and sortable table.

## Inputs

- `build-blueprint.md` (Admin Routes, Implementation Rules)
- `architecture.md` (Admin Routes: `/admin/complaints`)
- `design.md` (Component Style - Tables, Search/Filter, Pagination, Mobile Rules)

## Files likely touched

- `app.py` — `/admin/complaints` route with query params
- `templates/admin/complaints.html` — new
- `static/css/style.css` — filter toolbar, pagination, mobile card list
- `static/js/main.js` — filter form handling (optional, can be server-side only)

## Instructions for the coding agent

1. Add route in `app.py`:
   - `@app.route('/admin/complaints')` with `@login_required` + `@admin_required`
   - Query params: `page` (default 1), `per_page` (10), `q` (search), `category`, `status`, `priority`
   - Build query:
     ```python
     query = Complaint.query.join(User).order_by(Complaint.created_at.desc())
     if q:
         query = query.filter(
             Complaint.description.ilike(f'%{q}%') |
             Complaint.location.ilike(f'%{q}%') |
             User.username.ilike(f'%{q}%')
         )
     if category:
         query = query.filter(Complaint.category == category)
     if status:
         query = query.filter(Complaint.status == status)
     if priority:
         query = query.filter(Complaint.priority == priority)
     pagination = query.paginate(page=page, per_page=10, error_out=False)
     ```
   - Pass `pagination`, `complaints`, and filter values to template
   - Preserve filters in pagination links

2. Create `templates/admin/complaints.html` extending `admin/base.html`:
   - Page title: "Complaints Management"
   - **Filter Toolbar Card**:
     - Search input: `q` (placeholder "Search description, location, student...")
     - Category dropdown: all CATEGORIES + "All Categories"
     - Status dropdown: all STATUSES + "All Statuses"
     - Priority dropdown: all PRIORITIES + "All Priorities"
     - Submit button (Primary), Clear button (Secondary, resets to defaults)
     - Form method GET, preserves current filters
   - **Results Card**:
     - Header: "Showing X to Y of Z complaints"
     - Table (desktop ≥ 768px):
       - Columns: ID, Student, Category, Location, Status, Priority, Date, Actions
       - Student: username (text)
       - Status: badge with `complaint.status_badge_class()`
       - Priority: badge with `complaint.priority_badge_class()`
       - Actions: "View" button → `/admin/complaint/<id>`
     - Mobile Card List (< 768px):
       - Each complaint as card with labeled fields: ID, Student, Category, Location, Status, Priority, Date
       - "View" button at bottom
     - Empty state: "No complaints match your filters." + Clear filters button
   - **Pagination** (below table/cards):
     - Previous/Next, page numbers (max 5 visible), ellipsis
     - Preserves all filter query params

3. Add CSS in `static/css/style.css`:
   - `.filter-toolbar` — flex wrap, gap, aligned inputs
   - `.filter-toolbar select, .filter-toolbar input` — min-width 180px, flex-1
   - `.complaint-mobile-card` — for < 768px, card with labeled rows
   - `.pagination` — Bootstrap-style, current page highlighted
   - Mobile: filter toolbar stacks, table → card list

## What not to do

- Do not implement complaint detail/edit yet
- Do not add column sorting (created_at desc only for V1)
- Do not add bulk actions
- Do not add export

## Done when

- `/admin/complaints` shows filter toolbar with all 4 controls
- Search works across description, location, student username
- Category/Status/Priority filters work individually and combined
- Pagination works (10 per page) with preserved filters
- Table renders on desktop, card list on mobile
- "View" links to `/admin/complaint/<id>` (404 expected)
- Clear filters resets all controls
- Empty state shows when no results

## Verification steps

- [ ] `/admin/complaints` route with `@admin_required`
- [ ] Filter toolbar: search input, 3 dropdowns (category/status/priority), submit/clear buttons
- [ ] Search filters by description, location, student username (case-insensitive)
- [ ] Category filter uses CATEGORIES constant
- [ ] Status filter uses STATUSES constant
- [ ] Priority filter uses PRIORITIES constant
- [ ] Filters combine (AND logic)
- [ ] Pagination: 10 per page, prev/next, page numbers, preserves filters in URL
- [ ] Desktop ≥ 768px: table with 8 columns
- [ ] Mobile < 768px: card list with labeled fields
- [ ] Status/priority badges use correct semantic colors
- [ ] "View" button links to `/admin/complaint/<id>`
- [ ] Empty state with "Clear filters" when no results
- [ ] Navbar "Complaints" highlighted active
- [ ] URL reflects current filters (shareable/bookmarkable)

**Design check:** Filter toolbar follows design.md — organized controls, adequate spacing, clear labels, primary submit button. Table: 48px rows, striped, hover, badges with text+color. Mobile card list: each field labeled, no horizontal scroll. Pagination accessible (aria-labels).

## Localhost test before continuing

After this card, the learner should test:

- Start `python app.py`
- Login as admin → go to `/admin/complaints`
- Verify filter toolbar renders with all dropdowns populated
- Test search: enter partial description → results filter
- Test category filter: select "Electrical" → only electrical complaints
- Test status filter: select "In Progress" → only in progress
- Test priority filter: select "Critical" → only critical
- Test combined filters: category + status + priority
- Test pagination: create >10 complaints (or reduce per_page for testing) → verify page links work, filters preserved
- Test mobile view: table → card list, filter toolbar stacks
- Clear filters button resets all

If all tests pass, reply `continue`.
If anything fails, reply `fix` and paste the error or describe what you see.

## Stop condition

If pagination loses filter params on page change, stop and fix URL building in template before continuing.

## Status

Not started