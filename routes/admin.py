from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from models import db, Complaint, User
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    stats = {
        'total': Complaint.query.count(),
        'pending': Complaint.query.filter_by(status='pending').count(),
        'under_review': Complaint.query.filter_by(status='under_review').count(),
        'in_progress': Complaint.query.filter_by(status='in_progress').count(),
        'resolved': Complaint.query.filter_by(status='resolved').count(),
        'rejected': Complaint.query.filter_by(status='rejected').count(),
        'users': User.query.filter_by(is_admin=False).count(),
        'critical': Complaint.query.filter_by(urgency='critical').count(),
    }
    recent = Complaint.query.order_by(Complaint.created_at.desc()).limit(8).all()
    category_stats = db.session.query(Complaint.category, func.count(Complaint.id)).group_by(Complaint.category).all()
    urgency_stats = db.session.query(Complaint.urgency, func.count(Complaint.id)).group_by(Complaint.urgency).all()
    return render_template('admin/dashboard.html', stats=stats, recent_complaints=recent,
                           category_stats=category_stats, urgency_stats=urgency_stats)

@admin_bp.route('/complaints')
@login_required
@admin_required
def all_complaints():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    category_filter = request.args.get('category', '')
    urgency_filter = request.args.get('urgency', '')
    query = Complaint.query
    if status_filter: query = query.filter_by(status=status_filter)
    if category_filter: query = query.filter_by(category=category_filter)
    if urgency_filter: query = query.filter_by(urgency=urgency_filter)
    complaints = query.order_by(Complaint.created_at.desc()).paginate(page=page, per_page=15, error_out=False)
    categories = [c[0] for c in db.session.query(Complaint.category).distinct().all()]
    return render_template('admin/all_complaints.html', complaints=complaints,
                           status_filter=status_filter, category_filter=category_filter,
                           urgency_filter=urgency_filter, categories=categories)

@admin_bp.route('/complaint/<int:cid>', methods=['GET', 'POST'])
@login_required
@admin_required
def complaint_detail(cid):
    complaint = Complaint.query.get_or_404(cid)
    if request.method == 'POST':
        new_status = request.form.get('status')
        if new_status in Complaint.STATUS_CHOICES:
            complaint.status = new_status
            complaint.admin_notes = request.form.get('admin_notes', '')
            db.session.commit()
            flash('Complaint updated successfully.', 'success')
        return redirect(url_for('admin.complaint_detail', cid=cid))
    return render_template('admin/complaint_detail.html', complaint=complaint,
                           statuses=Complaint.STATUS_CHOICES)
