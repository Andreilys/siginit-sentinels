"""add comprehensive intel data

Revision ID: add_comprehensive_intel_data
Revises: add_bulk_intel_data
Create Date: 2024-11-24 07:15:00.000000

"""
from alembic import op
import sqlalchemy as sa
from random import uniform, choice, random
from datetime import datetime, timedelta

# revision identifiers, used by Alembic.
revision = 'add_comprehensive_intel_data'
down_revision = 'add_bulk_intel_data'
branch_labels = None
depends_on = None

def generate_coordinates(base_lat, base_lon, count):
    """Generate slightly varied coordinates around a base point"""
    coords = []
    for _ in range(count):
        lat = base_lat + uniform(-0.05, 0.05)
        lon = base_lon + uniform(-0.05, 0.05)
        coords.append((lat, lon))
    return coords

def generate_timestamp():
    """Generate random timestamp between October and November 2024"""
    start_date = datetime(2024, 10, 1)
    end_date = datetime(2024, 11, 30)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random() * days_between_dates
    return start_date + timedelta(days=random_number_of_days)

def upgrade():
    # Define base coordinates for each cluster
    clusters = {
        'Northern': (51.5074, 31.4567, 6),  # 6 points per intel type
        'Eastern': (50.4501, 32.5234, 5),   # 5 points per intel type
        'Southern': (49.2226, 30.7111, 5),  # 5 points per intel type
        'Western': (50.4501, 29.5234, 4),   # 4 points per intel type
    }

    intel_types = ['IMINT', 'SIGINT', 'HUMINT', 'OSINT', 'CYBERINT']
    reliability_ratings = ['A', 'B', 'C', 'D', 'E', 'F']
    credibility_ratings = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX']

    # Generate and execute insert statements for each cluster
    for cluster_name, (base_lat, base_lon, points_per_type) in clusters.items():
        for intel_type in intel_types:
            coords = generate_coordinates(base_lat, base_lon, points_per_type)
            
            for i, (lat, lon) in enumerate(coords):
                credibility_score = round(uniform(0.6, 0.95), 2)
                timestamp = generate_timestamp().strftime('%Y-%m-%d %H:%M:%S')
                
                op.execute(f"""
                INSERT INTO intelligence_data (
                    source, content, credibility_score, language, latitude, longitude,
                    intel_type, intel_subtype, source_reliability, info_credibility, timestamp
                )
                VALUES (
                    '{intel_type}-{cluster_name}-{i+1}',
                    'Intelligence report from {cluster_name} region indicating significant activity',
                    {credibility_score},
                    'en',
                    {lat},
                    {lon},
                    '{intel_type}',
                    CASE
                        WHEN '{intel_type}' = 'IMINT' THEN 
                            CASE (random() * 3)::int
                            WHEN 0 THEN 'Satellite imagery'
                            WHEN 1 THEN 'Drone surveillance'
                            ELSE 'Aerial photography'
                            END
                        WHEN '{intel_type}' = 'SIGINT' THEN 
                            CASE (random() * 3)::int
                            WHEN 0 THEN 'Radio intercepts'
                            WHEN 1 THEN 'Communications monitoring'
                            ELSE 'Electronic signals'
                            END
                        WHEN '{intel_type}' = 'HUMINT' THEN 
                            CASE (random() * 2)::int
                            WHEN 0 THEN 'Informants'
                            ELSE 'Diplomatic sources'
                            END
                        WHEN '{intel_type}' = 'OSINT' THEN 
                            CASE (random() * 2)::int
                            WHEN 0 THEN 'Social media monitoring'
                            ELSE 'News media and publications'
                            END
                        ELSE 
                            CASE (random() * 2)::int
                            WHEN 0 THEN 'Network traffic analysis'
                            ELSE 'Malware analysis'
                            END
                    END,
                    '{choice(reliability_ratings)}',
                    '{choice(credibility_ratings)}',
                    '{timestamp}'
                )
                """)

def downgrade():
    # Since this is just adding data, we don't need a downgrade
    pass
