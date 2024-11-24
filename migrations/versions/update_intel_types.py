"""update intel types

Revision ID: update_intel_types
Revises: fix_enum_defaults
Create Date: 2024-11-24 05:35:00.000000

"""
from alembic import op
import sqlalchemy as sa
from models import IntelType

# revision identifiers, used by Alembic.
revision = 'update_intel_types'
down_revision = 'fix_enum_defaults'
branch_labels = None
depends_on = None

def upgrade():
    # Update intel types based on content and metadata
    op.execute('''
    UPDATE intelligence_data
    SET intel_type = 'SIGINT'
    WHERE content LIKE '%radio%' OR content LIKE '%signal%' OR content LIKE '%intercept%'
    ''')
    
    op.execute('''
    UPDATE intelligence_data
    SET intel_type = 'IMINT'
    WHERE content LIKE '%satellite%' OR content LIKE '%photo%' OR content LIKE '%imagery%'
    ''')
    
    op.execute('''
    UPDATE intelligence_data
    SET intel_type = 'HUMINT'
    WHERE content LIKE '%informant%' OR content LIKE '%agent%' OR content LIKE '%source%'
    ''')
    
    op.execute('''
    UPDATE intelligence_data
    SET intel_subtype = CASE
        WHEN content LIKE '%satellite%' THEN 'Satellite imagery'
        WHEN content LIKE '%drone%' THEN 'Drone surveillance'
        WHEN content LIKE '%radio%' THEN 'Radio intercepts'
        WHEN content LIKE '%informant%' THEN 'Informants'
        WHEN content LIKE '%social%' THEN 'Social media monitoring'
        WHEN content LIKE '%cyber%' THEN 'Network traffic analysis'
        ELSE intel_subtype
    END
    ''')

def downgrade():
    pass
