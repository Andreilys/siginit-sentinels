"""add historical data

Revision ID: add_historical_data
Revises: update_intel_subtypes
Create Date: 2024-11-24 06:20:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_historical_data'
down_revision = 'update_intel_subtypes'
branch_labels = None
depends_on = None

def upgrade():
    # Add more historical intelligence data
    op.execute('''
    INSERT INTO intelligence_data (source, content, credibility_score, language, latitude, longitude, intel_type, intel_subtype, source_reliability, info_credibility, timestamp)
    VALUES 
    -- April 2023
    ('IMINT-3', 'Satellite imagery reveals new military installation construction', 0.85, 'en', 49.8397, 24.0297, 'IMINT', 'Satellite imagery', 'A', 'ONE', '2023-04-15'),
    -- July 2023
    ('SIGINT-3', 'Communications intercept indicates increased radio traffic', 0.75, 'en', 50.4501, 30.5234, 'SIGINT', 'Radio intercepts', 'B', 'TWO', '2023-07-20'),
    -- October 2023
    ('HUMINT-3', 'Local informant network reports troop movements', 0.80, 'en', 51.5074, 30.4567, 'HUMINT', 'Informants', 'B', 'TWO', '2023-10-10'),
    -- January 2024
    ('OSINT-3', 'Social media analysis shows pattern of military exercises', 0.70, 'en', 48.9226, 24.7111, 'OSINT', 'Social media monitoring', 'C', 'THREE', '2024-01-05'),
    -- April 2024
    ('CYBERINT-3', 'Detection of targeted cyber operations against infrastructure', 0.90, 'en', 50.9216, 34.8002, 'CYBERINT', 'Network traffic analysis', 'A', 'ONE', '2024-04-15'),
    -- July 2024
    ('IMINT-4', 'Drone surveillance footage of border activity', 0.85, 'en', 49.5883, 34.5514, 'IMINT', 'Drone surveillance', 'B', 'TWO', '2024-07-22')
    ''')

def downgrade():
    # Since this is just adding data, we don't need a downgrade
    pass
