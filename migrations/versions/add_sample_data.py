"""add sample data

Revision ID: add_sample_data
Revises: update_intel_types
Create Date: 2024-11-24 05:45:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_sample_data'
down_revision = 'update_intel_types'
branch_labels = None
depends_on = None

def upgrade():
    # First clear existing data
    op.execute('DELETE FROM intelligence_data')
    
    # Add sample IMINT data
    op.execute('''
    INSERT INTO intelligence_data (source, content, credibility_score, language, latitude, longitude, intel_type, intel_subtype, source_reliability, info_credibility)
    VALUES 
    ('Satellite-1', 'Satellite imagery shows tank column movement near border', 0.9, 'en', 50.4501, 30.5234, 'IMINT', 'Satellite imagery', 'A', 'ONE'),
    ('Drone-1', 'Drone footage reveals artillery positions in forest area', 0.8, 'en', 49.8397, 24.0297, 'IMINT', 'Drone surveillance', 'B', 'TWO')
    ''')
    
    # Add sample SIGINT data
    op.execute('''
    INSERT INTO intelligence_data (source, content, credibility_score, language, latitude, longitude, intel_type, intel_subtype, source_reliability, info_credibility)
    VALUES 
    ('SIGINT-1', 'Radio intercept: Units discussing ammunition resupply', 0.7, 'en', 48.9226, 24.7111, 'SIGINT', 'Radio intercepts', 'C', 'THREE'),
    ('SIGINT-2', 'Electronic signal detection indicates radar activation', 0.85, 'en', 51.5074, 30.4567, 'SIGINT', 'Electronic signals', 'B', 'TWO')
    ''')
    
    # Add sample HUMINT data
    op.execute('''
    INSERT INTO intelligence_data (source, content, credibility_score, language, latitude, longitude, intel_type, intel_subtype, source_reliability, info_credibility)
    VALUES 
    ('HUMINT-1', 'Local informant reports troop movements at night', 0.6, 'en', 49.5883, 34.5514, 'HUMINT', 'Informants', 'D', 'FOUR'),
    ('HUMINT-2', 'Diplomatic source confirms military exercise plans', 0.9, 'en', 50.4547, 30.5238, 'HUMINT', 'Diplomatic sources', 'A', 'ONE')
    ''')

    # Add sample OSINT data
    op.execute('''
    INSERT INTO intelligence_data (source, content, credibility_score, language, latitude, longitude, intel_type, intel_subtype, source_reliability, info_credibility)
    VALUES 
    ('OSINT-1', 'Social media posts showing military vehicles on highways', 0.5, 'en', 49.9935, 36.2304, 'OSINT', 'Social media monitoring', 'E', 'FIVE'),
    ('OSINT-2', 'News report details upcoming military exercises', 0.8, 'en', 50.9216, 34.8002, 'OSINT', 'News media and publications', 'B', 'TWO')
    ''')

    # Add sample CYBERINT data
    op.execute('''
    INSERT INTO intelligence_data (source, content, credibility_score, language, latitude, longitude, intel_type, intel_subtype, source_reliability, info_credibility)
    VALUES 
    ('CYBER-1', 'Malware analysis reveals targeting of military networks', 0.95, 'en', 50.4501, 30.5234, 'CYBERINT', 'Malware analysis', 'A', 'ONE'),
    ('CYBER-2', 'Dark web chatter indicates planned cyber operations', 0.7, 'en', 49.8397, 24.0297, 'CYBERINT', 'Dark web monitoring', 'C', 'THREE')
    ''')

    # Create corresponding alerts with different priorities
    op.execute('''
    INSERT INTO alert (title, description, priority, status, intel_id)
    SELECT 
        CASE 
            WHEN id.credibility_score >= 0.8 THEN 'High Priority Alert'
            WHEN id.credibility_score >= 0.6 THEN 'Medium Priority Alert'
            ELSE 'Low Priority Alert'
        END,
        id.content,
        CASE 
            WHEN id.credibility_score >= 0.8 THEN 1
            WHEN id.credibility_score >= 0.6 THEN 2
            ELSE 3
        END,
        'new',
        id.id
    FROM intelligence_data id
    ''')

def downgrade():
    op.execute('DELETE FROM alert')
    op.execute('DELETE FROM intelligence_data')
