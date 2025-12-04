"""create event hub tables

Revision ID: 002_event_hub
Revises: 001_initial_create_example_table
Create Date: 2025-12-03 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002_event_hub'
down_revision = '8f9de85ec2cc'  # Latest migration from the versions folder
branch_labels = None
depends_on = None


def upgrade():
    # Create events table
    op.create_table('events',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=300), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('event_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='upcoming'),
        sa.Column('max_participants', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('speaker_name', sa.String(length=200), nullable=True),
        sa.Column('speaker_avatar', sa.String(length=500), nullable=True),
        sa.Column('event_type', sa.String(length=100), nullable=True),
        sa.Column('google_calendar_id', sa.String(length=300), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_events_id', 'events', ['id'])
    op.create_index('ix_events_status', 'events', ['status'])
    op.create_index('ix_events_event_date', 'events', ['event_date'])

    # Create participants table
    op.create_table('participants',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('email', sa.String(length=200), nullable=False),
        sa.Column('avatar_url', sa.String(length=500), nullable=True),
        sa.Column('points', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('streak', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('rank_position', sa.Integer(), nullable=True),
        sa.Column('responses_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('quality_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('sentiment_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('joined_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('last_activity_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_participants_id', 'participants', ['id'])
    op.create_index('ix_participants_event_id', 'participants', ['event_id'])
    op.create_index('ix_participants_user_id', 'participants', ['user_id'])
    op.create_index('ix_participants_points', 'participants', ['points'])

    # Create questions table
    op.create_table('questions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('question_type', sa.String(length=50), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('options', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('is_ai_generated', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('ai_context', sa.Text(), nullable=True),
        sa.Column('asked_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_questions_id', 'questions', ['id'])
    op.create_index('ix_questions_event_id', 'questions', ['event_id'])
    op.create_index('ix_questions_order', 'questions', ['order'])

    # Create responses table
    op.create_table('responses',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('participant_id', sa.Integer(), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('sentiment', sa.String(length=50), nullable=True),
        sa.Column('sentiment_score', sa.Float(), nullable=True),
        sa.Column('quality_score', sa.Float(), nullable=True),
        sa.Column('ai_summary', sa.Text(), nullable=True),
        sa.Column('response_time_seconds', sa.Integer(), nullable=True),
        sa.Column('is_quick_option', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('points_awarded', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['participant_id'], ['participants.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_responses_id', 'responses', ['id'])
    op.create_index('ix_responses_question_id', 'responses', ['question_id'])
    op.create_index('ix_responses_participant_id', 'responses', ['participant_id'])
    op.create_index('ix_responses_sentiment', 'responses', ['sentiment'])

    # Create messages table
    op.create_table('messages',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('participant_id', sa.Integer(), nullable=True),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('message_type', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_messages_id', 'messages', ['id'])
    op.create_index('ix_messages_event_id', 'messages', ['event_id'])
    op.create_index('ix_messages_created_at', 'messages', ['created_at'])

    # Create badges table
    op.create_table('badges',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('display_name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('icon', sa.String(length=10), nullable=False),
        sa.Column('criteria_type', sa.String(length=50), nullable=False),
        sa.Column('criteria_value', sa.Integer(), nullable=False),
        sa.Column('rarity', sa.String(length=50), nullable=False, server_default='common'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index('ix_badges_id', 'badges', ['id'])
    op.create_index('ix_badges_name', 'badges', ['name'])

    # Create participant_badges table
    op.create_table('participant_badges',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('participant_id', sa.Integer(), nullable=False),
        sa.Column('badge_id', sa.Integer(), nullable=False),
        sa.Column('earned_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['participant_id'], ['participants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['badge_id'], ['badges.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_participant_badges_id', 'participant_badges', ['id'])
    op.create_index('ix_participant_badges_participant_id', 'participant_badges', ['participant_id'])
    op.create_index('ix_participant_badges_badge_id', 'participant_badges', ['badge_id'])


def downgrade():
    op.drop_index('ix_participant_badges_badge_id', table_name='participant_badges')
    op.drop_index('ix_participant_badges_participant_id', table_name='participant_badges')
    op.drop_index('ix_participant_badges_id', table_name='participant_badges')
    op.drop_table('participant_badges')
    
    op.drop_index('ix_badges_name', table_name='badges')
    op.drop_index('ix_badges_id', table_name='badges')
    op.drop_table('badges')
    
    op.drop_index('ix_messages_created_at', table_name='messages')
    op.drop_index('ix_messages_event_id', table_name='messages')
    op.drop_index('ix_messages_id', table_name='messages')
    op.drop_table('messages')
    
    op.drop_index('ix_responses_sentiment', table_name='responses')
    op.drop_index('ix_responses_participant_id', table_name='responses')
    op.drop_index('ix_responses_question_id', table_name='responses')
    op.drop_index('ix_responses_id', table_name='responses')
    op.drop_table('responses')
    
    op.drop_index('ix_questions_order', table_name='questions')
    op.drop_index('ix_questions_event_id', table_name='questions')
    op.drop_index('ix_questions_id', table_name='questions')
    op.drop_table('questions')
    
    op.drop_index('ix_participants_points', table_name='participants')
    op.drop_index('ix_participants_user_id', table_name='participants')
    op.drop_index('ix_participants_event_id', table_name='participants')
    op.drop_index('ix_participants_id', table_name='participants')
    op.drop_table('participants')
    
    op.drop_index('ix_events_event_date', table_name='events')
    op.drop_index('ix_events_status', table_name='events')
    op.drop_index('ix_events_id', table_name='events')
    op.drop_table('events')





