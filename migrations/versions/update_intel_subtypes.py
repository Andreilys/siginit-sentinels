"""update intel subtypes

Revision ID: update_intel_subtypes
Revises: update_intel_categorization
Create Date: 2024-11-24 06:15:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'update_intel_subtypes'
down_revision = 'update_intel_categorization'
branch_labels = None
depends_on = None

def upgrade():
    # First, ensure all records have proper intel types and subtypes based on content
    op.execute('''
    UPDATE intelligence_data
    SET intel_subtype = CASE
        WHEN intel_type = 'IMINT' AND content LIKE '%satellite%' THEN 'Satellite imagery'
        WHEN intel_type = 'IMINT' AND content LIKE '%drone%' THEN 'Drone surveillance'
        WHEN intel_type = 'SIGINT' AND (content LIKE '%intercept%' OR content LIKE '%communications%') THEN 'Radio intercepts'
        WHEN intel_type = 'SIGINT' AND content LIKE '%electronic%' THEN 'Electronic signals'
        WHEN intel_type = 'HUMINT' AND content LIKE '%informant%' THEN 'Informants'
        WHEN intel_type = 'HUMINT' AND content LIKE '%diplomatic%' THEN 'Diplomatic sources'
        WHEN intel_type = 'OSINT' AND content LIKE '%social%' THEN 'Social media monitoring'
        WHEN intel_type = 'OSINT' AND content LIKE '%news%' THEN 'News media and publications'
        WHEN intel_type = 'CYBERINT' AND content LIKE '%malware%' THEN 'Malware analysis'
        WHEN intel_type = 'CYBERINT' AND content LIKE '%dark web%' THEN 'Dark web monitoring'
        ELSE intel_subtype
    END
    WHERE intel_subtype IS NULL OR intel_subtype = 'Unknown'
    ''')

def downgrade():
    # Since this is just updating existing records, we don't need a downgrade
    pass
