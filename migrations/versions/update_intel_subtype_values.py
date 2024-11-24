"""update intel subtype values

Revision ID: update_intel_subtype_values
Revises: add_distributed_intel_data
Create Date: 2024-11-24 08:15:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'update_intel_subtype_values'
down_revision = 'add_distributed_intel_data'
branch_labels = None
depends_on = None

def upgrade():
    # Update IMINT subtypes
    op.execute("""
    UPDATE intelligence_data
    SET intel_subtype = CASE
        WHEN intel_subtype = 'Satellite imagery' THEN 'Satellite'
        WHEN intel_subtype = 'Drone surveillance' THEN 'Drone'
        WHEN intel_subtype = 'Aerial photography' THEN 'Aerial'
        ELSE intel_subtype
    END
    WHERE intel_type = 'IMINT'
    """)

    # Update SIGINT subtypes
    op.execute("""
    UPDATE intelligence_data
    SET intel_subtype = CASE
        WHEN intel_subtype = 'Radio intercepts' THEN 'Radio'
        WHEN intel_subtype = 'Communications monitoring' THEN 'Communications'
        WHEN intel_subtype = 'Electronic signals' THEN 'Signals'
        ELSE intel_subtype
    END
    WHERE intel_type = 'SIGINT'
    """)

    # Update HUMINT subtypes
    op.execute("""
    UPDATE intelligence_data
    SET intel_subtype = CASE
        WHEN intel_subtype = 'Diplomatic sources' THEN 'Diplomats'
        WHEN intel_subtype = 'Field agents' THEN 'Agents'
        ELSE intel_subtype
    END
    WHERE intel_type = 'HUMINT'
    """)

    # Update OSINT subtypes
    op.execute("""
    UPDATE intelligence_data
    SET intel_subtype = CASE
        WHEN intel_subtype = 'Social media monitoring' THEN 'Social Media'
        WHEN intel_subtype = 'News media and publications' THEN 'News'
        WHEN intel_subtype = 'Academic research' THEN 'Publications'
        ELSE intel_subtype
    END
    WHERE intel_type = 'OSINT'
    """)

    # Update CYBERINT subtypes
    op.execute("""
    UPDATE intelligence_data
    SET intel_subtype = CASE
        WHEN intel_subtype = 'Network traffic analysis' THEN 'Network'
        WHEN intel_subtype = 'Malware analysis' THEN 'Malware'
        WHEN intel_subtype = 'Dark web monitoring' THEN 'Dark Web'
        ELSE intel_subtype
    END
    WHERE intel_type = 'CYBERINT'
    """)

def downgrade():
    # Revert IMINT subtypes
    op.execute("""
    UPDATE intelligence_data
    SET intel_subtype = CASE
        WHEN intel_subtype = 'Satellite' THEN 'Satellite imagery'
        WHEN intel_subtype = 'Drone' THEN 'Drone surveillance'
        WHEN intel_subtype = 'Aerial' THEN 'Aerial photography'
        ELSE intel_subtype
    END
    WHERE intel_type = 'IMINT'
    """)

    # Revert SIGINT subtypes
    op.execute("""
    UPDATE intelligence_data
    SET intel_subtype = CASE
        WHEN intel_subtype = 'Radio' THEN 'Radio intercepts'
        WHEN intel_subtype = 'Communications' THEN 'Communications monitoring'
        WHEN intel_subtype = 'Signals' THEN 'Electronic signals'
        ELSE intel_subtype
    END
    WHERE intel_type = 'SIGINT'
    """)

    # Revert HUMINT subtypes
    op.execute("""
    UPDATE intelligence_data
    SET intel_subtype = CASE
        WHEN intel_subtype = 'Diplomats' THEN 'Diplomatic sources'
        WHEN intel_subtype = 'Agents' THEN 'Field agents'
        ELSE intel_subtype
    END
    WHERE intel_type = 'HUMINT'
    """)

    # Revert OSINT subtypes
    op.execute("""
    UPDATE intelligence_data
    SET intel_subtype = CASE
        WHEN intel_subtype = 'Social Media' THEN 'Social media monitoring'
        WHEN intel_subtype = 'News' THEN 'News media and publications'
        WHEN intel_subtype = 'Publications' THEN 'Academic research'
        ELSE intel_subtype
    END
    WHERE intel_type = 'OSINT'
    """)

    # Revert CYBERINT subtypes
    op.execute("""
    UPDATE intelligence_data
    SET intel_subtype = CASE
        WHEN intel_subtype = 'Network' THEN 'Network traffic analysis'
        WHEN intel_subtype = 'Malware' THEN 'Malware analysis'
        WHEN intel_subtype = 'Dark Web' THEN 'Dark web monitoring'
        ELSE intel_subtype
    END
    WHERE intel_type = 'CYBERINT'
    """)
