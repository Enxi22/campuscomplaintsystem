# Work Card 10 — Sample Data & Polish

## Goal

Create sample data seeder, error pages, empty states, loading states, and perform final mobile/responsive verification.

## Inputs

- `build-blueprint.md` (Proof Ladder, Sample Data, File and Folder Expectations)
- `architecture.md` (Sample data requirements)
- `design.md` (Anti-Slop Rules, Empty States, Loading States, Mobile Rules, Design Verification Checklist)

## Files likely touched

- `sample_data.py` — new
- `templates/404.html` — new
- `templates/500.html` — new
- `templates/student/complaints.html` — enhance empty state
- `templates/student/complaint_detail.html` — loading state
- `templates/admin/complaints.html` — empty state
- `templates/admin/dashboard.html` — empty charts handling
- `static/css/style.css` — skeleton loaders, empty state styles
- `static/js/main.js` — form loading states, toast improvements

## Instructions for the coding agent

1. Create `sample_data.py`:
   ```python
   from app import app, db
   from models import User, Complaint, CATEGORIES, STATUSES, PRIORITIES
   from werkzeug.security import generate_password_hash
   from datetime import datetime, timedelta
   import random

   with app.app_context():
       # Admin
       admin = User(username='admin', email='admin@campus.edu', role='admin')
       admin.set_password('admin123')
       db.session.add(admin)

       # Students
       students = []
       for i in range(1, 4):
           u = User(username=f'student{i}', email=f'student{i}@campus.edu', role='student')
           u.set_password('student123')
           db.session.add(u)
           students.append(u)
       db.session.commit()

       # Complaints
       sample_complaints = [
           {'category': 'Electrical', 'location': 'Library, 2nd Floor', 'description': 'Lights flickering in study area near windows.', 'status': 'Resolved', 'priority': 'High', 'remarks': 'Replaced faulty ballast.', 'days_ago': 5},
           {'category': 'Water / Plumbing', 'location': 'Building A, Restroom 101', 'description': 'Toilet continuously running, wasting water.', 'status': 'In Progress', 'priority': 'Medium', 'remarks': 'Plumber scheduled for tomorrow.', 'days_ago': 2},
           {'category': 'Internet / Wi-Fi', 'location': 'Student Center', 'description': 'Wi-Fi signal weak, frequent disconnections.', 'status': 'Under Review', 'priority': 'High', 'remarks': 'IT team investigating access point.', 'days_ago': 1},
           {'category': 'Furniture', 'location': 'Classroom 204', 'description': 'Three chairs have broken wheels.', 'status': 'Submitted', 'priority': 'Low', 'remarks': '', 'days_ago': 0},
           {'category': 'Cleanliness', 'location': 'Cafeteria', 'description': 'Tables not cleaned between lunch rushes.', 'status': 'Submitted', 'priority': 'Medium', 'remarks': '', 'days_ago': 0},
           {'category': 'Security', 'location': 'Parking Lot B', 'description': 'Emergency call button not working.', 'status': 'Resolved', 'priority': 'Critical', 'remarks': 'Replaced button unit, tested OK.', 'days_ago': 10},
           {'category': 'Classroom', 'location': 'Lecture Hall 1', 'description': 'Projector not displaying HDMI input.', 'status': 'In Progress', 'priority': 'High', 'remarks': 'Projector bulb replaced.', 'days_ago': 3},
           {'category': 'Campus Facilities', 'location': 'Main Entrance', 'description': 'Automatic door sensor failing.', 'status': 'Under Review', 'priority': 'Medium', 'remarks': 'Facilities notified.', 'days_ago': 1},
           {'category': 'Library', 'location': 'Quiet Study Room', 'description': 'Air conditioning too cold.', 'status': 'Submitted', 'priority': 'Low', 'remarks': '', 'days_ago': 0},
           {'category': 'Other', 'location': 'Sports Complex', 'description': 'Treadmill making grinding noise.', 'status': 'Rejected', 'priority': 'Low', 'remarks': 'Not campus maintenance responsibility.', 'days_ago': 7},
       ]

       for i, c in enumerate(sample_complaints):
           complaint = Complaint(
               user_id=random.choice(students).id,
               category=c['category'],
               location=c['location'],
               description=c['description'],
               status=c['status'],
               priority=c['priority'],
               admin_remarks=c['remarks'] if c['remarks'] else None,
               created_at=datetime.utcnow() - timedelta(days=c['days_ago']),
               updated_at=datetime.utcnow() - timedelta(days=c['days_ago'])
           )
           db.session.add(complaint)
       db.session.commit()
       print(f"Created admin + 3 students + {len(sample_complaints)} complaints")
   ```

2. Create `templates/404.html` extending `base.html`:
   - Friendly "Page Not Found" with search link back to dashboard

3. Create `templates/500.html` extending `base.html`:
   - "Server Error" with contact admin link

4. Enhance empty states in all list templates:
   - Illustrative icon (Bootstrap Icon: `inbox`, `exclamation-circle`, `search`)
   - Helpful text + primary action button

5. Add skeleton loaders in `static/css/style.css`:
   - `.skeleton` — animation pulse, gray-200 bg
   - `.skeleton-card`, `.skeleton-table-row`, `.skeleton-stat`
   - Apply via JS when fetching (optional for V1, CSS only is fine)

6. Add form loading states in `static/js/main.js`:
   - On form submit: disable button, show spinner, "Saving..."
   - Re-enable on response (success/error)

7. Mobile verification checklist (manual):
   - Test all pages at 375px, 768px, 992px, 1200px
   - Verify no horizontal scroll
   - Verify touch targets ≥ 44px
   - Verify text readable (no zoom needed)
   - Verify tables → card lists on mobile
   - Verify forms stack, buttons full-width
   - Verify charts stack
   - Verify sidebar/nav works (drawer/bottom nav)

## What not to do

- Do not add new features
- Do not modify core logic
- Do not add tests
- Do not add Docker/CI

## Done when

- `python sample_data.py` creates admin (admin/admin123), 3 students (student1-3/student123), 10 complaints across categories/statuses/priorities
- 404/500 pages render correctly
- All empty states show icon + text + CTA
- Form submit shows loading state
- Mobile testing passes at all breakpoints
- Design Verification Checklist (design.md) all items checked

## Verification steps

- [ ] `python sample_data.py` runs without errors, prints success message
- [ ] Admin login: `admin` / `admin123` works
- [ ] Student login: `student1` / `student123` works
- [ ] Admin dashboard shows stats > 0, charts render with data
- [ ] Admin complaints list shows 10 complaints, filters work
- [ ] Student dashboard shows their complaints (3-4 each)
- [ ] Student can submit new complaint, appears in their list
- [ ] Admin can edit any complaint status/priority/remarks
- [ ] 404 page: visit `/nonexistent` → friendly page
- [ ] 500 page: trigger error (temporarily break route) → friendly page
- [ ] Empty states: new student → dashboard shows empty state with CTA
- [ ] Form loading: submit complaint → button shows spinner, disabled
- [ ] Mobile 375px: all pages usable, no horizontal scroll, touch targets ok
- [ ] Mobile 768px: tablet layout works (2-col stats, stacked charts)
- [ ] Design Verification Checklist (design.md) — all 16 items verified

**Design check:** Full design.md checklist verified — colors, spacing, typography, components, mobile, accessibility, anti-slop rules.

## Localhost test before continuing

After this card, the learner should test:

- Run `python sample_data.py` — confirm admin + 3 students + 10 complaints created
- Start `python app.py`
- Login as admin → dashboard shows stats, charts with data
- Admin → complaints list → filter by category "Electrical" → 1 result
- Admin → click complaint → edit status to "Resolved", add remarks → save
- Login as student1 → dashboard shows their complaints
- Student → submit new complaint with image → appears in list
- Visit `/nonexistent` → 404 page
- Mobile test: Chrome DevTools device toolbar → iPhone SE (375px), iPad (768px), Desktop (1200px)
- Verify all Design Verification Checklist items

If all tests pass, reply `continue`.
If anything fails, reply `fix` and paste the error or describe what you see.

## Stop condition

If sample data fails to create (FK constraint, duplicate key), stop and fix sample_data.py before continuing.

## Status

Not started