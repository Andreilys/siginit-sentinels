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
    # Query intelligence data directly
    intel_data = IntelligenceData.query.order_by(IntelligenceData.timestamp.desc()).all()
    
    # Calculate Admiralty scores and assign priorities
    alerts_data = []
    for intel in intel_data:
        # Calculate Admiralty score
        reliability_scores = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1, 'F': 0}
        credibility_scores = {'ONE': 5, 'TWO': 4, 'THREE': 3, 'FOUR': 2, 'FIVE': 1, 'SIX': 0}
        
        rel_score = reliability_scores.get(intel.source_reliability.name, 0)
        cred_score = credibility_scores.get(intel.info_credibility.name, 0)
        admiralty_score = ((rel_score + cred_score) / 10)  # 0 to 1 scale
        
        # Assign priority based on Admiralty score
        if admiralty_score >= 0.7:
            priority = 'high'
        elif admiralty_score >= 0.4:
            priority = 'medium'
        else:
            priority = 'low'
            
        alerts_data.append({
            'intel': intel,
            'admiralty_score': admiralty_score,
            'priority': priority
        })
    
    return render_template('alerts.html', alerts=alerts_data)

@main_bp.route('/reports')
@login_required
def reports():
    return render_template('reports.html')

def calculate_threat_level():
    # Simple threat level calculation based on recent high-priority alerts
    high_priority_count = Alert.query.filter_by(priority=1).count()
    return min(high_priority_count * 20, 100)  # 20% per high-priority alert, max 100%
