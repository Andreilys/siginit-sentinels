"""update intel categorization

Revision ID: update_intel_categorization
Revises: reset_and_repopulate_data
Create Date: 2024-11-24 06:10:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'update_intel_categorization'
down_revision = 'reset_and_repopulate_data'
branch_labels = None
depends_on = None

def upgrade():
    # Update IMINT records
    op.execute('''
    UPDATE intelligence_data 
    SET intel_type = 'IMINT',
        intel_subtype = 'Satellite imagery'
    WHERE content LIKE '%Satellite%' OR content LIKE '%satellite%' OR content LIKE '%imagery%'
    ''')
    
    # Update SIGINT records
    op.execute('''
    UPDATE intelligence_data 
    SET intel_type = 'SIGINT',
        intel_subtype = 'Radio intercepts'
    WHERE content LIKE '%intercept%' OR content LIKE '%communications%' OR content LIKE '%radio%'
    ''')
    
    # Update HUMINT records
    op.execute('''
    UPDATE intelligence_data 
    SET intel_type = 'HUMINT',
        intel_subtype = 'Informants'
    WHERE content LIKE '%informant%' OR content LIKE '%source%' OR content LIKE '%agent%'
    ''')
    
    # Update OSINT records
    op.execute('''
    UPDATE intelligence_data 
    SET intel_type = 'OSINT',
        intel_subtype = 'Social media monitoring'
    WHERE content LIKE '%social%' OR content LIKE '%media%' OR content LIKE '%news%'
    ''')
    
    # Update CYBERINT records
    op.execute('''
    UPDATE intelligence_data 
    SET intel_type = 'CYBERINT',
        intel_subtype = 'Network traffic analysis'
    WHERE content LIKE '%cyber%' OR content LIKE '%network%' OR content LIKE '%malware%'
    ''')

def downgrade():
    # Since this is just updating existing records, we don't need a downgrade
    pass
