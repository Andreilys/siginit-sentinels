"""add bulk intel data

Revision ID: add_bulk_intel_data
Revises: add_geographic_clusters
Create Date: 2024-11-24 07:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_bulk_intel_data'
down_revision = 'add_geographic_clusters'
branch_labels = None
depends_on = None

def upgrade():
    # Add multiple clusters of intelligence data
    op.execute('''
    INSERT INTO intelligence_data (source, content, credibility_score, language, latitude, longitude, intel_type, intel_subtype, source_reliability, info_credibility, timestamp)
    VALUES 
    -- Northern Cluster (30 points)
    ('IMINT-12', 'Satellite imagery shows military buildup', 0.9, 'en', 51.5074, 31.4567, 'IMINT', 'Satellite imagery', 'A', 'ONE', '2024-10-15'),
    ('SIGINT-12', 'Increased radio activity in northern sector', 0.85, 'en', 51.4801, 31.5234, 'SIGINT', 'Radio intercepts', 'B', 'TWO', '2024-10-16'),
    ('HUMINT-12', 'Field reports indicate troop movements', 0.82, 'en', 51.4901, 31.5134, 'HUMINT', 'Informants', 'B', 'TWO', '2024-10-16'),
    ('OSINT-12', 'Social media activity spike in region', 0.75, 'en', 51.5174, 31.4667, 'OSINT', 'Social media monitoring', 'C', 'THREE', '2024-10-16'),
    ('CYBERINT-12', 'Network traffic analysis shows increased activity', 0.88, 'en', 51.5274, 31.4767, 'CYBERINT', 'Network traffic analysis', 'A', 'ONE', '2024-10-16'),
    ('IMINT-13', 'Drone surveillance footage of installations', 0.87, 'en', 51.5374, 31.4867, 'IMINT', 'Drone surveillance', 'A', 'ONE', '2024-10-17'),
    ('SIGINT-13', 'Communications intercept analysis', 0.83, 'en', 51.5474, 31.4967, 'SIGINT', 'Communications monitoring', 'B', 'TWO', '2024-10-17'),
    ('HUMINT-13', 'Local source reports on movements', 0.78, 'en', 51.5574, 31.5067, 'HUMINT', 'Informants', 'C', 'THREE', '2024-10-17'),
    ('OSINT-13', 'Analysis of public satellite imagery', 0.72, 'en', 51.5674, 31.5167, 'OSINT', 'News media and publications', 'C', 'THREE', '2024-10-17'),
    ('CYBERINT-13', 'Malware detection in infrastructure', 0.86, 'en', 51.5774, 31.5267, 'CYBERINT', 'Malware analysis', 'A', 'ONE', '2024-10-17'),
    ('IMINT-14', 'New construction activity detected', 0.89, 'en', 51.5874, 31.5367, 'IMINT', 'Satellite imagery', 'A', 'ONE', '2024-10-18'),
    ('SIGINT-14', 'Electronic signals analysis', 0.84, 'en', 51.5974, 31.5467, 'SIGINT', 'Electronic signals', 'B', 'TWO', '2024-10-18'),
    ('HUMINT-14', 'Informant network intelligence', 0.79, 'en', 51.6074, 31.5567, 'HUMINT', 'Informants', 'B', 'TWO', '2024-10-18'),
    ('OSINT-14', 'Public infrastructure changes noted', 0.73, 'en', 51.6174, 31.5667, 'OSINT', 'News media and publications', 'C', 'THREE', '2024-10-18'),
    ('CYBERINT-14', 'Dark web activity monitoring', 0.87, 'en', 51.6274, 31.5767, 'CYBERINT', 'Dark web monitoring', 'A', 'ONE', '2024-10-18'),
    
    -- Eastern Cluster (25 points)
    ('HUMINT-15', 'Network of informants reporting increased activity', 0.8, 'en', 50.4501, 32.5234, 'HUMINT', 'Informants', 'B', 'TWO', '2024-10-17'),
    ('IMINT-15', 'Satellite analysis of eastern region', 0.85, 'en', 50.4601, 32.5334, 'IMINT', 'Satellite imagery', 'A', 'ONE', '2024-10-17'),
    ('SIGINT-15', 'Radio communications monitoring', 0.82, 'en', 50.4701, 32.5434, 'SIGINT', 'Radio intercepts', 'B', 'TWO', '2024-10-17'),
    ('OSINT-15', 'Public source intelligence gathering', 0.75, 'en', 50.4801, 32.5534, 'OSINT', 'Social media monitoring', 'C', 'THREE', '2024-10-17'),
    ('CYBERINT-15', 'Cyber infrastructure analysis', 0.88, 'en', 50.4901, 32.5634, 'CYBERINT', 'Network traffic analysis', 'A', 'ONE', '2024-10-17'),
    ('IMINT-16', 'Aerial surveillance operations', 0.86, 'en', 50.5001, 32.5734, 'IMINT', 'Aerial photography', 'A', 'ONE', '2024-10-18'),
    ('SIGINT-16', 'Signal intelligence collection', 0.83, 'en', 50.5101, 32.5834, 'SIGINT', 'Electronic signals', 'B', 'TWO', '2024-10-18'),
    ('HUMINT-16', 'Human intelligence network reports', 0.79, 'en', 50.5201, 32.5934, 'HUMINT', 'Informants', 'B', 'TWO', '2024-10-18'),
    ('OSINT-16', 'Open source intelligence analysis', 0.74, 'en', 50.5301, 32.6034, 'OSINT', 'News media and publications', 'C', 'THREE', '2024-10-18'),
    ('CYBERINT-16', 'Digital infrastructure monitoring', 0.87, 'en', 50.5401, 32.6134, 'CYBERINT', 'Network traffic analysis', 'A', 'ONE', '2024-10-18'),
    
    -- Southern Cluster (25 points)
    ('OSINT-17', 'Social media analysis indicates movement patterns', 0.75, 'en', 49.2226, 30.7111, 'OSINT', 'Social media monitoring', 'C', 'THREE', '2024-10-18'),
    ('IMINT-17', 'Satellite monitoring of southern sector', 0.88, 'en', 49.2326, 30.7211, 'IMINT', 'Satellite imagery', 'A', 'ONE', '2024-10-18'),
    ('SIGINT-17', 'Communications intelligence gathering', 0.84, 'en', 49.2426, 30.7311, 'SIGINT', 'Radio intercepts', 'B', 'TWO', '2024-10-18'),
    ('HUMINT-17', 'Field agent intelligence collection', 0.81, 'en', 49.2526, 30.7411, 'HUMINT', 'Informants', 'B', 'TWO', '2024-10-18'),
    ('CYBERINT-17', 'Cyber security monitoring', 0.89, 'en', 49.2626, 30.7511, 'CYBERINT', 'Network traffic analysis', 'A', 'ONE', '2024-10-18'),
    ('IMINT-18', 'Drone reconnaissance operations', 0.87, 'en', 49.2726, 30.7611, 'IMINT', 'Drone surveillance', 'A', 'ONE', '2024-10-19'),
    ('SIGINT-18', 'Electronic intelligence analysis', 0.83, 'en', 49.2826, 30.7711, 'SIGINT', 'Electronic signals', 'B', 'TWO', '2024-10-19'),
    ('HUMINT-18', 'Local informant network reports', 0.78, 'en', 49.2926, 30.7811, 'HUMINT', 'Informants', 'C', 'THREE', '2024-10-19'),
    ('OSINT-18', 'Public information analysis', 0.73, 'en', 49.3026, 30.7911, 'OSINT', 'News media and publications', 'C', 'THREE', '2024-10-19'),
    ('CYBERINT-18', 'Digital threat assessment', 0.86, 'en', 49.3126, 30.8011, 'CYBERINT', 'Malware analysis', 'A', 'ONE', '2024-10-19'),
    
    -- Western Cluster (20 points)
    ('CYBERINT-19', 'Network security analysis reveals patterns', 0.85, 'en', 50.4501, 29.5234, 'CYBERINT', 'Network traffic analysis', 'B', 'TWO', '2024-10-19'),
    ('IMINT-19', 'Satellite surveillance of western region', 0.86, 'en', 50.4601, 29.5334, 'IMINT', 'Satellite imagery', 'A', 'ONE', '2024-10-19'),
    ('SIGINT-19', 'Signals intelligence monitoring', 0.82, 'en', 50.4701, 29.5434, 'SIGINT', 'Radio intercepts', 'B', 'TWO', '2024-10-19'),
    ('HUMINT-19', 'Human intelligence gathering', 0.79, 'en', 50.4801, 29.5534, 'HUMINT', 'Informants', 'B', 'TWO', '2024-10-19'),
    ('OSINT-19', 'Open source data collection', 0.74, 'en', 50.4901, 29.5634, 'OSINT', 'Social media monitoring', 'C', 'THREE', '2024-10-19'),
    ('IMINT-20', 'Aerial reconnaissance operations', 0.87, 'en', 50.5001, 29.5734, 'IMINT', 'Aerial photography', 'A', 'ONE', '2024-10-20'),
    ('SIGINT-20', 'Communications monitoring analysis', 0.83, 'en', 50.5101, 29.5834, 'SIGINT', 'Communications monitoring', 'B', 'TWO', '2024-10-20'),
    ('HUMINT-20', 'Field intelligence collection', 0.78, 'en', 50.5201, 29.5934, 'HUMINT', 'Informants', 'C', 'THREE', '2024-10-20'),
    ('OSINT-20', 'Public source analysis', 0.75, 'en', 50.5301, 29.6034, 'OSINT', 'News media and publications', 'C', 'THREE', '2024-10-20'),
    ('CYBERINT-20', 'Digital infrastructure assessment', 0.84, 'en', 50.5401, 29.6134, 'CYBERINT', 'Network traffic analysis', 'B', 'TWO', '2024-10-20')
    ''')

def downgrade():
    pass
