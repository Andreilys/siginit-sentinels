"""add extensive military data

Revision ID: add_extensive_military_data
Revises: add_extensive_intel_data
Create Date: 2024-11-24 07:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from random import uniform, choice, random
from datetime import datetime, timedelta

# revision identifiers, used by Alembic.
revision = 'add_extensive_military_data'
down_revision = 'add_extensive_intel_data'
branch_labels = None
depends_on = None

def generate_random_coordinates(base_lat, base_lon, count):
    """Generate coordinates with random variations"""
    return [(base_lat + uniform(-0.1, 0.1), base_lon + uniform(-0.1, 0.1)) 
            for _ in range(count)]

def generate_content(intel_type, cluster, activity_type):
    """Generate detailed content description"""
    activities = {
        'IMINT': [
            f"Satellite imagery reveals {activity_type} in {cluster} sector",
            f"Aerial reconnaissance identifies {activity_type} near {cluster} region",
            f"Drone footage shows {activity_type} in {cluster} area"
        ],
        'SIGINT': [
            f"Communications intercept indicates {activity_type} in {cluster} sector",
            f"Signal analysis suggests {activity_type} near {cluster} region",
            f"Electronic surveillance detects {activity_type} in {cluster} area"
        ],
        'HUMINT': [
            f"Local sources report {activity_type} in {cluster} sector",
            f"Field agents confirm {activity_type} near {cluster} region",
            f"Reliable informants indicate {activity_type} in {cluster} area"
        ],
        'OSINT': [
            f"Social media analysis reveals {activity_type} in {cluster} sector",
            f"Public sources indicate {activity_type} near {cluster} region",
            f"Media reports suggest {activity_type} in {cluster} area"
        ],
        'CYBERINT': [
            f"Network analysis detects {activity_type} in {cluster} sector",
            f"Cyber surveillance identifies {activity_type} near {cluster} region",
            f"Digital intelligence suggests {activity_type} in {cluster} area"
        ]
    }
    return choice(activities[intel_type])

def generate_timestamp():
    """Generate random timestamp between October and November 2024"""
    start = datetime(2024, 10, 1)
    end = datetime(2024, 11, 30)
    delta = end - start
    random_days = random() * delta.days
    return start + timedelta(days=random_days)

def upgrade():
    # Define clusters with base coordinates and point counts
    clusters = {
        'Northern': {'coords': (51.5074, 31.4567), 'points': 30},
        'Eastern': {'coords': (50.4501, 32.5234), 'points': 25},
        'Southern': {'coords': (49.2226, 30.7111), 'points': 25},
        'Western': {'coords': (50.4501, 29.5234), 'points': 20}
    }

    intel_types = ['IMINT', 'SIGINT', 'HUMINT', 'OSINT', 'CYBERINT']
    reliability_ratings = ['A', 'B', 'C', 'D', 'E', 'F']
    credibility_ratings = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX']
    
    activity_types = [
        'military vehicle movements',
        'troop concentrations',
        'supply line activity',
        'defensive position construction',
        'communication infrastructure deployment',
        'radar system activation',
        'field hospital establishment',
        'command post relocation',
        'ammunition depot activity',
        'training exercise preparations'
    ]

    # Generate and insert data for each cluster
    for cluster_name, cluster_info in clusters.items():
        base_lat, base_lon = cluster_info['coords']
        points_count = cluster_info['points']
        
        coordinates = generate_random_coordinates(base_lat, base_lon, points_count)
        
        for idx, (lat, lon) in enumerate(coordinates):
            intel_type = intel_types[idx % len(intel_types)]
            activity = choice(activity_types)
            credibility_score = round(uniform(0.6, 0.95), 2)
            timestamp = generate_timestamp()
            
            content = generate_content(intel_type, cluster_name, activity)
            
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
                CASE '{intel_type}'
                    WHEN 'IMINT' THEN (
                        CASE (random() * 2)::int
                        WHEN 0 THEN 'Satellite imagery'
                        WHEN 1 THEN 'Drone surveillance'
                        ELSE 'Aerial photography'
                        END
                    )
                    WHEN 'SIGINT' THEN (
                        CASE (random() * 2)::int
                        WHEN 0 THEN 'Radio intercepts'
                        WHEN 1 THEN 'Communications monitoring'
                        ELSE 'Electronic signals'
                        END
                    )
                    WHEN 'HUMINT' THEN (
                        CASE (random() * 1)::int
                        WHEN 0 THEN 'Informants'
                        ELSE 'Diplomatic sources'
                        END
                    )
                    WHEN 'OSINT' THEN (
                        CASE (random() * 1)::int
                        WHEN 0 THEN 'Social media monitoring'
                        ELSE 'News media and publications'
                        END
                    )
                    ELSE (
                        CASE (random() * 1)::int
                        WHEN 0 THEN 'Network traffic analysis'
                        ELSE 'Malware analysis'
                        END
                    )
                END,
                '{choice(reliability_ratings)}',
                '{choice(credibility_ratings)}',
                '{timestamp}'
            )
            """)

def downgrade():
    # Since this is just adding data, we don't need a downgrade
    pass
