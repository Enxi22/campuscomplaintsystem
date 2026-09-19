# --- IMPORTS ---
import os
import uuid
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from PIL import Image

# --- CONFIG ---
from config import Config

# --- EXTENSIONS ---
from models import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- MODELS ---
from models import User, Complaint, CATEGORIES, STATUSES, PRIORITIES, ROLES

# --- CONSTANTS ---
# Constants imported from models.py

# --- HELPERS ---
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_complaint_image(file):
    if not file or not allowed_file(file.filename):
        return None
    # Verify MIME type
    file.seek(0)
    try:
        img = Image.open(file)
        img.verify()
        file.seek(0)
    except Exception:
        return None
    # Generate secure filename
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return f"uploads/complaints/{filename}"

# --- AUTH ---
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_student():
            flash('Student access required.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Admin access required.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_student():
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password) and user.is_student():
            login_user(user, remember=remember)
            flash('Welcome back!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('student/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        errors = []
        
        if len(username) < 3:
            errors.append('Username must be at least 3 characters.')
        if not email or '@' not in email:
            errors.append('Please enter a valid email address.')
        if len(password) < 8:
            errors.append('Password must be at least 8 characters.')
        if password != confirm_password:
            errors.append('Passwords do not match.')
        
        if User.query.filter_by(username=username).first():
            errors.append('Username already taken.')
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered.')
        
        if errors:
            for error in errors:
                flash(error, 'error')
        else:
            user = User(username=username, email=email, role='student')
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    
    return render_template('student/register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin_dashboard'))
        else:
            logout_user()
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password) and user.is_admin():
            login_user(user, remember=remember)
            flash('Welcome to Admin Dashboard!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials.', 'error')
    
    return render_template('admin/login.html')


@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin_login'))


@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_student():
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('admin_dashboard'))
    return redirect(url_for('login'))

# --- STUDENT ROUTES ---

@app.route('/dashboard')
@login_required
@student_required
def dashboard():
    my_complaints = Complaint.query.filter_by(user_id=current_user.id).order_by(Complaint.created_at.desc()).all()
    
    total = len(my_complaints)
    pending = len([c for c in my_complaints if c.status in ['Submitted', 'Under Review']])
    in_progress = len([c for c in my_complaints if c.status == 'In Progress'])
    resolved = len([c for c in my_complaints if c.status == 'Resolved'])
    
    recent_complaints = my_complaints[:5]
    
    stats = {
        'total': total,
        'pending': pending,
        'in_progress': in_progress,
        'resolved': resolved
    }
    
    return render_template('student/dashboard.html', stats=stats, recent_complaints=recent_complaints)


@app.route('/submit', methods=['GET', 'POST'], endpoint='submit_complaint')
@login_required
@student_required
def submit_complaint():
    if request.method == 'POST':
        category = request.form.get('category', '').strip()
        location = request.form.get('location', '').strip()
        description = request.form.get('description', '').strip()
        image_file = request.files.get('image')
        
        errors = []
        
        if not category:
            errors.append('Category is required.')
        elif category not in CATEGORIES:
            errors.append('Invalid category selected.')
        
        if not location:
            errors.append('Location is required.')
        elif len(location) > 200:
            errors.append('Location must be 200 characters or less.')
        
        if not description:
            errors.append('Description is required.')
        elif len(description) < 20:
            errors.append('Description must be at least 20 characters.')
        
        image_path = None
        if image_file and image_file.filename:
            image_path = save_complaint_image(image_file)
            if image_path is None:
                errors.append('Invalid file type. Allowed: PNG, JPG, JPEG, WebP')
        
        if errors:
            for error in errors:
                flash(error, 'error')
        else:
            complaint = Complaint(
                user_id=current_user.id,
                category=category,
                location=location,
                description=description,
                image_path=image_path,
                status='Submitted',
                priority='Medium'
            )
            db.session.add(complaint)
            db.session.commit()
            flash('Complaint submitted successfully!', 'success')
            return redirect(url_for('my_complaints'))
    
    return render_template('student/submit.html', categories=CATEGORIES)


@app.route('/complaints', endpoint='my_complaints')
@login_required
@student_required
def my_complaints():
    complaints = Complaint.query.filter_by(user_id=current_user.id).order_by(Complaint.created_at.desc()).all()
    return render_template('student/complaints.html', complaints=complaints)


@app.route('/complaint/<int:complaint_id>')
@login_required
@student_required
def complaint_detail(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    if complaint.user_id != current_user.id:
        abort(403)
    return render_template('student/complaint_detail.html', complaint=complaint)


# --- ADMIN ROUTES ---

from sqlalchemy import func

@app.route('/admin/dashboard', endpoint='admin_dashboard')
@login_required
@admin_required
def admin_dashboard():
    all_complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
    
    total = len(all_complaints)
    new_count = len([c for c in all_complaints if c.status == 'Submitted'])
    in_progress_count = len([c for c in all_complaints if c.status in ['Under Review', 'In Progress']])
    resolved_count = len([c for c in all_complaints if c.status == 'Resolved'])
    critical_count = len([c for c in all_complaints if c.priority == 'Critical'])
    
    recent_complaints = all_complaints[:10]
    
    stats = {
        'total': total,
        'new': new_count,
        'in_progress': in_progress_count,
        'resolved': resolved_count,
        'critical': critical_count
    }
    
    return render_template('admin/dashboard.html', stats=stats, recent_complaints=recent_complaints)


@app.route('/admin/stats')
@login_required
@admin_required
def admin_stats():
    # Category distribution
    category_data = db.session.query(Complaint.category, func.count(Complaint.id)).group_by(Complaint.category).all()
    categories = {cat: count for cat, count in category_data}
    
    # Status distribution
    status_data = db.session.query(Complaint.status, func.count(Complaint.id)).group_by(Complaint.status).all()
    statuses = {status: count for status, count in status_data}
    
    # Ensure all categories/statuses are present (0 if missing)
    for cat in CATEGORIES:
        if cat not in categories:
            categories[cat] = 0
    for status in STATUSES:
        if status not in statuses:
            statuses[status] = 0
    
    return {'categories': categories, 'statuses': statuses}


@app.route('/admin/statistics', endpoint='admin_statistics')
@login_required
@admin_required
def admin_statistics():
    from sqlalchemy import func
    # Category distribution
    category_data = db.session.query(Complaint.category, func.count(Complaint.id)).group_by(Complaint.category).all()
    categories = {cat: count for cat, count in category_data}
    for cat in CATEGORIES:
        if cat not in categories:
            categories[cat] = 0
    
    # Status distribution
    status_data = db.session.query(Complaint.status, func.count(Complaint.id)).group_by(Complaint.status).all()
    statuses = {status: count for status, count in status_data}
    for status in STATUSES:
        if status not in statuses:
            statuses[status] = 0
    
    # Priority distribution
    priority_data = db.session.query(Complaint.priority, func.count(Complaint.id)).group_by(Complaint.priority).all()
    priorities = {p: count for p, count in priority_data}
    for p in PRIORITIES:
        if p not in priorities:
            priorities[p] = 0
    
    # Total stats
    total = Complaint.query.count()
    by_student = db.session.query(User.username, func.count(Complaint.id)).join(Complaint).group_by(User.username).all()
    
    return render_template('admin/statistics.html', 
                           categories=categories, statuses=statuses, priorities=priorities,
                           total=total, by_student=by_student)


@app.route('/admin/complaints', endpoint='admin_complaints')
@login_required
@admin_required
def admin_complaints():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    q = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    status = request.args.get('status', '').strip()
    priority = request.args.get('priority', '').strip()
    
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
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    complaints = pagination.items
    
    return render_template('admin/complaints.html', 
                           pagination=pagination, 
                           complaints=complaints,
                           q=q, category=category, status=status, priority=priority,
                           CATEGORIES=CATEGORIES, STATUSES=STATUSES, PRIORITIES=PRIORITIES)


@app.route('/admin/complaint/<int:complaint_id>', endpoint='admin_complaint_detail', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_complaint_detail(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    
    if request.method == 'POST':
        new_status = request.form.get('status', '').strip()
        new_priority = request.form.get('priority', '').strip()
        admin_remarks = request.form.get('admin_remarks', '').strip()
        
        errors = []
        
        if new_status not in STATUSES:
            errors.append('Invalid status selected.')
        if new_priority not in PRIORITIES:
            errors.append('Invalid priority selected.')
        
        if errors:
            for error in errors:
                flash(error, 'error')
        else:
            complaint.status = new_status
            complaint.priority = new_priority
            complaint.admin_remarks = admin_remarks if admin_remarks else None
            complaint.updated_at = datetime.utcnow()
            db.session.commit()
            flash('Complaint updated successfully!', 'success')
            return redirect(url_for('admin_complaint_detail', complaint_id=complaint.id))
    
    return render_template('admin/complaint_detail.html', complaint=complaint, STATUSES=STATUSES, PRIORITIES=PRIORITIES)


# --- ERROR HANDLERS ---

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


# --- MAIN ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)