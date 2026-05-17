from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(300), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    complaints = db.relationship('Complaint', backref='user', lazy=True)

class Complaint(db.Model):
    __tablename__ = 'complaint'
    STATUS_CHOICES = ['pending', 'under_review', 'in_progress', 'resolved', 'rejected']
    URGENCY_CHOICES = ['low', 'medium', 'high', 'critical']
    CATEGORY_CHOICES = [
        'Sanitation','Infrastructure','Water Supply','Electricity',
        'Public Safety','Healthcare','Education','Transportation',
        'Environment','Animal Control','General'
    ]
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False, default='General')
    urgency = db.Column(db.String(20), nullable=False, default='medium')
    status = db.Column(db.String(30), nullable=False, default='pending')
    location = db.Column(db.String(300), nullable=True)
    sentiment_score = db.Column(db.Float, default=0.0)
    admin_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
