from flask import Blueprint, jsonify, request
from flask_login import login_required
from models import Alert, IntelligenceData
from app import db

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/intel-points')
@login_required
def get_intel_points():
    query = IntelligenceData.query.filter(
        IntelligenceData.latitude.isnot(None),
        IntelligenceData.longitude.isnot(None)
    )
    
    if intel_type := request.args.get('type'):
        query = query.filter(IntelligenceData.intel_type == intel_type)
    if subtype := request.args.get('subtype'):
        query = query.filter(IntelligenceData.intel_subtype == subtype)
    if reliability := request.args.get('reliability'):
        query = query.filter(IntelligenceData.source_reliability == reliability)
    if credibility := request.args.get('credibility'):
        query = query.filter(IntelligenceData.info_credibility == credibility)
    
    intel_data = query.all()
    
    return jsonify([{
        'latitude': point.latitude,
        'longitude': point.longitude,
        'title': point.source,
        'source': point.source,
        'timestamp': point.timestamp.isoformat(),
        'priority': get_priority(point),
        'credibility_score': point.credibility_score,
        'content': point.content,
        'intel_type': point.intel_type.name if point.intel_type else None,
        'intel_subtype': point.intel_subtype or 'Unknown',
        'source_reliability': point.source_reliability.name if point.source_reliability else None,
        'info_credibility': point.info_credibility.name if point.info_credibility else None
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

from models import IntelType, IntelligenceData, Alert, SourceReliability, InfoCredibility

@api_bp.route('/statistics')
@login_required
def get_statistics():
    # Get count of alerts by priority
    high_priority = Alert.query.filter_by(priority=1).count()
    medium_priority = Alert.query.filter_by(priority=2).count()
    low_priority = Alert.query.filter_by(priority=3).count()
    
    # Get count by intel type and subtype
    intel_types = {}
    for intel_type in IntelType:
        type_count = IntelligenceData.query.filter_by(intel_type=intel_type).count()
        subtypes = db.session.query(
            IntelligenceData.intel_subtype,
            db.func.count(IntelligenceData.id)
        ).filter_by(intel_type=intel_type).group_by(
            IntelligenceData.intel_subtype
        ).all()
        
        intel_types[intel_type.name] = {
            'total': type_count,
            'subtypes': {subtype: count for subtype, count in subtypes}
        }
    
    # Get source reliability distribution
    reliability_counts = db.session.query(
        IntelligenceData.source_reliability,
        db.func.count(IntelligenceData.id)
    ).group_by(IntelligenceData.source_reliability).all()
    
    # Get info credibility distribution
    credibility_counts = db.session.query(
        IntelligenceData.info_credibility,
        db.func.count(IntelligenceData.id)
    ).group_by(IntelligenceData.info_credibility).all()
    
    return jsonify({
        'highPriority': high_priority,
        'mediumPriority': medium_priority,
        'lowPriority': low_priority,
        'intelTypes': intel_types,
        'sourceReliability': {rel[0].name: rel[1] for rel in reliability_counts},
        'infoCredibility': {cred[0].name: cred[1] for cred in credibility_counts}
    })