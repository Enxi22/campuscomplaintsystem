from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

CATEGORIES = [
    'Classroom', 'Furniture', 'Electrical', 'Water / Plumbing',
    'Internet / Wi-Fi', 'Cleanliness', 'Parking', 'Security',
    'Campus Facilities', 'Library', 'Other'
]

STATUSES = ['Submitted', 'Under Review', 'In Progress', 'Resolved', 'Rejected']

PRIORITIES = ['Low', 'Medium', 'High', 'Critical']

ROLES = ['student', 'admin']


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def is_student(self):
        return self.role == 'student'

    @property
    def is_active(self):
        return True

    def __repr__(self):
        return f'<User {self.username}>'


class Complaint(db.Model):
    __tablename__ = 'complaint'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(300), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Submitted')
    priority = db.Column(db.String(10), nullable=False, default='Medium')
    admin_remarks = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('complaints', lazy=True))

    @property
    def status_badge_class(self):
        mapping = {
            'Submitted': 'badge-secondary',
            'Under Review': 'badge-info',
            'In Progress': 'badge-warning',
            'Resolved': 'badge-success',
            'Rejected': 'badge-danger'
        }
        return mapping.get(self.status, 'badge-secondary')

    @property
    def priority_badge_class(self):
        mapping = {
            'Low': 'badge-secondary',
            'Medium': 'badge-primary',
            'High': 'badge-warning',
            'Critical': 'badge-danger'
        }
        return mapping.get(self.priority, 'badge-secondary')

    def __repr__(self):
        return f'<Complaint {self.id} - {self.category}>'