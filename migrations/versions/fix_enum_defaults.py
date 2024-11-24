"""fix enum defaults

Revision ID: fix_enum_defaults
Revises: initial_migration
Create Date: 2024-11-24 05:15:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fix_enum_defaults'
down_revision = 'initial_migration'
branch_labels = None
depends_on = None

def upgrade():
    # Update the default values to use proper enum values
    op.alter_column('intelligence_data', 'intel_type',
                   server_default='OSINT',
                   existing_type=postgresql.ENUM('IMINT', 'SIGINT', 'HUMINT', 'OSINT', 'CYBERINT', name='intel_type'))
    
    op.alter_column('intelligence_data', 'source_reliability',
                   server_default='F',
                   existing_type=postgresql.ENUM('A', 'B', 'C', 'D', 'E', 'F', name='source_reliability'))
    
    op.alter_column('intelligence_data', 'info_credibility',
                   server_default='SIX',
                   existing_type=postgresql.ENUM('ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', name='info_credibility'))

def downgrade():
    op.alter_column('intelligence_data', 'intel_type',
                   server_default='OSINT',
                   existing_type=postgresql.ENUM('IMINT', 'SIGINT', 'HUMINT', 'OSINT', 'CYBERINT', name='intel_type'))
    
    op.alter_column('intelligence_data', 'source_reliability',
                   server_default='F',
                   existing_type=postgresql.ENUM('A', 'B', 'C', 'D', 'E', 'F', name='source_reliability'))
    
    op.alter_column('intelligence_data', 'info_credibility',
                   server_default='6',
                   existing_type=postgresql.ENUM('1', '2', '3', '4', '5', '6', name='info_credibility'))
