from app import app, db
from models import User, Complaint, CATEGORIES, STATUSES, PRIORITIES
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

with app.app_context():
    # Admin - check if exists
    admin = User.query.filter_by(email='admin@campus.edu').first()
    if not admin:
        admin = User(username='admin', email='admin@campus.edu', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        print("Created admin user")
    else:
        print("Admin user already exists")

    # Students - check if exist
    students = []
    for i in range(1, 4):
        email = f'student{i}@campus.edu'
        u = User.query.filter_by(email=email).first()
        if not u:
            u = User(username=f'student{i}', email=email, role='student')
            u.set_password('student123')
            db.session.add(u)
            print(f"Created student{i}")
        students.append(u)
    db.session.commit()

    # Complaints - check if any exist
    existing_complaints = Complaint.query.count()
    if existing_complaints == 0:
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
        print(f"Created {len(sample_complaints)} sample complaints")
    else:
        print(f"Complaints already exist ({existing_complaints} found)")
    
    print("Sample data seeding complete!")