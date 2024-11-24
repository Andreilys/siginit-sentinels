"""reset and repopulate data

Revision ID: reset_and_repopulate_data
Revises: fix_sigint_data
Create Date: 2024-11-24 06:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'reset_and_repopulate_data'
down_revision = 'fix_sigint_data'
branch_labels = None
depends_on = None

def upgrade():
    # Clear existing data
    op.execute('DELETE FROM alert')
    op.execute('DELETE FROM intelligence_data')
    
    # Add sample SIGINT data
    op.execute('''
    INSERT INTO intelligence_data (source, content, credibility_score, language, latitude, longitude, intel_type, intel_subtype, source_reliability, info_credibility)
    VALUES 
    ('SIGINT-1', 'Intercepted communications indicate troop movements near border region', 0.9, 'en', 50.4501, 30.5234, 'SIGINT', 'Radio intercepts', 'A', 'ONE'),
    ('SIGINT-2', 'Radio intercepts reveal supply route changes', 0.85, 'en', 49.8397, 24.0297, 'SIGINT', 'Communications monitoring', 'B', 'TWO')
    ''')
    
    # Add sample IMINT data
    op.execute('''
    INSERT INTO intelligence_data (source, content, credibility_score, language, latitude, longitude, intel_type, intel_subtype, source_reliability, info_credibility)
    VALUES 
    ('IMINT-1', 'Satellite imagery shows new fortification construction', 0.95, 'en', 48.9226, 24.7111, 'IMINT', 'Satellite imagery', 'A', 'ONE'),
    ('IMINT-2', 'Drone footage confirms vehicle depot expansion', 0.8, 'en', 51.5074, 30.4567, 'IMINT', 'Drone surveillance', 'B', 'TWO')
    ''')

    # Add corresponding alerts
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
    # For safety, we don't want to automatically delete data in downgrade
    pass
