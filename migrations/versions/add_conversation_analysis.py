"""add conversation analysis

Revision ID: add_conversation_analysis
Revises: update_intel_subtype_values
Create Date: 2024-11-24 20:20:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'add_conversation_analysis'
down_revision = 'update_intel_subtype_values'
branch_labels = None
depends_on = None

def upgrade():
    # Create conversation_analysis table
    op.create_table(
        'conversation_analysis',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('priority_level', sa.String(length=50), nullable=False),
        sa.Column('risk_assessment', sa.Text(), nullable=False),
        sa.Column('key_insights', sa.Text(), nullable=False),
        sa.Column('critical_entities', JSONB, nullable=False),
        sa.Column('locations_mentioned', JSONB, nullable=False),
        sa.Column('sentiment_summary', sa.Text(), nullable=False),
        sa.Column('source_reliability', sa.String(length=50), nullable=False),
        sa.Column('information_credibility', sa.String(length=50), nullable=False),
        sa.Column('recommended_actions', JSONB, nullable=False),
        sa.Column('entity_relationships', sa.Text(), nullable=False),
        sa.Column('speakers', JSONB, nullable=False),
        sa.Column('conversation_duration', sa.String(length=50), nullable=False),
        sa.Column('analyzed_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )

    # Insert sample data
    op.execute('''
    INSERT INTO conversation_analysis (
        priority_level, risk_assessment, key_insights, critical_entities, 
        locations_mentioned, sentiment_summary, source_reliability, 
        information_credibility, recommended_actions, entity_relationships,
        speakers, conversation_duration, analyzed_at
    ) VALUES (
        'High',
        'Potential threat from enemy movement and positioning near Bakhmut.',
        'Enemy forces, including two armored vehicles and at least 12 infantrymen, are moving towards the speaker''s position near Bakhmut. They are approximately 800 meters south of Berkhivska Road and seem to be establishing a forward position. There is also movement towards Ivanivske, indicating a possible larger operation.',
        '["Bakhmut", "Berkhivska Road", "Ivanivske", "Dmitry", "Victor"]'::jsonb,
        '["Bakhmut", "Berkhivska Road", "Ivanivske"]'::jsonb,
        'The conversation reflects a sense of urgency and concern about enemy movements and the need for immediate support.',
        'B - Usually reliable',
        '2 - Probably True',
        '["Request immediate artillery support to target enemy movements before they reach the tree line.", "Monitor the installation of heavy weaponry by the enemy.", "Maintain current position and continue surveillance of enemy activities."]'::jsonb,
        'Speaker A and Speaker B are coordinating to monitor and respond to enemy movements near Bakhmut.',
        '["Speaker A", "Speaker B"]'::jsonb,
        'Short',
        '2023-10-21T00:00:00Z'
    )
    ''')

def downgrade():
    op.drop_table('conversation_analysis')
