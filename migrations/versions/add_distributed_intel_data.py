"""add distributed intel data

Revision ID: add_distributed_intel_data
Revises: add_extensive_military_data
Create Date: 2024-11-24 08:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from random import uniform, choice, random
from datetime import datetime, timedelta

# revision identifiers, used by Alembic.
revision = 'add_distributed_intel_data'
down_revision = 'add_extensive_military_data'
branch_labels = None
depends_on = None

def generate_timestamp():
    """Generate random timestamp between October and November 2024"""
    start = datetime(2024, 10, 1)
    end = datetime(2024, 11, 30)
    delta = end - start
    random_days = random() * delta.days
    return start + timedelta(days=random_days)

def generate_coordinates(base_lat, base_lon):
    """Generate coordinates with ±0.1 degree variation"""
    return (base_lat + uniform(-0.1, 0.1), base_lon + uniform(-0.1, 0.1))

def upgrade():
    # Define clusters
    clusters = {
        'Northern': (51.5074, 31.4567),
        'Eastern': (50.4501, 32.5234),
        'Southern': (49.2226, 30.7111),
        'Western': (50.4501, 29.5234)
    }

    # Intel types and their subtypes
    intel_subtypes = {
        'IMINT': ['Satellite imagery', 'Drone surveillance', 'Aerial photography'],
        'SIGINT': ['Radio intercepts', 'Communications monitoring', 'Electronic signals'],
        'HUMINT': ['Informants', 'Diplomatic sources', 'Field agents'],
        'OSINT': ['Social media monitoring', 'News media and publications'],
        'CYBERINT': ['Network traffic analysis', 'Malware analysis', 'Dark web monitoring']
    }

    reliability_ratings = ['A', 'B', 'C', 'D', 'E', 'F']
    credibility_ratings = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX']

    # Generate content templates for each intel type
    content_templates = {
        'IMINT': [
            "Visual confirmation of military activities through {subtype}",
            "Identified strategic positions using {subtype}",
            "Military infrastructure developments captured via {subtype}"
        ],
        'SIGINT': [
            "Detected significant communications through {subtype}",
            "Intercepted tactical information via {subtype}",
            "Monitored strategic communications using {subtype}"
        ],
        'HUMINT': [
            "Intelligence gathered from {subtype} indicates military movements",
            "Strategic information obtained through {subtype}",
            "Operational details confirmed by {subtype}"
        ],
        'OSINT': [
            "Analysis of {subtype} reveals military preparations",
            "Strategic patterns identified through {subtype}",
            "Intelligence derived from {subtype} suggests increased activity"
        ],
        'CYBERINT': [
            "Digital intelligence gathered through {subtype}",
            "Cyber surveillance using {subtype} indicates activity",
            "Technical analysis via {subtype} reveals patterns"
        ]
    }

    # Generate and insert 20 records for each intel type
    for intel_type, subtypes in intel_subtypes.items():
        for _ in range(20):  # 20 records per type
            # Select random cluster and generate coordinates
            cluster_name = choice(list(clusters.keys()))
            base_lat, base_lon = clusters[cluster_name]
            lat, lon = generate_coordinates(base_lat, base_lon)
            
            # Select subtype and generate content
            subtype = choice(subtypes)
            content_template = choice(content_templates[intel_type])
            content = content_template.format(subtype=subtype)
            content = f"{content} in {cluster_name} cluster"
            
            # Generate other random attributes
            credibility_score = round(uniform(0.6, 0.95), 2)
            timestamp = generate_timestamp()

            op.execute(f"""
            INSERT INTO intelligence_data (
                source,
                content,
                credibility_score,
                language,
                latitude,
                longitude,
                intel_type,
                intel_subtype,
                source_reliability,
                info_credibility,
                timestamp
            ) VALUES (
                '{intel_type}-{cluster_name}-{_}',
                '{content}',
                {credibility_score},
                'en',
                {lat},
                {lon},
                '{intel_type}',
                '{subtype}',
                '{choice(reliability_ratings)}',
                '{choice(credibility_ratings)}',
                '{timestamp}'
            )
            """)

def downgrade():
    # Since this is just adding data, we don't need a downgrade
    pass
