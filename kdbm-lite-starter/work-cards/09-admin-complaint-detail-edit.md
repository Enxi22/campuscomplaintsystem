# Work Card 09 — Admin Complaint Detail & Edit

## Goal

Build admin complaint detail view with editable status, priority, and admin remarks; save changes with flash confirmation.

## Inputs

- `build-blueprint.md` (Admin Routes: `/admin/complaint/<id>`)
- `architecture.md` (Admin Routes, Complaint Model)
- `design.md` (Component Style - Forms, Badges, Cards, Mobile Rules)

## Files likely touched

- `app.py` — `/admin/complaint/<id>` GET/POST route
- `templates/admin/complaint_detail.html` — new
- `static/css/style.css` — detail layout, form in card, mobile
- `static/js/main.js` — optional: confirm before status change

## Instructions for the coding agent

1. Add route in `app.py`:
   - `@app.route('/admin/complaint/<int:complaint_id>', methods=['GET', 'POST'])` with `@login_required` + `@admin_required`
   - Query: `complaint = Complaint.query.get_or_404(complaint_id)`
   - GET: render detail template
   - POST:
     - Validate `status` in STATUSES, `priority` in PRIORITIES
     - Update `complaint.status`, `complaint.priority`, `complaint.admin_remarks`
     - `complaint.updated_at = datetime.utcnow()`
     - `db.session.commit()`
     - Flash success, redirect to same page (or `/admin/complaints`)

2. Create `templates/admin/complaint_detail.html` extending `admin/base.html`:
   - Page title: "Complaint #{{ complaint.id }}"
   - **Header Card**:
     - Row 1: Complaint ID (large), Category badge, Status badge (current), Priority badge (current)
     - Row 2: Student (username, link to filter), Submitted date, Updated date
   - **Details Card**:
     - Location (with icon)
     - Description (formatted)
     - Image (if exists): clickable to open full-size in new tab
   - **Admin Actions Card** (form):
     - Status: `<select>` with STATUSES, current selected
     - Priority: `<select>` with PRIORITIES, current selected
     - Admin Remarks: `<textarea rows="4">` placeholder "Add remarks for the student...", value = existing remarks
     - Submit button: "Save Changes" (Primary)
     - Cancel button: link to `/admin/complaints` (Secondary)
   - **Status Timeline Card** (read-only):
     - Vertical timeline showing status changes (Submitted → current)
     - If admin_remarks exist at each stage, show in timeline

3. Add CSS in `static/css/style.css`:
   - `.detail-header` — grid layout for ID, badges, meta
   - `.admin-actions-form` — form in card, 20px gap, selects full-width mobile
   - `.timeline-admin` — similar to student but with remark bubbles
   - Mobile: header stacks, form fields full-width, image full-width

## What not to do

- Do not add student notification/email on update
- Do not add audit log (updated_at covers basics)
- Do not restrict status transitions (admin can set any status)
- Do not add "notify student" checkbox

## Done when

- Admin views `/admin/complaint/<id>` → sees full details + edit form
- Status dropdown shows all 5 statuses, current selected
- Priority dropdown shows all 4 priorities, current selected
- Admin remarks textarea shows existing remarks
- Submit → saves to DB, flashes success, redirects to detail (or list)
- Changes persist on refresh
- Status timeline updates to show new status
- Mobile: form usable, image viewable, timeline stacks
- Unauthorized (student) → 403

## Verification steps

- [ ] `/admin/complaint/<id>` GET renders detail with header, details, admin form, timeline
- [ ] Header shows: ID, category badge, status badge, priority badge, student, dates
- [ ] Image displays if exists, clickable for full-size
- [ ] Form: status select (5 options), priority select (4 options), remarks textarea
- [ ] Current values pre-selected/filled
- [ ] POST with valid data → updates DB, flashes success, redirects
- [ ] POST with invalid status/priority → error flash, form re-renders with values
- [ ] Updated status/priority/remarks visible immediately after save
- [ ] Status timeline reflects new status
- [ ] Student cannot access (403)
- [ ] Mobile: form stacks, image scales, timeline vertical
- [ ] Navbar "Complaints" highlighted active

**Design check:** Detail page follows design.md — two-column layout on desktop (info + actions), stacked on mobile. Form in card with subtle background. Status/priority badges use semantic colors. Timeline vertical with connectors. Focus rings on form controls.

## Localhost test before continuing

After this card, the learner should test:

- Start `python app.py`
- Login as admin → go to `/admin/complaints` → click "View" on a complaint
- Verify detail page shows all info
- Change status from "Submitted" to "In Progress", priority to "High", add remarks
- Click "Save Changes" → verify flash success, page reloads with new values
- Refresh page → verify changes persist
- Check timeline shows "In Progress" with remarks
- Try invalid status (manual HTML edit) → verify server rejects
- Mobile view: form stacks, image full-width

If all tests pass, reply `continue`.
If anything fails, reply `fix` and paste the error or describe what you see.

## Stop condition

If DB commit fails (constraint, session), stop and fix transaction handling before continuing.

## Status

Not started