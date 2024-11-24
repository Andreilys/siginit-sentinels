"""add more historical data

Revision ID: add_more_historical_data
Revises: add_historical_data
Create Date: 2024-11-24 06:25:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_more_historical_data'
down_revision = 'add_historical_data'
branch_labels = None
depends_on = None

def upgrade():
    # Add more historical intelligence data spanning from April 2023 to October 2024
    op.execute('''
    INSERT INTO intelligence_data (source, content, credibility_score, language, latitude, longitude, intel_type, intel_subtype, source_reliability, info_credibility, timestamp)
    VALUES 
    -- May 2023
    ('IMINT-5', 'Satellite imagery shows construction of new military facilities', 0.85, 'en', 49.8397, 24.0297, 'IMINT', 'Satellite imagery', 'A', 'ONE', '2023-05-15'),
    -- June 2023
    ('SIGINT-5', 'Encrypted communications suggest increased military activity', 0.75, 'en', 50.4501, 30.5234, 'SIGINT', 'Electronic signals', 'B', 'TWO', '2023-06-20'),
    -- August 2023
    ('HUMINT-5', 'Network of informants reports troop rotations', 0.80, 'en', 51.5074, 30.4567, 'HUMINT', 'Informants', 'B', 'TWO', '2023-08-10'),
    -- September 2023
    ('OSINT-5', 'Analysis of public satellite imagery reveals new developments', 0.70, 'en', 48.9226, 24.7111, 'OSINT', 'Social media monitoring', 'C', 'THREE', '2023-09-05'),
    -- November 2023
    ('CYBERINT-5', 'Detection of new cyber infrastructure targeting military networks', 0.90, 'en', 50.9216, 34.8002, 'CYBERINT', 'Network traffic analysis', 'A', 'ONE', '2023-11-15'),
    -- December 2023
    ('IMINT-6', 'Aerial surveillance shows new defensive positions', 0.85, 'en', 49.5883, 34.5514, 'IMINT', 'Aerial photography', 'B', 'TWO', '2023-12-22'),
    -- February 2024
    ('SIGINT-6', 'Increased radio traffic in border region', 0.80, 'en', 50.4501, 30.5234, 'SIGINT', 'Radio intercepts', 'B', 'TWO', '2024-02-15'),
    -- March 2024
    ('HUMINT-6', 'Local sources report unusual military movements', 0.75, 'en', 49.8397, 24.0297, 'HUMINT', 'Informants', 'C', 'THREE', '2024-03-20'),
    -- May 2024
    ('OSINT-6', 'Social media analysis indicates military exercise preparations', 0.85, 'en', 51.5074, 30.4567, 'OSINT', 'Social media monitoring', 'B', 'TWO', '2024-05-10'),
    -- June 2024
    ('CYBERINT-6', 'Dark web intelligence suggests planned cyber operations', 0.70, 'en', 48.9226, 24.7111, 'CYBERINT', 'Dark web monitoring', 'C', 'THREE', '2024-06-05')
    ''')

def downgrade():
    # Since this is just adding data, we don't need a downgrade
    pass
