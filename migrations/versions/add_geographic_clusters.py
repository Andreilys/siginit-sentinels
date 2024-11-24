"""add geographic clusters

Revision ID: add_geographic_clusters
Revises: add_heatmap_data
Create Date: 2024-11-24 06:45:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_geographic_clusters'
down_revision = 'add_heatmap_data'
branch_labels = None
depends_on = None

def upgrade():
    # Add more intelligence data points for better heatmap visualization
    op.execute('''
    INSERT INTO intelligence_data (source, content, credibility_score, language, latitude, longitude, intel_type, intel_subtype, source_reliability, info_credibility)
    VALUES 
    -- Northern Cluster
    ('IMINT-9', 'Satellite imagery of northern military installations', 0.9, 'en', 51.5074, 31.4567, 'IMINT', 'Satellite imagery', 'A', 'ONE'),
    ('SIGINT-9', 'Communications intercept from northern region', 0.85, 'en', 51.4801, 31.5234, 'SIGINT', 'Radio intercepts', 'B', 'TWO'),
    ('HUMINT-9', 'Field agent reports from northern border', 0.8, 'en', 51.4901, 31.5134, 'HUMINT', 'Informants', 'B', 'TWO'),
    
    -- Eastern Cluster
    ('IMINT-10', 'Drone surveillance of eastern facilities', 0.75, 'en', 50.4501, 32.5234, 'IMINT', 'Drone surveillance', 'C', 'THREE'),
    ('SIGINT-10', 'Signal monitoring from eastern sector', 0.8, 'en', 50.4601, 32.5334, 'SIGINT', 'Electronic signals', 'B', 'TWO'),
    ('OSINT-8', 'Social media activity in eastern region', 0.7, 'en', 50.4401, 32.5134, 'OSINT', 'Social media monitoring', 'C', 'THREE'),
    
    -- Southern Cluster
    ('IMINT-11', 'Aerial photography of southern region', 0.95, 'en', 49.2226, 30.7111, 'IMINT', 'Aerial photography', 'A', 'ONE'),
    ('CYBERINT-8', 'Network analysis from southern facilities', 0.9, 'en', 49.2326, 30.7211, 'CYBERINT', 'Network traffic analysis', 'A', 'ONE'),
    ('HUMINT-10', 'Local informant network in south', 0.85, 'en', 49.2426, 30.7311, 'HUMINT', 'Informants', 'B', 'TWO'),
    
    -- Western Cluster
    ('SIGINT-11', 'Communications monitoring in west', 0.7, 'en', 50.4501, 29.5234, 'SIGINT', 'Communications monitoring', 'C', 'THREE'),
    ('OSINT-9', 'Media reports from western region', 0.75, 'en', 50.4601, 29.5334, 'OSINT', 'News media and publications', 'C', 'THREE'),
    ('CYBERINT-9', 'Cyber threat analysis from west', 0.8, 'en', 50.4401, 29.5134, 'CYBERINT', 'Malware analysis', 'B', 'TWO')
    ''')

def downgrade():
    pass
