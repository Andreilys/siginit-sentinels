from flask import Blueprint, render_template
from flask_login import login_required
from models import Alert, IntelligenceData

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/dashboard')
@login_required
def dashboard():
    alerts = Alert.query.order_by(Alert.timestamp.desc()).limit(5).all()
    threat_level = calculate_threat_level()
    return render_template('dashboard.html', alerts=alerts, threat_level=threat_level)

@main_bp.route('/alerts')
@login_required
def alerts():
    alerts = Alert.query.order_by(Alert.timestamp.desc()).all()
    return render_template('alerts.html', alerts=alerts)

@main_bp.route('/reports')
@login_required
def reports():
    return render_template('reports.html')

def calculate_threat_level():
    # Simple threat level calculation based on recent high-priority alerts
    high_priority_count = Alert.query.filter_by(priority=1).count()
    return min(high_priority_count * 20, 100)  # 20% per high-priority alert, max 100%
