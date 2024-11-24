from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from models import Alert, IntelligenceData
from models import Alert, IntelligenceData, ConversationAnalysis
from elasticsearch import Elasticsearch
from datetime import datetime

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
    from flask import current_app
    # Query intelligence data directly
    intel_data = IntelligenceData.query.order_by(IntelligenceData.timestamp.desc()).all()
    
    # Calculate Admiralty scores and assign priorities
    alerts_data = []
    for intel in intel_data:
        try:
            # Calculate Admiralty score
            reliability_scores = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1, 'F': 0}
            credibility_scores = {'ONE': 5, 'TWO': 4, 'THREE': 3, 'FOUR': 2, 'FIVE': 1, 'SIX': 0}
            
            # Safely get enum values with fallback to lowest score
            rel_score = reliability_scores.get(intel.source_reliability.name if intel.source_reliability else 'F', 0)
            cred_score = credibility_scores.get(intel.info_credibility.name if intel.info_credibility else 'SIX', 0)
            
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
        except Exception as e:
            # Log the error but continue processing other records
            current_app.logger.error(f'Error processing intel record {intel.id}: {str(e)}')
            continue
    
    return render_template('alerts.html', alerts=alerts_data)

@main_bp.route('/reports')
@login_required
def reports():
    return render_template('reports.html')

def calculate_threat_level():
    # Simple threat level calculation based on recent high-priority alerts
    high_priority_count = Alert.query.filter_by(priority=1).count()

@main_bp.route('/audio')
@login_required
def audio():
    conversations = ConversationAnalysis.query.order_by(ConversationAnalysis.analyzed_at.desc()).all()
    return render_template('audio.html', conversations=conversations)

@main_bp.route('/telegram')
@login_required
def telegram():
    return render_template('telegram.html')

@main_bp.route('/api/telegram-data')
@login_required
def telegram_data():
    es = Elasticsearch(['localhost:9200'])  # Default elasticsearch endpoint
    
    # Get filter parameters
    query = request.args.get('query', '')
    channel = request.args.get('channel', '')
    language = request.args.get('language', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    
    # Build Elasticsearch query
    must_conditions = []
    if query:
        must_conditions.append({"multi_match": {
            "query": query,
            "fields": ["content", "title"]
        }})
    if channel:
        must_conditions.append({"match": {"channel": channel}})
    if language:
        must_conditions.append({"match": {"language": language}})
    if start_date and end_date:
        must_conditions.append({
            "range": {
                "timestamp": {
                    "gte": start_date,
                    "lte": end_date
                }
            }
        })
    
    body = {
        "query": {
            "bool": {
                "must": must_conditions if must_conditions else [{"match_all": {}}]
            }
        },
        "sort": [{"timestamp": "desc"}],
        "size": 100
    }
    
    try:
        result = es.search(index="telegram_data", body=body)
        return jsonify(result['hits']['hits'])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return min(high_priority_count * 20, 100)  # 20% per high-priority alert, max 100%
