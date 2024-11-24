"""add heatmap data

Revision ID: add_heatmap_data
Revises: add_more_historical_data
Create Date: 2024-11-24 06:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_heatmap_data'
down_revision = 'add_more_historical_data'
branch_labels = None
depends_on = None

def upgrade():
    # Add more sample data points for better visualization
    op.execute('''
    INSERT INTO intelligence_data (source, content, credibility_score, language, latitude, longitude, intel_type, intel_subtype, source_reliability, info_credibility)
    VALUES 
    -- Cluster 1 - High activity area
    ('IMINT-7', 'Satellite imagery shows increased activity in border region', 0.9, 'en', 50.4501, 30.5234, 'IMINT', 'Satellite imagery', 'A', 'ONE'),
    ('SIGINT-7', 'Multiple radio intercepts in northern sector', 0.85, 'en', 50.4601, 30.5334, 'SIGINT', 'Radio intercepts', 'B', 'TWO'),
    ('HUMINT-7', 'Local reports of unusual movement patterns', 0.8, 'en', 50.4401, 30.5134, 'HUMINT', 'Informants', 'B', 'TWO'),
    
    -- Cluster 2 - Medium activity area
    ('OSINT-7', 'Social media activity spike in eastern region', 0.75, 'en', 49.8397, 24.0297, 'OSINT', 'Social media monitoring', 'C', 'THREE'),
    ('CYBERINT-7', 'Detected network anomalies in industrial zone', 0.8, 'en', 49.8497, 24.0397, 'CYBERINT', 'Network traffic analysis', 'B', 'TWO'),
    
    -- Cluster 3 - Low activity area
    ('IMINT-8', 'Routine surveillance imagery of southern region', 0.6, 'en', 48.9226, 24.7111, 'IMINT', 'Drone surveillance', 'D', 'FOUR'),
    ('SIGINT-8', 'Standard communications monitoring report', 0.5, 'en', 48.9326, 24.7211, 'SIGINT', 'Communications monitoring', 'E', 'FIVE')
    ''')

def downgrade():
    pass
