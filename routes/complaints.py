from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Complaint
from ai_utils import analyze_complaint

complaints_bp = Blueprint('complaints', __name__)

@complaints_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin.dashboard'))
    complaints = Complaint.query.filter_by(user_id=current_user.id).order_by(Complaint.created_at.desc()).all()
    stats = {
        'total': len(complaints),
        'pending': sum(1 for c in complaints if c.status == 'pending'),
        'in_progress': sum(1 for c in complaints if c.status == 'in_progress'),
        'resolved': sum(1 for c in complaints if c.status == 'resolved'),
    }
    return render_template('dashboard.html', recent_complaints=complaints[:5], stats=stats)

@complaints_bp.route('/submit', methods=['GET', 'POST'])
@login_required
def submit_complaint():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        location = request.form.get('location', '').strip()
        if not title or not description:
            flash('Title and description are required.', 'error')
            return render_template('submit_complaint.html')
        analysis = analyze_complaint(title, description)
        complaint = Complaint(
            user_id=current_user.id, title=title, description=description,
            location=location, category=analysis['category'],
            urgency=analysis['urgency'], sentiment_score=analysis['sentiment_score']
        )
        db.session.add(complaint)
        db.session.commit()
        flash(f'✅ Complaint submitted! AI detected: Category — {analysis["category"]} | Urgency — {analysis["urgency"].title()}', 'success')
        return redirect(url_for('complaints.my_complaints'))
    return render_template('submit_complaint.html', categories=Complaint.CATEGORY_CHOICES)

@complaints_bp.route('/my-complaints')
@login_required
def my_complaints():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    query = Complaint.query.filter_by(user_id=current_user.id)
    if status_filter:
        query = query.filter_by(status=status_filter)
    complaints = query.order_by(Complaint.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('my_complaints.html', complaints=complaints, status_filter=status_filter)

@complaints_bp.route('/track/<int:complaint_id>')
@login_required
def track_complaint(complaint_id):
    complaint = Complaint.query.filter_by(id=complaint_id, user_id=current_user.id).first_or_404()
    return render_template('track_status.html', complaint=complaint)

@complaints_bp.route('/chatbot')
@login_required
def chatbot_page():
    return render_template('chatbot.html')

@complaints_bp.route('/api/chat', methods=['POST'])
@login_required
def chat_api():
    from chatbot.chatbot import process_message
    data = request.get_json(silent=True) or {}
    message = data.get('message', '')
    step = int(data.get('step', 0))
    session_data = data.get('session_data', {})
    result = process_message(message, step, session_data)
    if result.get('done') and result.get('complaint_data'):
        cd = result['complaint_data']
        analysis = analyze_complaint(cd.get('title', ''), cd.get('description', ''))
        complaint = Complaint(
            user_id=current_user.id,
            title=cd.get('title', 'Chatbot Complaint'),
            description=cd.get('description', ''),
            location=cd.get('location', ''),
            category=cd.get('category') or analysis['category'],
            urgency=analysis['urgency'],
            sentiment_score=analysis['sentiment_score']
        )
        db.session.add(complaint)
        db.session.commit()
        result['complaint_id'] = complaint.id
    return jsonify(result)
