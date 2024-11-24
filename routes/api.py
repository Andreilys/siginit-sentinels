from flask import Blueprint, jsonify, request
from flask_login import login_required
from models import Alert, IntelligenceData, AudioAnalysis
from app import db

# Create the blueprint
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

@api_bp.route('/audio-analysis', methods=['POST'])
def save_audio_analysis():
    data = request.get_json()
    
    # Validate required fields
    if 'file_name' not in data:
        return jsonify({'error': 'file_name is required'}), 400
    
    # Create new audio analysis record
    analysis = AudioAnalysis(
        file_name=data['file_name'],
        transcription=data.get('transcription'),
        translation=data.get('translation'),
        key_insights=data.get('key_insights'),
        keywords=data.get('keywords'),
        locations_mentioned=data.get('locations_mentioned'),
        sentiment_summary=data.get('sentiment_summary'),
        critical_entities=data.get('critical_entities'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude')
    )
    
    # Save to database
    db.session.add(analysis)
    db.session.commit()
    
    return jsonify({
        'id': analysis.id,
        'message': 'Audio analysis saved successfully'
    }), 201

@api_bp.route('/audio-analysis/<int:analysis_id>', methods=['GET'])
def get_audio_analysis(analysis_id):
    analysis = AudioAnalysis.query.get_or_404(analysis_id)
    
    return jsonify({
        'id': analysis.id,
        'file_name': analysis.file_name,
        'transcription': analysis.transcription,
        'translation': analysis.translation,
        'key_insights': analysis.key_insights,
        'keywords': analysis.keywords,
        'locations_mentioned': analysis.locations_mentioned,
        'sentiment_summary': analysis.sentiment_summary,
        'critical_entities': analysis.critical_entities,
        'latitude': analysis.latitude,
        'longitude': analysis.longitude,
        'timestamp': analysis.timestamp.isoformat()
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
    # Calculate Admiralty scores for each intel record
    def calculate_admiralty_score(reliability, credibility):
        # Convert letter grades to numbers (A=5, B=4, C=3, D=2, E=1, F=0)
        reliability_scores = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1, 'F': 0}
        # Convert credibility to numbers (ONE=5, TWO=4, etc)
        credibility_scores = {'ONE': 5, 'TWO': 4, 'THREE': 3, 'FOUR': 2, 'FIVE': 1, 'SIX': 0}
        
        rel_score = reliability_scores.get(reliability, 0)
        cred_score = credibility_scores.get(credibility, 0)
        
        # Calculate percentage (both factors weighted equally)
        # Maximum possible score is 5+5=10, so divide by 10 for percentage
        return ((rel_score + cred_score) / 10) * 100

    # Get intel records with their Admiralty scores
    intel_records = db.session.query(
        IntelligenceData.intel_type,
        IntelligenceData.source_reliability,
        IntelligenceData.info_credibility
    ).all()
    
    # Calculate statistics
    type_scores = {}
    for intel_type in IntelType:
        type_records = [r for r in intel_records if r[0] == intel_type]
        if type_records:
            scores = [calculate_admiralty_score(r[1].name, r[2].name) for r in type_records]
            type_scores[intel_type.name] = {
                'count': len(scores),
                'average_score': sum(scores) / len(scores),
                'max_score': max(scores),
                'min_score': min(scores)
            }

    return jsonify({
        'intelTypes': type_scores
    })