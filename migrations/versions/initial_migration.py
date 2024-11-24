"""initial migration

Revision ID: initial_migration
Revises: 
Create Date: 2024-11-24 05:10:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'initial_migration'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create enum types
    op.execute("CREATE TYPE intel_type AS ENUM ('IMINT', 'SIGINT', 'HUMINT', 'OSINT', 'CYBERINT')")
    op.execute("CREATE TYPE source_reliability AS ENUM ('A', 'B', 'C', 'D', 'E', 'F')")
    op.execute("CREATE TYPE info_credibility AS ENUM ('1', '2', '3', '4', '5', '6')")
    
    # Add new columns to intelligence_data table
    op.add_column('intelligence_data', sa.Column('intel_type', postgresql.ENUM('IMINT', 'SIGINT', 'HUMINT', 'OSINT', 'CYBERINT', name='intel_type'), nullable=False, server_default='OSINT'))
    op.add_column('intelligence_data', sa.Column('intel_subtype', sa.String(50), nullable=True))
    op.add_column('intelligence_data', sa.Column('source_reliability', postgresql.ENUM('A', 'B', 'C', 'D', 'E', 'F', name='source_reliability'), nullable=False, server_default='F'))
    op.add_column('intelligence_data', sa.Column('info_credibility', postgresql.ENUM('1', '2', '3', '4', '5', '6', name='info_credibility'), nullable=False, server_default='6'))

def downgrade():
    op.drop_column('intelligence_data', 'info_credibility')
    op.drop_column('intelligence_data', 'source_reliability')
    op.drop_column('intelligence_data', 'intel_subtype')
    op.drop_column('intelligence_data', 'intel_type')
    
    op.execute('DROP TYPE info_credibility')
    op.execute('DROP TYPE source_reliability')
    op.execute('DROP TYPE intel_type')
