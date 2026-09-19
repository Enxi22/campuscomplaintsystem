# Project Brief

## Project Identity

Smart Campus Complaint System

## One-Sentence Concept

A full-stack web application where students submit campus complaints with categories/locations/images, track status via complaint ID, and admins manage complaints through a dashboard with filtering, status updates, priorities, remarks, and analytics.

## Target User

- **Students** — submit and track campus complaints
- **Admins** — manage all complaints, view statistics, update status/priority/remarks

## User Goal

- **Students:** Register, login, submit complaints (category, location, description, optional image), receive complaint ID, view/track their complaints, receive status updates
- **Admins:** Login to dashboard, view all complaints, search/filter, view details, change status, set priority, add remarks, view statistics (total, new, in-progress, resolved, critical, by category/status)

## Build Shape

Full-stack web application (Python Flask + SQLite + Bootstrap) — requires authentication, database, backend, file uploads, role-based access, admin system. Exceeds KDBM Lite browser-only guardrails; planning only per learner choice.

## Shape Confirmation

Confirmed — learner chose to proceed with planning phase for full stack implementation.

## Version-One Success

Complete planning documents: project-brief.md, architecture.md, design.md, build-blueprint.md, work-cards/*.md — ready for Flask/SQLite implementation.

## Now / Later / Never

### Now

All planning documents (this phase)

### Later

Full Flask implementation: database schema, authentication, student/admin UI, complaint CRUD, image upload, search/filter, statistics dashboard, sample data

### Never

Real-time notifications, email/SMS alerts, mobile app, multi-campus support, advanced analytics, payment integration

## Assumptions

- Local development in VS Code with Python Flask + SQLite
- Bootstrap 5 for responsive UI
- Password hashing (werkzeug.security or bcrypt)
- Role-based access control (student vs admin)
- Sample/demo data for testing
- Complaint categories: Classroom, Furniture, Electrical, Water/Plumbing, Internet/Wi-Fi, Cleanliness, Parking, Security, Campus Facilities, Library, Other
- Complaint statuses: Submitted, Under Review, In Progress, Resolved, Rejected
- Priorities: Low, Medium, High, Critical

## Proof Target

Working local Flask app with complete student/admin flows, verified in browser

## Trainer / Learner Notes

Planning phase only — implementation starts after build-blueprint.md and work-cards are generated and learner says "Start Work Card 01"