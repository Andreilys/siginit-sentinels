"""fix sigint data

Revision ID: fix_sigint_data
Revises: add_sample_data
Create Date: 2024-11-24 05:50:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'fix_sigint_data'
down_revision = 'add_sample_data'
branch_labels = None
depends_on = None

def upgrade():
    # Update the record with intercepted communications to be SIGINT
    op.execute('''
    UPDATE intelligence_data 
    SET intel_type = 'SIGINT',
        intel_subtype = 'Radio intercepts'
    WHERE content LIKE '%intercept%' OR content LIKE '%communications%'
    ''')

def downgrade():
    pass
