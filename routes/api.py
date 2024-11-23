from flask import Blueprint, jsonify
from flask_login import login_required
from models import Alert, IntelligenceData
from app import db

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/intel-points')
@login_required
def get_intel_points():
    intel_data = IntelligenceData.query.filter(
        IntelligenceData.latitude.isnot(None),
        IntelligenceData.longitude.isnot(None)
    ).all()
    
    return jsonify([{
        'latitude': point.latitude,
        'longitude': point.longitude,
        'title': point.source,
        'source': point.source,
        'timestamp': point.timestamp.isoformat(),
        'priority': get_priority(point),
        'credibility_score': point.credibility_score,
        'content': point.content
    } for point in intel_data])

@api_bp.route('/threat-level')
@login_required
def get_threat_level():
    # Calculate current threat level
    high_priority = Alert.query.filter_by(priority=1).count()
    medium_priority = Alert.query.filter_by(priority=2).count()
    
    threat_level = min((high_priority * 20 + medium_priority * 10), 100)
    return jsonify({'level': threat_level})

@api_bp.route('/alerts/<int:alert_id>/acknowledge', methods=['POST'])
@login_required
def acknowledge_alert(alert_id):
    alert = Alert.query.get_or_404(alert_id)
    alert.status = 'acknowledged'
    db.session.commit()
    return jsonify({'success': True})

@api_bp.route('/alerts/<int:alert_id>/resolve', methods=['POST'])
@login_required
def resolve_alert(alert_id):
    alert = Alert.query.get_or_404(alert_id)
    alert.status = 'resolved'
    db.session.commit()
    return jsonify({'success': True})

@api_bp.route('/alerts/<int:alert_id>/details')
@login_required
def get_alert_details(alert_id):
    alert = Alert.query.get_or_404(alert_id)
    intel = IntelligenceData.query.get(alert.intel_id)
    return jsonify({
        'alert': {
            'id': alert.id,
            'title': alert.title,
            'description': alert.description,
            'priority': alert.priority,
            'status': alert.status
        },
        'intel': {
            'source': intel.source,
            'content': intel.content,
            'timestamp': intel.timestamp.isoformat(),
            'credibility_score': intel.credibility_score,
            'language': intel.language,
            'latitude': intel.latitude,
            'longitude': intel.longitude
        } if intel else None
    })

def get_priority(intel_data):
    # Determine priority based on credibility score
    if intel_data.credibility_score >= 0.8:
        return 1
    elif intel_data.credibility_score >= 0.5:
        return 2
    return 3
