"""add final intel clusters

Revision ID: add_final_intel_clusters
Revises: add_extensive_military_data
Create Date: 2024-11-24 08:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from random import uniform, choice, random
from datetime import datetime, timedelta

# revision identifiers, used by Alembic.
revision = 'add_final_intel_clusters'
down_revision = 'add_extensive_military_data'
branch_labels = None
depends_on = None

def generate_random_coordinates(base_lat, base_lon, count):
    """Generate coordinates with random variations within ±0.1 degrees"""
    return [(base_lat + uniform(-0.1, 0.1), base_lon + uniform(-0.1, 0.1)) 
            for _ in range(count)]

def generate_timestamp():
    """Generate random timestamp between October and November 2024"""
    start = datetime(2024, 10, 1)
    end = datetime(2024, 11, 30)
    delta = end - start
    random_days = random() * delta.days
    return start + timedelta(days=random_days)

def generate_detailed_content(intel_type, cluster, activity):
    """Generate detailed intelligence content"""
    activities = {
        'IMINT': [
            f"High-resolution satellite imagery reveals {activity} in {cluster} region",
            f"Drone reconnaissance footage shows {activity} near {cluster} sector",
            f"Aerial photography confirms {activity} in {cluster} area"
        ],
        'SIGINT': [
            f"Signal intercepts indicate {activity} in {cluster} region",
            f"Communications monitoring reveals {activity} near {cluster} sector",
            f"Electronic surveillance detects {activity} in {cluster} area"
        ],
        'HUMINT': [
            f"Field operatives report {activity} in {cluster} region",
            f"Local sources confirm {activity} near {cluster} sector",
            f"Intelligence network identifies {activity} in {cluster} area"
        ],
        'OSINT': [
            f"Social media analysis suggests {activity} in {cluster} region",
            f"Open source intelligence indicates {activity} near {cluster} sector",
            f"Public data sources reveal {activity} in {cluster} area"
        ],
        'CYBERINT': [
            f"Network analysis detects {activity} in {cluster} region",
            f"Cyber surveillance identifies {activity} near {cluster} sector",
            f"Digital intelligence confirms {activity} in {cluster} area"
        ]
    }
    return choice(activities[intel_type])

def upgrade():
    # Define clusters with their base coordinates and point counts
    clusters = {
        'Northern': {'coords': (51.5074, 31.4567), 'points': 30},
        'Eastern': {'coords': (50.4501, 32.5234), 'points': 30},
        'Southern': {'coords': (49.2226, 30.7111), 'points': 25},
        'Western': {'coords': (50.4501, 29.5234), 'points': 25}
    }

    intel_types = ['IMINT', 'SIGINT', 'HUMINT', 'OSINT', 'CYBERINT']
    reliability_ratings = ['A', 'B', 'C', 'D', 'E', 'F']
    credibility_ratings = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX']
    
    military_activities = [
        'large-scale troop movements',
        'military vehicle convoys',
        'defensive position fortification',
        'communication infrastructure deployment',
        'supply line establishment',
        'command post relocation',
        'field hospital construction',
        'ammunition depot activity',
        'radar system installation',
        'training exercise preparations',
        'logistics hub development',
        'reconnaissance operations'
    ]

    subtypes = {
        'IMINT': ['Satellite imagery', 'Drone surveillance', 'Aerial photography'],
        'SIGINT': ['Radio intercepts', 'Communications monitoring', 'Electronic signals'],
        'HUMINT': ['Informants', 'Diplomatic sources', 'Field agents'],
        'OSINT': ['Social media monitoring', 'News media and publications'],
        'CYBERINT': ['Network traffic analysis', 'Malware analysis', 'Dark web monitoring']
    }

    # Generate and insert data for each cluster
    for cluster_name, cluster_info in clusters.items():
        base_lat, base_lon = cluster_info['coords']
        points_count = cluster_info['points']
        
        coordinates = generate_random_coordinates(base_lat, base_lon, points_count)
        
        for idx, (lat, lon) in enumerate(coordinates):
            intel_type = intel_types[idx % len(intel_types)]
            activity = choice(military_activities)
            credibility_score = round(uniform(0.6, 0.95), 2)
            timestamp = generate_timestamp()
            
            content = generate_detailed_content(intel_type, cluster_name, activity)
            subtype = choice(subtypes[intel_type])
            
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
