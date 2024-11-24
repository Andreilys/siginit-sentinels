"""add extensive intel data

Revision ID: add_extensive_intel_data
Revises: add_comprehensive_intel_data
Create Date: 2024-11-24 07:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from random import uniform, choice, random
from datetime import datetime, timedelta

# revision identifiers, used by Alembic.
revision = 'add_extensive_intel_data'
down_revision = 'add_comprehensive_intel_data'
branch_labels = None
depends_on = None

def generate_varied_coordinates(base_lat, base_lon, count):
    """Generate coordinates with random offsets"""
    coordinates = []
    for _ in range(count):
        lat = base_lat + uniform(-0.1, 0.1)
        lon = base_lon + uniform(-0.1, 0.1)
        coordinates.append((lat, lon))
    return coordinates

def generate_random_timestamp():
    """Generate random timestamp between October and November 2024"""
    start = datetime(2024, 10, 1)
    end = datetime(2024, 11, 30)
    delta = end - start
    random_days = random() * delta.days
    return start + timedelta(days=random_days)

def upgrade():
    # Base coordinates for each cluster
    clusters = {
        'Northern': (51.5074, 31.4567),
        'Eastern': (50.4501, 32.5234),
        'Southern': (49.2226, 30.7111),
        'Western': (50.4501, 29.5234)
    }

    intel_types = ['IMINT', 'SIGINT', 'HUMINT', 'OSINT', 'CYBERINT']
    reliability_ratings = ['A', 'B', 'C', 'D', 'E', 'F']
    credibility_ratings = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX']

    # Generate 25+ points for each cluster
    for cluster_name, (base_lat, base_lon) in clusters.items():
        coordinates = generate_varied_coordinates(base_lat, base_lon, 30)  # 30 points per cluster
        
        for idx, (lat, lon) in enumerate(coordinates):
            intel_type = intel_types[idx % len(intel_types)]
            credibility_score = round(uniform(0.6, 0.95), 2)
            timestamp = generate_random_timestamp()
            
            subtype = {
                'IMINT': choice(['Satellite imagery', 'Drone surveillance', 'Aerial photography']),
                'SIGINT': choice(['Radio intercepts', 'Communications monitoring', 'Electronic signals']),
                'HUMINT': choice(['Informants', 'Diplomatic sources', 'Field agents']),
                'OSINT': choice(['Social media monitoring', 'News media and publications']),
                'CYBERINT': choice(['Network traffic analysis', 'Malware analysis', 'Dark web monitoring'])
            }[intel_type]

            content = f"{intel_type} report from {cluster_name} cluster indicating military activity. "
            content += f"Analysis shows significant developments in the region. Timestamp: {timestamp}"

            op.execute(f"""
            INSERT INTO intelligence_data (
                source, content, credibility_score, language, latitude, longitude,
                intel_type, intel_subtype, source_reliability, info_credibility, timestamp
            ) VALUES (
                '{intel_type}-{cluster_name}-{idx + 1}',
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
