from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from models import Alert, IntelligenceData
from elasticsearch import Elasticsearch
from datetime import datetime

# load env
from dotenv import load_dotenv

import os

load_dotenv()


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@main_bp.route("/dashboard")
@login_required
def dashboard():
    alerts = Alert.query.order_by(Alert.timestamp.desc()).limit(5).all()
    threat_level = calculate_threat_level()
    return render_template("dashboard.html", alerts=alerts, threat_level=threat_level)


@main_bp.route("/alerts")
@login_required
def alerts():
    from flask import current_app

    # Query intelligence data directly
    intel_data = IntelligenceData.query.order_by(
        IntelligenceData.timestamp.desc()
    ).all()

    # Calculate Admiralty scores and assign priorities
    alerts_data = []
    for intel in intel_data:
        try:
            # Calculate Admiralty score
            reliability_scores = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "F": 0}
            credibility_scores = {
                "ONE": 5,
                "TWO": 4,
                "THREE": 3,
                "FOUR": 2,
                "FIVE": 1,
                "SIX": 0,
            }

            # Safely get enum values with fallback to lowest score
            rel_score = reliability_scores.get(
                intel.source_reliability.name if intel.source_reliability else "F", 0
            )
            cred_score = credibility_scores.get(
                intel.info_credibility.name if intel.info_credibility else "SIX", 0
            )

            admiralty_score = (rel_score + cred_score) / 10  # 0 to 1 scale

            # Assign priority based on Admiralty score
            if admiralty_score >= 0.7:
                priority = "high"
            elif admiralty_score >= 0.4:
                priority = "medium"
            else:
                priority = "low"

            alerts_data.append(
                {
                    "intel": intel,
                    "admiralty_score": admiralty_score,
                    "priority": priority,
                }
            )
        except Exception as e:
            # Log the error but continue processing other records
            current_app.logger.error(
                f"Error processing intel record {intel.id}: {str(e)}"
            )
            continue

    return render_template("alerts.html", alerts=alerts_data)


@main_bp.route("/reports")
@login_required
def reports():
    return render_template("reports.html")


def calculate_threat_level():
    # Simple threat level calculation based on recent high-priority alerts
    high_priority_count = Alert.query.filter_by(priority=1).count()


@main_bp.route("/telegram")
@login_required
def telegram():
    return render_template("telegram.html")


@main_bp.route("/audio")
@login_required
def audio():
    return render_template("audio.html")


@main_bp.route("/api/telegram-data")
@login_required
def telegram_data():

    es_host = os.getenv("ELASTICSEARCH_HOST", "http://localhost:9200")
    es_api_key = os.getenv("ELASTICSEARCH_API_KEY")

    # Initialize Elasticsearch with proper URL format
    es = Elasticsearch(
        [es_host],
        api_key=es_api_key,
    )

    # Build the query
    query = {"bool": {"must": [], "filter": []}}

    # Text search
    if search_query := request.args.get("query"):
        query["bool"]["must"].append(
            {
                "multi_match": {
                    "query": search_query,
                    "fields": ["text", "translated_text", "media_description"],
                }
            }
        )

    # Channel filter
    if channel := request.args.get("channel"):
        query["bool"]["filter"].append({"term": {"channel_name": channel}})

    # Language filter
    if language := request.args.get("language"):
        query["bool"]["filter"].append({"term": {"detected_language_code": language}})

    # Date range
    date_filter = {}
    if start_date := request.args.get("start_date"):
        date_filter["gte"] = start_date
    if end_date := request.args.get("end_date"):
        date_filter["lte"] = end_date
    if date_filter:
        query["bool"]["filter"].append({"range": {"date": date_filter}})

    # Entity filter
    if entity_type := request.args.get("entity_type"):
        query["bool"]["filter"].append(
            {
                "nested": {
                    "path": f"entities.{entity_type}",
                    "query": {"exists": {"field": f"entities.{entity_type}"}},
                }
            }
        )

    # Location mentioned filter
    if request.args.get("location_mentioned") == "true":
        query["bool"]["filter"].append({"term": {"location_mentioned": True}})

    # Execute search
    results = es.search(
        index="telegram_messages_temp",
        query=query,
        size=50,  # Limit results
        sort=[{"date": {"order": "desc"}}],
    )

    return jsonify(results["hits"]["hits"])
